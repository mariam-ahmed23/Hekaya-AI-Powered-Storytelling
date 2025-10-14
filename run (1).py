import os
import uuid
import base64
import subprocess
import requests
import streamlit as st
from pydub import AudioSegment
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import soundfile as sf
import numpy as np


st.set_page_config(page_title="Story Generator (LLM + TTS + Video)", page_icon="🎧", layout="centered")


LLM_API_KEY = 
TTS_API_KEY = 


def ensure_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        st.error("❌ ffmpeg غير موجود. برجاء تثبيته في البيئة قبل تشغيل التطبيق.")

# ======================================
# 🧠 Node 1 — Generate Story (Arabic + 2 mins)
# ======================================
def node_generate_story(prompt: str) -> str:
    prompt_with_limit = (
        "اكتب القصة باللهجة المصرية فقط، واجعلها مكتوبة بالكامل باللغة العربية، "
        "بأسلوب شيق ومناسب للأطفال، مع حبكة قصيرة وممتعة، "
        "ولا تتجاوز مدة روايتها دقيقتين عندما تُروى بصوت طبيعي. "
        "ابدأ القصة بناءً على الفكرة التالية: " + prompt
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
# 🔊 Node 2 — Text to Speech (Arabic + Egyptian)
# ======================================
def node_text_to_speech(story_text: str):
    MODEL = "models/gemini-2.5-pro-preview-tts"
    URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={TTS_API_KEY}"

    style_instruction = (
        "اتكلم باللهجة المصرية الطبيعية، بصوت واضح ومليان حيوية كأنك بتحكي للأطفال قصة ممتعة. "
        "خلي النطق مصري أصيل (ج = g، ق = ’a) والنبرة فيها دفء وضحك بسيط، "
        "زي الراوي في كرتون مصري بيحكي للأطفال بحماس وود. "
        "خلي الأداء يكون فيه مشاعر حقيقية ودفء، وحافظ على الأسلوب العربي المصري الممزوج بالعربية الفصحى الخفيفة.\n\n"
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": style_instruction + story_text}]}],
        "generationConfig": {
            "response_modalities": ["AUDIO"],
            "speech_config": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Leda"}}}
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL, headers=headers, json=payload)

    if response.status_code != 200:
        st.error(f"❌ خطأ {response.status_code}: {response.text}")
        return None, None

    result = response.json()
    try:
        audio_base64 = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    except KeyError:
        st.error("❌ لم يتم العثور على بيانات الصوت في الاستجابة.")
        return None, None

    raw_bytes = base64.b64decode(audio_base64)
    audio_np = np.frombuffer(raw_bytes, dtype=np.int16)
    wav_path = os.path.abspath(f"story_audio_{uuid.uuid4().hex[:6]}.wav")
    sf.write(wav_path, audio_np, samplerate=24000, subtype="PCM_16")

    # Normalize & fix frame rate
    audio = AudioSegment.from_wav(wav_path).set_frame_rate(24000)
    audio.export(wav_path, format="wav")

    with open(wav_path, "rb") as f:
        wav_bytes = f.read()

    return wav_path, wav_bytes

# ======================================
# 🎬 Node 3 — LatentSync Video Generation
# ======================================
def node_generate_video(audio_path: str):
    st.info("🎬 جاري إنشاء الفيديو باستخدام Latent Sync...")

    try:
        cwd = os.getcwd()
        latentsync_dir = "/teamspace/studios/this_studio/LatentSync"
        os.chdir(latentsync_dir)

        base_video_path = os.path.join(latentsync_dir, "cartoongda.mp4")
        output_name = f"cartoon_output_{uuid.uuid4().hex[:6]}.mp4"
        output_path = os.path.join(latentsync_dir, output_name)

        if not os.path.exists(base_video_path):
            st.error("❌ ملف الفيديو الأساسي cartoon4women.mp4 غير موجود.")
            os.chdir(cwd)
            return None

        command = [
            "python", "-m", "scripts.inference",
            "--unet_config_path", "configs/unet/stage2_512.yaml",
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
            return output_path
        else:
            st.error("❌ فشل إنشاء الفيديو.")
            st.text(result.stderr)
            return None

    except Exception as e:
        st.error(f"⚠️ خطأ أثناء إنشاء الفيديو: {e}")
        return None

# ======================================
# 🚀 STREAMLIT APP (with session_state)
# ======================================
st.title("🎙️ مُنشئ القصص باللهجة المصرية بالصوت والفيديو 🎬")

ensure_ffmpeg_installed()

# Initialize session state
for key in ["story", "audio_path", "audio_bytes", "video_path"]:
    if key not in st.session_state:
        st.session_state[key] = None

prompt = st.text_area("✍️ اكتب فكرة القصة:", "اكتب لي قصة قصيرة عن فتاة شجاعة تعيش في الصحراء وتكتشف كنزًا سحريًا.")

if st.button("🚀 إنشاء القصة + الصوت + الفيديو"):
    # 🧠 Generate Story
    with st.spinner("🧠 جاري إنشاء القصة..."):
        st.session_state.story = node_generate_story(prompt)
        st.subheader("📖 القصة الناتجة")
        st.write(st.session_state.story)

    # 🔊 Generate Audio
    with st.spinner("🎤 جاري إنشاء الصوت..."):
        st.session_state.audio_path, st.session_state.audio_bytes = node_text_to_speech(st.session_state.story)
        if st.session_state.audio_bytes:
            st.success("✅ تم إنشاء الصوت بنجاح.")
            st.audio(st.session_state.audio_bytes, format="audio/wav")

    # 🎬 Generate Video
    if st.session_state.audio_path:
        with st.spinner("🎞️ جاري إنشاء الفيديو..."):
            st.session_state.video_path = node_generate_video(st.session_state.audio_path)
            if st.session_state.video_path:
                st.video(st.session_state.video_path)
                st.success("🎬 تم إنشاء الفيديو بنجاح!")

# ✅ Display saved state even after rerun
if st.session_state.story:
    st.subheader("📖 القصة:")
    st.write(st.session_state.story)

if st.session_state.audio_bytes:
    st.subheader("🎧 الصوت:")
    st.audio(st.session_state.audio_bytes, format="audio/wav")
    st.download_button(
        "⬇️ تحميل الصوت",
        data=st.session_state.audio_bytes,
        file_name=os.path.basename(st.session_state.audio_path),
        mime="audio/wav"
    )

if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    st.subheader("🎬 الفيديو:")
    st.video(st.session_state.video_path)
