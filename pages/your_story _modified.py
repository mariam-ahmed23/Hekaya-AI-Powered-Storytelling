import os
import uuid
import base64
import subprocess
import requests
import streamlit as st
from pydub import AudioSegment
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from pathlib import Path

# --- Page configuration ---

# ======================================
# 🧠 Node 1 — Generate Story (Max 2 mins)
# ======================================
def node_generate_story(prompt: str) -> str:
    prompt_with_limit = (
        prompt + " اكتب القصة بحيث تكون مدتها عندما تتلى دقيقة كحد أقصى."
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=LLM_API_KEY,
        temperature=0.7
    )

    response = llm.invoke([HumanMessage(content=prompt_with_limit)])
    content = getattr(response, "content", response)

    if isinstance(content, list):
        if len(content) > 0:
            if isinstance(content[0], dict) and "text" in content[0]:
                story = content[0]["text"]
            else:
                story = content[0]
        else:
            story = ""
    else:
        story = content

    return str(story).strip()

# ======================================
# 🔊 Node 2 — Text to Speech (Robust WAV)
# ======================================
def node_text_to_speech(story_text: str,voice):
    import soundfile as sf
    import numpy as np

    MODEL = "models/gemini-2.5-pro-preview-tts"
    URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={TTS_API_KEY}"

    # 🎙️ Style prompt
    style_instruction = (
            "Read aloud in a clear and natural Egyptian Arabic accent, "
            "using authentic Egyptian pronunciation (ج = g, ق = ’a). "
            "Deliver the story with a warm, friendly, and cartoon-like tone — "
            "as if narrating a fun story for children, full of emotion and liveliness.\n\n"
        )
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": style_instruction + story_text}]
        }],
        "generationConfig": {
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL, headers=headers, json=payload)

    if response.status_code != 200:
        st.error(f"❌ Error {response.status_code}: {response.text}")
        return None, None

    result = response.json()
    audio_base64 = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    raw_bytes = base64.b64decode(audio_base64)

    # ✅ Decode 16-bit PCM and fix playback speed
    audio_np = np.frombuffer(raw_bytes, dtype=np.int16)
    wav_path = os.path.abspath(f"story_audio_{uuid.uuid4().hex[:6]}.wav")
    sf.write(wav_path, audio_np, samplerate=24000, subtype="PCM_16")

    # 🔁 Normalize and ensure consistent frame rate
    audio = AudioSegment.from_wav(wav_path).set_frame_rate(24000)
    audio.export(wav_path, format="wav")

    # 📦 Return audio for Streamlit
    with open(wav_path, "rb") as f:
        wav_bytes = f.read()

    return wav_path, wav_bytes

