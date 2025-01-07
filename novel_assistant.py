import streamlit as st
from deepseek_api import generate_outline_stream

def init_session_state():
    """初始化session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = ""
    if 'outline' not in st.session_state:
        st.session_state.outline = ""
    if 'chapters' not in st.session_state:
        st.session_state.chapters = ""
    if 'chapter_contents' not in st.session_state:
        st.session_state.chapter_contents = {}
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = "主题创建"

def stream_output(stream_generator, placeholder):
    """处理流式输出"""
    full_response = ""
    for chunk in stream_generator:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            placeholder.markdown(full_response)
    return full_response

def main():
    st.set_page_config(layout="wide", page_title="AI小说创作助手")
    init_session_state()
    
    st.title("AI小说创作助手")
    st.markdown("### 欢迎使用AI小说创作助手")
    
    # 主题输入
    if not st.session_state.theme:
        st.header("第一步：输入小说主题")
        theme_input = st.text_input("请输入您想要创作的小说主题：")
        if st.button("开始创作", key="start_button"):
            if theme_input.strip():
                st.session_state.theme = theme_input
                st.session_state.current_stage = "大纲生成"
                st.rerun()
            else:
                st.error("请输入主题！")
    else:
        st.info(f"当前创作主题：{st.session_state.theme}")
        if st.button("重新开始", key="restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # 显示创作进度
    st.divider()
    st.markdown("### 创作进度")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.outline:
            st.success("✅ 大纲已完成")
        else:
            st.info("⏳ 待创作大纲")
            
    with col2:
        if st.session_state.chapters:
            st.success("✅ 目录已完成")
        else:
            st.info("⏳ 待创作目录")
            
    with col3:
        if st.session_state.chapter_contents:
            st.success(f"✅ 已完成 {len(st.session_state.chapter_contents)} 个章节")
        else:
            st.info("⏳ 待创作章节")

if __name__ == "__main__":
    main() 