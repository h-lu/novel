import streamlit as st
from deepseek_api import generate_chapters_stream
from novel_assistant import stream_output

st.set_page_config(layout="wide", page_title="章节目录")

if 'outline' not in st.session_state or not st.session_state.outline:
    st.warning("请先生成小说大纲！")
    st.stop()

st.title("📑 章节目录")

if not st.session_state.chapters:
    st.markdown("### 当前大纲")
    with st.expander("查看大纲"):
        st.write(st.session_state.outline)
    
    if st.button("生成章节目录", key="generate_chapters"):
        chapters_placeholder = st.empty()
        with st.spinner("正在生成章节目录..."):
            stream = generate_chapters_stream(st.session_state.outline)
            st.session_state.chapters = stream_output(stream, chapters_placeholder)
            st.session_state.current_stage = "章节创作"
else:
    st.success("章节目录已生成")
    st.markdown("### 当前目录")
    st.write(st.session_state.chapters)
    
    with st.expander("查看大纲"):
        st.write(st.session_state.outline)
    
    if st.button("重新生成目录"):
        st.session_state.chapters = ""
        st.rerun() 