# ======================================
# 🎬 Node 3 — LatentSync Video Generation
# ======================================
def node_generate_video(audio_path: str,base_video_path):
    st.info("🎬 Running Latent Sync for video generation...")

    try:
        cwd = os.getcwd()
        latentsync_dir = "LatentSync"
        os.chdir(latentsync_dir)


        # ✅ مخرج الفيديو النهائي في نفس المكان
        output_name = f"cartony_{uuid.uuid4().hex[:6]}.mp4"
        output_path = f"{output_name}"

        command = [
            "python", "-m", "scripts.inference",
            "--unet_config_path", "configs/unet/stage2_efficient.yaml",
            "--inference_ckpt_path", "checkpoints/latentsync_unet.pt",
            "--inference_steps", "25",
            "--guidance_scale", "2.0",
            "--video_path", base_video_path,
            "--audio_path", audio_path,
            "--video_out_path", output_path
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        os.chdir(cwd)

        if result.returncode == 0 and os.path.exists(output_path):
            st.success(f"✅ Video generated successfully: {output_path}")
            return output_path
        else:
            st.error(f"❌ LatentSync Error:\n{result.stderr}")
            st.warning("Video generation failed or output file not found.")
            return None

    except Exception as e:
        st.error(f"⚠️ Exception while running LatentSync: {e}")
        return None

#________________________________
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
        if st.button("حكايتك"):
            st.switch_page("pages/your_story.py")
    with col4:
        if st.button("اتعرف على شخصيتنا"):
            st.switch_page("pages/our_Char.py")  
    with col6:
        st.image("logo2.jpg",width=100)
    with col5:
        if st.button("2حكايتك"):
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

# --- Container Box for Input story title ---
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

st.markdown("""
<style>
.character-card {
    position: relative;
    text-align: center;
    margin-bottom: 20px;
}
.character-card img {
    width: 100%;
    border-radius: 15px;
    box-shadow: 2px 4px 8px rgba(0,0,0,0.2);
}
.character-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(255, 215, 0, 0.9); /* Gold with transparency */
    color: black;
    border: 2px solid #FFB700;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
.character-button:hover {
    background-color: #FF6F61;
    color: white;
    transform: translate(-50%, -50%) scale(1.05);
}
</style>
""", unsafe_allow_html=True)


# --- Title Section ---
st.markdown("<div class='title'>✏️ أنشئ قصتك الخاصة</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>اكتب فكرة بسيطة أو موضوع القصة، وخلي خيالك يرسم الأحداث ✨</div>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown('<div class="container-box">', unsafe_allow_html=True)
with st.container():
    prompt = st.text_input("اكتب موضوع حكيتك هنا:", placeholder="مثلاً: قطة صغيرة بتدور على صديق جديد...")
st.markdown('</div>', unsafe_allow_html=True)

#--- Character selection section ---
characters = {
    "ليلى": "char\WhatsApp Image 2025-10-08 at 00.41.05_1370b935.jpg",
    "حمزه": "char\WhatsApp Image 2025-10-08 at 10.31.21_18364218.jpg",
    "الجد": "char\grandpa.jpg",
    "الجدة": "char\grandma.jpg",
    "لولو": "char\little_girl.jpg",
    "مريم": r"char/red_head_girl.jpg",
    "احمد": "char\man.jpg"
}
st.markdown("<h2 style='text-align: center; color: #FF6F61; font-family: Cairo, sans-serif;'> اختار شخصيتك المفضلة</h2>", unsafe_allow_html=True)

cols = st.columns(len(characters))
selected_character = None
voice={
    "ليلى":'Laomedeia',
    "الجدة":"Gacrux",
    "الجد":"Algieba",
    "حمزه":"Fenrir",
    "لولو": "erinome",
    "مريم": "kore",
    "احمد": "puck"
}

videos={
    "ليلى":"videos\woman.mp4",
    "الجدة":"videos\grandma.mp4",
    "الجد":"videos\grandpa.mp4",
    "حمزه":"video_rabbit.mp4",
    "لولو": "videos\littel girl (online-video-cutter.com).mp4",
    "مريم": "videos\Generating_Talking_Head_Video.mp4",
    "احمد": "videos\man.mp4"
}


cols_per_row=3
items = list(characters.items())
for row_start in range(0, len(items), cols_per_row):
    cols = st.columns(cols_per_row)
    for i, (name, img) in enumerate(items[row_start:row_start + cols_per_row]):
        with cols[i]:
            st.image(img, use_container_width=True)
            if st.button(name, key=f"select_{row_start + i}"):
                st.session_state["selected_character"] = name
                st.session_state["selected_voice"] = voice[name]
                st.session_state["selected_video"] = videos[name]
        

if st.session_state.get("selected_character"):
    st.success(f"✅ اخترت: {st.session_state['selected_character']}")
    
with st.container():
    generate = st.button("🎬 أنشئ القصة", key="generate_btn")

# --- Placeholder for generated content ---
if generate:
    if prompt.strip() == "":
        st.warning("📝 من فضلك اكتب موضوع القصة أولاً!")
    else:
        st.success(f"🌟 جاري إنشاء قصة عن: **{prompt}** ...")
        story = node_generate_story(prompt)
        if story:
            audio_path, audio_bytes = node_text_to_speech(story,st.session_state['selected_voice'])
        else:
            st.error("خطأ في أنشأ القصه")

        if audio_path:    
            video_path = node_generate_video(audio_path,st.session_state["selected_video"])
            st.video(video_path)
        else: 
            st.error("خطأ في أنشأالصوت")   

        

                
        
        