import streamlit as st
import base64
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
import json, time, os
from google import genai
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Gemini client
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
# Veo client
veo_client = genai.Client(api_key=VEO_API_KEY)

# ======================
# 🧩 تعريف الحالة (State)
# ======================
class StoryState(TypedDict):
    idea: str
    story: str
    scenes: List[Dict]
    video_paths: List[str]
    final_video: str

# ======================
# 🧠 Node 1 - Gemini Story
# ======================
def generate_story(state: StoryState):
    print("🧠 توليد القصة باللهجة المصرية...")
    prompt = f"""
    اكتب قصة قصيرة باللهجة المصرية مدتها حوالي 30 ثانية عن:
    {state['idea']}
    خليها ظريفة، مناسبة للأطفال، وفيها شخصيات كرتونية.
    """
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    story = response.text
    return {**state, "story": story}

# ======================
# ✂️ Node 2 - Scene Splitter
# ======================
def split_story(state: StoryState):
    print("✂️ تقسيم القصة إلى مشاهد...")
    prompt = f"""
    قسم القصة التالية إلى 4 مشاهد متتابعة (كل مشهد حوالي 7 ثواني)
    وارجع النتيجة بصيغة JSON كده:
    [
        {{"scene_number": 1, "description": "..." }},
        {{"scene_number": 2, "description": "..." }},
        {{"scene_number": 3, "description": "..." }},
        {{"scene_number": 4, "description": "..." }}
    ]
    القصة:
    {state['story']}
    """
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text
    try:
        scenes = json.loads(text)
    except Exception:
        print("⚠️ فشل في JSON، تقسيم بديل...")
        scenes = [{"scene_number": i + 1, "description": s.strip()} for i, s in enumerate(state["story"].split(".")[:4])]
    return {**state, "scenes": scenes}

# ======================
# 🎬 Node 3 - Veo Scene Generator
# ======================
def generate_videos(state: StoryState):
    print("🎬 توليد الفيديوهات بالمشاهد...")
    video_paths = []
    for scene in state["scenes"]:
        prompt = scene["description"]
        print(f"🎥 توليد المشهد {scene['scene_number']}...")
        operation = veo_client.models.generate_videos(
            model="veo-3.0-generate-001",
            prompt=prompt,
        )

        while not operation.done:
            print(f"⏳ انتظار المشهد {scene['scene_number']}...")
            time.sleep(10)
            operation = veo_client.operations.get(operation)

        generated_video = operation.response.generated_videos[0]
        veo_client.files.download(file=generated_video.video)
        filename = f"scene_{scene['scene_number']}.mp4"
        generated_video.video.save(filename)
        video_paths.append(filename)
        print(f"✅ تم حفظ المشهد: {filename}")

    return {**state, "video_paths": video_paths}

# ======================
# 🎞️ Node 4 - Merge Videos
# ======================
def merge_videos(state: StoryState):
    print("🎞️ دمج الفيديوهات...")
    clips = [VideoFileClip(v) for v in state["video_paths"]]
    final = concatenate_videoclips(clips, method="compose")
    final_filename = "final_story.mp4"
    final.write_videofile(final_filename, codec="libx264", audio=False)
    print(f"✅ تم حفظ الفيديو النهائي: {final_filename}")
    return {**state, "final_video": final_filename}

# ======================
# 🧠 بناء الـ LangGraph
# ======================
graph = StateGraph(StoryState)

graph.add_node("generate_story", generate_story)
graph.add_node("split_story", split_story)
graph.add_node("generate_videos", generate_videos)
graph.add_node("merge_videos", merge_videos)

# التسلسل
graph.add_edge(START, "generate_story")
graph.add_edge("generate_story", "split_story")
graph.add_edge("split_story", "generate_videos")
graph.add_edge("generate_videos", "merge_videos")
graph.add_edge("merge_videos", END)

# بناء الرسم البياني
story_graph = graph.compile()

    


