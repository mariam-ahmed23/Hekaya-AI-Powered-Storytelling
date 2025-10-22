# Hekaya – AI-Powered Storytelling Companion

> **“Turning your imagination into animated stories.”**

Hekaya is an **AI-powered storytelling platform** that transforms children’s ideas into **personalized animated tales**.  
It combines **language models**, **text-to-speech**, and **lip-sync animation** to generate **interactive Egyptian-Arabic story videos** — fun, creative, and educational.

---

## 🎬Overview

Children often lose interest in static, traditional stories.  
**Hekaya** reimagines storytelling by using AI to create **interactive, culture-fit narratives** that teach values, spark imagination, and engage emotionally.  

With just a **text prompt**, Hekaya can generate either:
- A **narrated story** (audio + talking character), or  
- A **fully animated short story video.**

---

##  Core Features

###  Feature 1: Narrated Stories

Bring cartoon characters to life with expressive narration.

**Workflow**
1. **User Input:** Story idea (text prompt).  
2. **LLM:** Generates full story script.  
3. **TTS:** Converts script into Egyptian-Arabic speech audio.  
4. **User Selects:** Cartoon character.  
5. **Integration:** LatentSync aligns lip movements with the audio.  
6. **Output:** Video with a character narrating the story.  

 *Result:* A personalized storytelling video where the character tells the story in natural Egyptian Arabic.

---

### 🎞️ Feature 2: Animated Stories

Transform an idea into a complete animated short film.

**Workflow**
1. **User Input:** Story idea (text prompt).  
2. **LLM:** Generates the full story.  
3. **LLM:** Divides the story into multiple scenes or prompts.  
4. **Loop:** Each scene is sent to **Veo (video generation model)**.  
5. **Combine:** Merge generated scenes into one cohesive video.  
6. **Output:** Fully animated story video.  

 *Result:* A dynamic cartoon video with consistent characters, transitions, and scenes.

---

## ⚙️ System Architecture

```text
[User Input] 
      ↓
[LLM - Gemini/Qwen 2.5]
      ↓
[Story Script]
      ↓
[TTS - Gemini 2.5 Pro] → [Audio File]
      ↓
[Lip Sync - LatentSync] → [Character Animation]
      ↓
[Streamlit UI] → [Final Video Output]
```

---

##  Models & Technologies

| Component | Model / Tool | Purpose |
|------------|---------------|----------|
| **LLM** | Gemini  | Story generation & scene division |
| **TTS** | Gemini 2.5 Pro | Natural Egyptian-Arabic speech |
| **Lip Sync** | LatentSync | Character facial animation |
| **Video Generation** | Veo | Scene animation |
| **Frontend** | Streamlit | User interaction & video playback |
| **Database** | SQLite | Store stories, audio, and characters |

---

## 🧩 Workflow Summary

1. **Input Story Idea:** User enters a short text prompt.  
2. **AI Processing:** LLM → TTS → Animation pipeline.  
3. **Rendering:** Streamlit app displays final video with synchronized narration.  
4. **Storage:** SQLite database stores story data for reuse.  

---

## 🖥️ Demo

🎥 **Watch Demo Video:**  
[▶️ View Demo](./demo.mp4)

> The demo showcases the full process — from text prompt to AI-generated story video using Egyptian-Arabic narration.

---

## 💼 Business Use Cases

- **Schools & Educational Platforms:** Cultural and moral stories for classrooms.  
- **Content Studios:** Automate cartoon production.  
- **Therapists & Counselors:** Use storytelling for emotional learning.  
- **Brands & Organizations:** Story-driven campaigns and awareness content.  

---

## Competitive Advantages

✅ Runs locally — no expensive API costs  
✅ Consistent characters across all scenes  
✅ Long-form and scene-based storytelling  
✅ Natural voice and expressive facial sync  
✅ Unlimited story generation on mid-range GPUs  

---


## Team Members

| Name |
|------|
| **Mariam Ahmed** |
| **Nouran Khaled** | 
| **Jana Mohamed** | 
| **Tasneem Mohsen** | 
| **Roaa Ehab** | 

---

## 🧾 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/YourUsername/Hekaya.git
cd Hekaya

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open your browser to interact with the Hekaya interface.

---



