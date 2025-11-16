# app.py (Streamlit main) - IT Helpdesk Assistant
import streamlit as st
from config.config import settings
from models.llm import get_chat_model
from models.embeddings import get_embeddings_client
from utils.rag import build_faiss_index_from_texts, retrieve_from_index
from utils.web_search import serpapi_search
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import traceback

st.set_page_config(page_title="IT Helpdesk Assistant", layout="wide", initial_sidebar_state="expanded")

def show_exception(e):
    st.error(str(e))
    st.write(traceback.format_exc())

with st.sidebar:
    st.title("IT Helpdesk Assistant")
    st.markdown("Upload internal IT docs (SOPs, runbooks, KB articles) to build a knowledge base for RAG.")
    uploaded_files = st.file_uploader("Upload docs (multiple)", accept_multiple_files=True, type=['txt','md','pdf'])
    st.markdown('---')
    st.markdown('Response mode')
    mode = st.radio('', ['Concise','Detailed'])
    st.markdown('---')
    if st.button('Build / Rebuild RAG index'):
        st.session_state.get('rebuild', True)
    st.markdown('⚠️ Deploy: ensure env variables are set in Streamlit Cloud')

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hello — I am the IT Helpdesk Assistant. Upload docs or ask a question!"}]
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'docs_texts' not in st.session_state:
    st.session_state.docs_texts = []

if uploaded_files:
    texts = []
    for f in uploaded_files:
        try:
            raw = f.read()
            if isinstance(raw, bytes):
                try:
                    txt = raw.decode('utf-8')
                except Exception:
                    try:
                        from PyPDF2 import PdfReader
                        f.seek(0)
                        reader = PdfReader(f)
                        pages = [p.extract_text() for p in reader.pages]
                        txt = '\n'.join(pages)
                    except Exception:
                        txt = ''
            else:
                txt = str(raw)
            texts.append(txt)
        except Exception as e:
            st.warning(f"Could not read {f.name}: {e}")

    if texts:
        try:
            with st.spinner('Building vector index...'):
                vs = build_faiss_index_from_texts(texts)
                st.session_state.vectorstore = vs
                st.session_state.docs_texts = texts
                st.success('RAG index built and stored in session.')
        except Exception as e:
            show_exception(e)

st.title("🤖 IT Helpdesk Assistant")
st.write("Upload SOPs or KB articles, build an index, then ask operational questions. Use 'Concise' for quick steps or 'Detailed' for full procedures.")

chat_col, status_col = st.columns([4,1])

with chat_col:
    for m in st.session_state.messages:
        role = m['role']
        if role == 'user':
            with st.chat_message('user'):
                st.markdown(m['content'])
        else:
            with st.chat_message('assistant'):
                st.markdown(m['content'])

    prompt = st.chat_input("e.g., 'How do I reset a Windows domain password?' or 'Steps to onboard a new developer laptop'")

    if prompt:
        st.session_state.messages.append({'role':'user','content':prompt})
        sys_prompt = (
            "You are an IT Helpdesk Assistant. Prioritize safety, clarity, and step-by-step troubleshooting. "
            "When citing internal docs, include short source excerpts and recommend next steps. "
            "If the answer is not found locally, perform a web search and summarize findings. "
            "Keep responses in the requested mode: Concise or Detailed."
        )

        answer_text = None
        try:
            if st.session_state.vectorstore:
                results = retrieve_from_index(st.session_state.vectorstore, prompt, k=4)
                if results:
                    ctx = "\n\n".join([f"Source score {score:.3f}:\n{doc.page_content[:800]}..." for doc, score in results])
                    msgs = [SystemMessage(content=sys_prompt),
                            HumanMessage(content=f"Use the following internal context to answer the query.\n\nCONTEXT:\n{ctx}\n\nQuery: {prompt}\nAnswer in {mode} mode and include 'Source:' lines.")]
                    chat = get_chat_model()
                    try:
                        resp = chat.generate(messages=[msgs[0], msgs[1]])
                        answer_text = resp.generations[0][0].text
                    except Exception:
                        try:
                            resp = chat.invoke([msgs[0], msgs[1]])
                            answer_text = resp.content
                        except Exception:
                            answer_text = "Error: could not get model response"
                    st.session_state.messages.append({'role':'assistant','content':answer_text})
                else:
                    st.info("No relevant documents found in local index.")
            else:
                st.info("No local index available — trying web search fallback.")
        except Exception as e:
            st.warning(f"RAG retrieval failed: {e}")

        if not answer_text:
            try:
                web_snippets = []
                try:
                    web_snippets = serpapi_search(prompt, num_results=3)
                except Exception:
                    st.info("Live web search not available or API key missing.")

                web_context = ""
                if web_snippets:
                    web_context = "\n\n".join([f"{r['title']}\n{r.get('snippet','')}\n{r.get('link','')}" for r in web_snippets])

                chat = get_chat_model()
                messages = [SystemMessage(content=sys_prompt)]
                if web_context:
                    messages.append(HumanMessage(content=f"Use these web search results:\n{web_context}\n\nQuestion: {prompt}\nAnswer in {mode} mode and provide recommended next steps."))
                else:
                    messages.append(HumanMessage(content=f"Answer the question: {prompt}\nAnswer in {mode} mode."))

                try:
                    resp = chat.generate(messages=messages)
                    final_answer = resp.generations[0][0].text
                except Exception:
                    try:
                        resp = chat.invoke(messages)
                        final_answer = resp.content
                    except Exception:
                        final_answer = "Error: could not get model response"
                st.session_state.messages.append({'role':'assistant','content':final_answer})

            except Exception as e:
                show_exception(e)

        st.experimental_rerun()

with status_col:
    st.markdown("### Status")
    if st.session_state.vectorstore:
        st.success("RAG index: built")
    else:
        st.info("RAG index: not built")
    st.markdown("---")
    st.markdown("Environment")
    st.text(f"Provider: {settings.PROVIDER}")
    st.text(f"LLM model: {settings.LLM_MODEL}")
