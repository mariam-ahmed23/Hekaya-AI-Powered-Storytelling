import streamlit as st
import base64
from pathlib import Path
import sqlite3

st.set_page_config(page_title="حكايتنا ليك", layout="wide")

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

# --- Database setup ---
# DB_PATH = Path("stories.db")

# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS stories (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT,
#             video_path TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# def add_story(title, video_path):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("INSERT INTO stories (title, video_path) VALUES (?, ?)", (title, video_path))
#     conn.commit()
#     conn.close()

# def get_stories():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT id, title, video_path FROM stories")
#     data = c.fetchall()
#     conn.close()
#     return data

# # --- Initialize database ---
# init_db()

# --- Page Styling ---
st.markdown("""
<style>
body {
    background-color: #FFF8E7;
}
h1 {
    text-align: center;
    color: black;
    font-family: 'Cairo', sans-serif;
}
.story-card {
    background-color: white;
    border-radius: 15px;
    box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
    padding: 20px;
    margin: 20px auto;
    width: 80%;
    text-align: center;
}
.story-card h3 {
    color: #3B3B3B;
    font-family: 'Cairo', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
body {
    background-color: #FFF8E7;
}
.title {
    text-align: center;
    color: #FF6F61;
    font-family: 'Cairo', sans-serif;
    font-size: 40px;
    margin-bottom: 20px;
}
            </style>
""", unsafe_allow_html=True)
# --- Page Header ---

st.markdown("<div class='title'>حكايتنا</div>", unsafe_allow_html=True)
storys = {
    "ليلى و الغابه السحريه": "saved_videos/WhatsApp Video 2025-10-11 at 21.35.46_6cec20c1.mp4",
    "البحار و أعماق البحر": "saved_videos/grandma.mp4",
    "الكلب زغلول في الفضاء": "saved_videos/grandpa.mp4"}
cols_per_row=3
video_selected=None
items = list(storys.items())
for row_start in range(0, len(items), cols_per_row):
    cols = st.columns(cols_per_row)
    for i, (name, img) in enumerate(items[row_start:row_start + cols_per_row]):
        with cols[i]:
            if st.button(name, key=f"select_{row_start + i}"):
                video_selected=storys[name]
                
    st.video(video_selected)