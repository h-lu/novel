import streamlit as st
from deepseek_api import generate_outline_stream, call_deepseek_api_stream
from novel_assistant import stream_output

st.set_page_config(layout="wide", page_title="大纲创作")

if 'theme' not in st.session_state or not st.session_state.theme:
    st.warning("请先在主页设置创作主题！")
    st.stop()

if 'outline_confirmed' not in st.session_state:
    st.session_state.outline_confirmed = False

st.title("📝 小说大纲")
st.info(f"当前主题：{st.session_state.theme}")

def modify_outline(current_outline, user_feedback):
    """根据用户反馈修改大纲"""
    prompt = f"""请根据用户的反馈意见修改以下小说大纲：

当前大纲：
{current_outline}

用户反馈：
{user_feedback}

请保持相同的格式，给出修改后的完整大纲。"""
    
    return call_deepseek_api_stream(prompt, max_tokens=4000)

# 未生成大纲
if not st.session_state.outline:
    if st.button("生成大纲", key="generate_outline"):
        outline_placeholder = st.empty()
        with st.spinner("正在生成大纲..."):
            stream = generate_outline_stream(st.session_state.theme)
            st.session_state.outline = stream_output(stream, outline_placeholder)
            st.session_state.current_stage = "章节规划"

# 已生成大纲但未确认
elif not st.session_state.outline_confirmed:
    st.success("大纲已生成，请审阅并提出修改意见")
    
    # 显示当前大纲
    st.markdown("### 当前大纲")
    st.write(st.session_state.outline)
    
    # 用户反馈区
    st.markdown("### 修改建议")
    user_feedback = st.text_area(
        "请输入您对大纲的修改建议（如果满意请直接点击确认按钮）：",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("修改大纲", key="modify_outline"):
            if user_feedback.strip():
                outline_placeholder = st.empty()
                with st.spinner("正在根据您的建议修改大纲..."):
                    stream = modify_outline(st.session_state.outline, user_feedback)
                    st.session_state.outline = stream_output(stream, outline_placeholder)
                st.rerun()
            else:
                st.warning("请输入修改建议！")
    
    with col2:
        if st.button("确认大纲", key="confirm_outline"):
            st.session_state.outline_confirmed = True
            st.rerun()
    
    with col3:
        if st.button("重新生成大纲", key="regenerate_outline"):
            st.session_state.outline = ""
            st.rerun()

# 大纲已确认
else:
    st.success("✅ 大纲已确认")
    st.markdown("### 最终大纲")
    st.write(st.session_state.outline)
    
    if st.button("重新编辑大纲", key="edit_again"):
        st.session_state.outline_confirmed = False
        st.rerun() 