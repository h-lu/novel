import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 配置API密钥
# 从环境变量中获取API密钥
# 需要在.env文件中添加:
# DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 初始化客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def call_deepseek_api(prompt, max_tokens=100):
    """
    基础API调用示例
    
    Args:
        prompt: 输入提示文本
        max_tokens: 生成的最大token数量
        
    Returns:
        返回模型生成的回复内容
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def call_deepseek_api_stream(prompt, max_tokens=100):
    """
    流式API调用
    
    Args:
        prompt: 输入提示文本
        max_tokens: 生成的最大token数量
        
    Returns:
        返回流式响应对象
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
        stream=True
    )
    
    return response

def generate_outline(theme):
    """
    根据主题生成小说大纲
    
    Args:
        theme: 小说主题
    Returns:
        返回生成的大纲
    """
    prompt = f"""请根据主题"{theme}"创建一个详细的小说大纲，包括以下方面：
    1. 故事背景
    2. 主要人物设定
    3. 核心冲突
    4. 主要情节发展
    5. 结局走向
    请用清晰的条目形式组织。"""
    
    return call_deepseek_api(prompt, max_tokens=4000)

def generate_outline_stream(theme):
    """使用生成器返回大纲流"""
    prompt = f"""请根据主题"{theme}"创建一个详细的小说大纲，包括以下方面：
    1. 故事背景
    2. 主要人物设定
    3. 核心冲突
    4. 主要情节发展
    5. 结局走向
    请用清晰的条目形式组织。"""
    
    return call_deepseek_api_stream(prompt, max_tokens=4000)

def generate_chapters(outline):
    """
    根据大纲生成章节目录
    
    Args:
        outline: 小说大纲
    Returns:
        返回章节目录列表
    """
    prompt = f"""基于以下小说大纲，请创建一个详细的章节目录：
    {outline}
    
    请列出10-15个章节，每个章节都要有标题和简短的内容概述。
    格式要求：每章一行，章节序号-章节标题：内容概述"""
    
    return call_deepseek_api(prompt, max_tokens=4000)

def generate_chapters_stream(outline):
    """使用生成器返回章节目录流"""
    prompt = f"""基于以下小说大纲，请创建一个详细的章节目录：
    {outline}
    
    请列出10-15个章节，每个章节都要有标题和简短的内容概述。
    格式要求：每章一行，章节序号-章节标题：内容概述"""
    
    return call_deepseek_api_stream(prompt, max_tokens=4000)

def write_chapter(outline, chapter_info):
    """
    写作具体章节内容
    
    Args:
        outline: 小说大纲
        chapter_info: 章节信息
    Returns:
        返回章节具体内容
    """
    prompt = f"""请基于以下信息写作小说章节：
    
    总体大纲：
    {outline}
    
    本章节信息：
    {chapter_info}
    
    要求：
    1. 字数在2000字左右
    2. 注意情节连贯性
    3. 细致描写场景和人物
    4. 适当运用对话推进情节
    5. 注意文学性和可读性"""
    
    return call_deepseek_api(prompt, max_tokens=4000)

def write_chapter_stream(outline, chapter_info):
    """使用生成器返回章节内容流"""
    prompt = f"""请基于以下信息写作小说章节：
    
    总体大纲：
    {outline}
    
    本章节信息：
    {chapter_info}
    
    要求：
    1. 字数在2000字左右
    2. 注意情节连贯性
    3. 细致描写场景和人物
    4. 适当运用对话推进情节
    5. 注意文学性和可读性"""
    
    return call_deepseek_api_stream(prompt, max_tokens=4000)

# # 示例调用
# prompt = "你好，世界！"
# response = call_deepseek_api(prompt)
# print(response)