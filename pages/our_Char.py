import streamlit as st
import base64

st.set_page_config(page_title="اتعرف على شخصيتنا", layout="wide")

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
    

# Function to encode local images
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Encode your images
img1 = get_base64_image("char/WhatsApp Image 2025-10-08 at 00.41.05_1370b935.jpg")
img2 = get_base64_image("char/WhatsApp Image 2025-10-08 at 10.31.21_18364218.jpg")
img3 = get_base64_image("char/man.jpg")
img4 = get_base64_image("char/grandma.jpg")
img5 = get_base64_image("char/grandpa.jpg")
img6 = get_base64_image("char/red_head_girl.jpg")
img7 = get_base64_image("char/little_girl.jpg")




st.markdown(f"""
<style>
.story-card {{
    background-color: #FFF8E7;
    border-radius: 15px;
    box-shadow: 2px 4px 8px rgba(0,0,0,0.1);
    padding: 10px;
    text-align: center;
    width: 250px;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
}}
.story-card:hover {{
    transform: scale(1.07);
    box-shadow: 4px 8px 16px rgba(255, 111, 97, 0.4);
}}
.story-card img {{
    border-radius: 10px;
    width: 100%;
    height: 180px;
    object-fit: cover;
    transition: transform 0.4s ease-in-out;
}}
.story-card:hover img {{
    transform: scale(1.05);
}}
.story-card p {{
    color: #3B3B3B;
    font-size: 16px;
    margin-top: 8px;
    transition: color 0.3s;
}}
.story-card:hover p {{
    color: #FF6F61;
}}
.story-gallery {{
    display: flex;
    justify-content: center;
    gap: 25px;
    flex-wrap: wrap;
}}
</style>

<div class="story-gallery">
    <div class="story-card">
        <img src="data:image/jpg;base64,{img1}">
        <p>ليلى</p>
    </div>
    <div class="story-card">
        <img src="data:image/jpg;base64,{img2}">
        <p>حمزه</p>
    </div>
    <div class="story-card">
        <img src="data:image/jpg;base64,{img3}">
        <p>احمد</p>
    </div>
    <div class="story-card">
        <img src="data:image/jpg;base64,{img4}">
        <p>الجدة</p>
    </div>
    <div class="story-card">
        <img src="data:image/jpg;base64,{img5}">
        <p>الجد</p>
    </div>
    <div class="story-card">
        <img src="data:image/jpg;base64,{img6}">
        <p>مريم</p>
    </div>
    <div class="story-card">
        <img src="data:image/jpg;base64,{img7}">
        <p>لولو</p>
    </div>
</div>

""", unsafe_allow_html=True)