st.set_page_config(page_title="حكايتك", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #FFF8E7;  /* soft creamy beige */
}
div.stButton > button {
    background-color: #FFD700;   /* Gold */
    color: black;
    border-radius: 10px;
    height: 40px;
    width: 100%;
    border: 2px solid #FFB700;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #FFB700;
    color: white;
}
</style>
""", unsafe_allow_html=True)



# --- Toolbar at the top ---
toolbar = st.container()
with toolbar:
    col1, col2, col3, col4,col5,col6 = st.columns([1, 1, 1, 2,4,1])
    with col1:
        if st.button("حكاية"):
            st.switch_page("app.py")
    with col2:
        if st.button("حكايتنا ليك"):
            st.switch_page("pages/stories.py")
    with col3:
        if st.button("احكايتك"):
            st.switch_page("pages/your_story.py")
    with col4:
        if st.button("اتعرف على شخصيتنا"):
            st.switch_page("pages/our_Char.py")  
    with col6:
        st.image("logo2.jpg",width=100)
    with col5:
        if st.button("حكايتك"):
            st.switch_page("pages/model2.py")         
st.markdown("""
<style>
body {
    background-color: #FFF8E7;
}
.title {
    text-align: center;
    color: #FF6F61;
    font-family: 'Cairo', sans-serif;
    font-size: 36px;
    margin-bottom: 20px;
}
.subtitle {
    text-align: center;
    color: #3B3B3B;
    font-family: 'Cairo', sans-serif;
    margin-bottom: 40px;
}
.input-box {
    background-color: black;
    color: black;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
    width: 80%;
    margin: auto;
}
.input[type="text"] {
    background-color: white !important;
    color: #3B3B3B !important;
    border: 2px solid #FF6F61 !important;
    border-radius: 10px !important;
    padding: 10px !important; 
}


.generate-btn {
    display: block;
    width: 200px;
    margin: 20px auto;
    align-items: center;
    background-color: #FFD700;
    color: #3B3B3B;
    border: none;
    padding: 10px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
}
.generate-btn:hover {
    background-color: #FF6F61;
    color: white;
}
.video-box {
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    width: 80%;
    margin: 30px auto;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.container-box {
    background-color: #FFF8E7;  /* creamy background */
    padding: 30px;
    border-radius: 20px;
    box-shadow: 2px 4px 10px rgba(0,0,0,0);
    width: 0%;
    margin: 30px auto;
    text-align: center;
}
input[type="text"] {
    background-color: white !important;
    color: #3B3B3B !important;
    border: 2px solid #FF6F61 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
            </style>
""", unsafe_allow_html=True)
# --- Title Section ---
st.markdown("<div class='title'>✏️ أنشئ قصتك الخاصة</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>اكتب فكرة بسيطة أو موضوع القصة، وخلي خيالك يرسم الأحداث ✨</div>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown('<div class="container-box">', unsafe_allow_html=True)
with st.container():
    subject = st.text_input("اكتب موضوع حكيتك هنا:", placeholder="مثلاً: قطة صغيرة بتدور على صديق جديد...")
st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    generate = st.button("🎬 أنشئ القصة", key="generate_btn")

if generate:
    if subject.strip() == "":
        st.warning("📝 من فضلك اكتب موضوع القصة أولاً!")
    else:
        st.success(f"🌟 جاري إنشاء قصة عن: **{subject}** ...")

        # Placeholder video section
        st.markdown("<div class='video-box'>🎥 الفيديو هيظهر هنا بعد ما يتولد</div>", unsafe_allow_html=True)

        inputs = {"idea": subject}
        result = story_graph.invoke(inputs)
        print("🎬 الفيديو النهائي:", result["final_video"])
        final= result["final_video"]

        video_path = Path(final)
        if video_path.exists():
            with open(video_path, "rb") as f:
                st.video(f.read())
            st.success("✅ تم إنشاء الفيديو بنجاح! اتفرج على حكايتك تحت 👇")
    