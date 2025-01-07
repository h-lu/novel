import streamlit as st
from deepseek_api import write_chapter_stream
from novel_assistant import stream_output

st.set_page_config(layout="wide", page_title="章节创作")

if 'chapters' not in st.session_state or not st.session_state.chapters:
    st.warning("请先生成章节目录！")
    st.stop()

st.title("📖 章节创作")

# 左侧：章节选择和创作
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### 选择章节")
    chapter_list = [ch for ch in st.session_state.chapters.split('\n') if ch.strip()]
    selected_chapter = st.selectbox(
        "选择要创作的章节",
        chapter_list
    )
    
    if st.button("创作此章节", key="write_chapter"):
        if selected_chapter not in st.session_state.chapter_contents:
            chapter_placeholder = st.empty()
            with st.spinner(f"正在创作 {selected_chapter}..."):
                stream = write_chapter_stream(
                    st.session_state.outline,
                    selected_chapter
                )
                content = stream_output(stream, chapter_placeholder)
                st.session_state.chapter_contents[selected_chapter] = content
                st.session_state.current_stage = f"已完成：{selected_chapter}"
        else:
            st.warning("该章节已创作完成！")

    # 显示创作进度
    st.markdown("### 创作进度")
    total_chapters = len(chapter_list)
    completed_chapters = len(st.session_state.chapter_contents)
    progress = completed_chapters / total_chapters
    st.progress(progress)
    st.write(f"已完成 {completed_chapters}/{total_chapters} 章")

# 右侧：章节内容展示
with right_col:
    st.markdown("### 章节内容")
    if selected_chapter in st.session_state.chapter_contents:
        st.write(st.session_state.chapter_contents[selected_chapter])
        if st.button("重写本章"):
            del st.session_state.chapter_contents[selected_chapter]
            st.rerun()
    else:
        st.info("尚未创作此章节内容")

# 底部：参考信息
with st.expander("查看大纲与目录"):
    tab1, tab2 = st.tabs(["📝 大纲", "📑 目录"])
    with tab1:
        st.write(st.session_state.outline)
    with tab2:
        st.write(st.session_state.chapters) 