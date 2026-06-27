import streamlit as st
import requests
import time

# --- 1. DESIGN N'ISHUSHO YA WEBSITE (UI CONFIG) ---
st.set_page_config(
    page_title="AECGI Super AI Engine", 
    page_icon="🎬", 
    layout="wide"
)

# Isura n'Ibyapa bya Hollywood Enterprise
st.title("🎬 AECGI SUPER AI VIDEO ENGINE v10.0")
st.subheader("Hollywood-Grade Animation & CGI Automation Studio")
st.write("Urubuga rwa Kinyamwuga rwo Gukora no Guhindura Video na CGI Ukoresheje AI")

st.markdown("---")

# --- 2. SIDEBAR CONFIGURATIONS (API KEY MANAGEMENT) ---
st.sidebar.header("⚙️ AECGI Core Settings")
st.sidebar.write("Umutekano n'Imiyoborere ya System")
replicate_key = st.sidebar.text_input("Shyiramo Replicate API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.info(
    "ℹ️ Iyi Engine ikorana na Modeli zihambaye za AI (nk'iza Luma cyangwa Runway) "
    "kuri Replicate API hub, ikazana amashusho meza cyane yo mu rurego rwa CGI."
)

# --- 3. THE MAIN VIDEO & CGI ENGINE ---
st.header("🎞️ Generator & Prompt Studio")
st.write("Shyiraho Ibisobanuro (Prompt), uheze ukande buto ngo AI iguhe video ishashagirana.")

# Akajambo gafasha umuser gukora prompt zikomeye
ai_editing_prompt = st.text_area(
    "Andika Prompt ya Video cyangwa CGI Script hano:",
    placeholder="Urugero: A high-speed Jeep Trackhawk racing through Kigali streets, tactical cars with guns attached, massive Hollywood explosions, cinematic lighting, 8k resolution, photorealistic CGI..."
)

# Guhitamo ishusho (Aspect Ratio)
aspect_ratio = st.selectbox("Hitemo Imiterere ya Video (Aspect Ratio):", ["16:9", "9:16", "1:1"])

st.markdown("###")

# --- 4. TANGIRA GUKORA VIDEO ---
if st.button("🚀 Tangira Gukora Video / Render CGI") and ai_editing_prompt:
    if not replicate_key:
        st.error("⚠️ Ugomba gushyiramo Replicate API Key mu ruhande (Sidebar) ngo iyi Engine ifungure umuyoboro!")
    else:
        with st.spinner("AECGI AI Core iri gukorana na Server za Replicate... Tegereza gato..."):
            try:
                headers = {
                    "Authorization": f"Token {replicate_key}",
                    "Content-Type": "application/json"
                }
                
                # Iyi ni modeli ihambaye ya Luma-Dream-Machine cyangwa Generative Video kuri Replicate
                data = {
                    "version": "14a1a666cfd4e9a0f023f05d60e7e0fb845ff4b13ee4ed6f8da956e10816999a", 
                    "input": {
                        "prompt": ai_editing_prompt,
                        "aspect_ratio": aspect_ratio
                    }
                }
                
                # Kohereza Itegeko kuri Replicate
                response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=data)
                prediction_id = response.json().get("id")
                
                if prediction_id:
                    status = "starting"
                    ai_video_url = ""
                    
                    # Gukurikiranira hafi niba video yuzuye (Polling loop)
                    while status not in ["succeeded", "failed"]:
                        time.sleep(5)
                        check_res = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
                        status = check_res.json().get("status")
                        
                        if status == "succeeded":
                            ai_video_url = check_res.json().get("output")
                            break
                        elif status == "failed":
                            break
                    
                    if ai_video_url:
                        st.success("✅ Filime/CGI yawe iruzuye neza kandi irarangiye!")
                        
                        # Kwerekana Video yuzuye kuri Website
                        if isinstance(ai_video_url, list):
                            st.video(ai_video_url[0])
                        else:
                            st.video(ai_video_url)
                            
                        st.balloons()
                    else:
                        st.error("⚠️ AI yanze guhindura video yawe cyangwa igihe cyarayirangiranye. Ongera ugerageze.")
                else:
                    st.error("⚠️ Replicate API Key yawe ifite ikibazo cyangwa account yawe nta credit (mafaranga) iriho.")
            except Exception as e:
                st.error(f"⚠️ Haza ikosa mu mivugururire: {e}")
