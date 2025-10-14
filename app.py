import streamlit as st
import base64

# --- Page configuration ---
st.set_page_config(page_title="Hekaya", layout="wide")

st.markdown("""
<style>
div.stButton > button {
    background-color: #FFD700;   /* Gold */
    color: black;
    border-radius: 10px;
    height: 40px;
    width: 100%;
    border: 2px solid #FFB700;
    font-weight: 800;
    font-size: 160px;
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
                      
    


# --- Set background ---
def set_bg(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/webp;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg(r"D:\Data Science\HireReady CV\Hekaya _app\ChatGPT Image Oct 8, 2025, 10_02_03 PM.png")

st.markdown("""
<style>
.hero {
    position: relative;
    height: 100vh;
     /* Keep original colors */
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    font-family: 'Cairo', sans-serif;
    animation: fadeIn 2s ease-in-out;
}

/* Transparent glass-like content box */
.hero-content {
    background-color: rgba(255, 255, 255, 0.25);
    border-radius: 25px;
    padding: 60px 80px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    backdrop-filter: blur(6px);
    animation: float 5s ease-in-out infinite;
}

/* Floating animation */
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}

/* Fade-in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero h1 {
    font-size: 64px;
    color: #FF6F61;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.hero p {
    font-size: 26px;
    color: black;
    margin-top: 15px;
    max-width: 800px;
}
</style>

<div class="hero">
    <div class="hero-content">
        <h1> اهلا بك في <span style="color:#FFD700;">حِكايَة</span> 🌟</h1>
        <p>عالم القصص اللي فيه الخيال بيحيا، والمغامرة بتبدأ من هنا 🎬  
        اكتشف قصص جديدة، شارك حكايتك، وخليك جزء من عالم مليان إبداع وضحك وحب 💫</p>
    </div>
</div>
""", unsafe_allow_html=True)



# --- Load and encode video ---
video_path = "Home_page.mp4"
try:
    with open(video_path, "rb") as f:
        video_base64 = base64.b64encode(f.read()).decode("utf-8")
except FileNotFoundError:
    video_base64 = None
    st.error(f"❌ لم يتم العثور على الفيديو في: {video_path}")

# --- Display styled card with embedded video ---
if video_base64:
    st.markdown(f"""
    <style>
    .video-card {{
        background-color: #FFF8E7;
        border-radius: 20px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.15);
        padding: 20px;
        text-align: center;
        width: 80%;
        margin: 40px auto;
        transition: transform 0.3s ease;
    }}
    .video-card:hover {{
        transform: scale(1.02);
    }}
    .video-title {{
        font-size: 22px;
        color: #FF6F61;
        font-family: 'Cairo', sans-serif;
        margin-bottom: 15px;
    }}
    .video-container video {{
        border-radius: 15px;
        width: 100%;
        height: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    </style>

    <div class="video-card">
        <div class="video-title">ايه هى حِكايَة</div>
        <div class="video-container">
            <video controls autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                متصفحك لا يدعم عرض الفيديو.
            </video>
        </div>
    </div>
    """, unsafe_allow_html=True)
##########################
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
img1 = get_base64_image("library.jpg")
img2 = get_base64_image("imaginations.jpg")
st.markdown( f"""
<style>
.nav-section {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 30px;
    margin-top: 40px;
}}
.nav-card {{
    background-color: #FFF8E7;
    border-radius: 20px;
    box-shadow: 2px 4px 10px rgba(0,0,0,0.15);
    width: 250px;
    padding: 20px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}
.nav-card:hover {{
    transform: scale(1.05);
    box-shadow: 4px 6px 14px rgba(0,0,0,0.2);
}}
.nav-card img {{
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 15px;
}}
.nav-card p {{
    font-family: 'Cairo', sans-serif;
    font-size: 18px;
    color: #3B3B3B;
    margin-top: 10px;
}}
</style>

<h2 style='text-align:center; color:#FF6F61; font-family:Cairo;'>🌈 اختار وجهتك في عالم حِكايَة</h2>

<div class="nav-section">

<a href="?page=stories" target="stories" style="text-decoration:none;">
    <div class="nav-card">
        <img src="data:image/jpg;base64,{img1}">
        <p>حكايتنا ليك</p>
    </div>
</a>

<a href="?page=create" target="your_story" style="text-decoration:none;">
    <div class="nav-card">
        <img src="data:image/jpg;base64,{img2}">
        <p>حكايتك</p>
    </div>
</a>

<a href="?page=about" target="our_Char" style="text-decoration:none;">
    <div class="nav-card">
        <img src="https://cdn-icons-png.flaticon.com/512/1828/1828884.png">
        <p>اتعرف على شخصيتنا</p>
    </div>
</a>

</div>
""", unsafe_allow_html=True)

