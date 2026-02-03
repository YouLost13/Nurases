import streamlit as st
import whisper
import os
from fpdf import FPDF
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="NURASES v1.1", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFC0CB; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ffcbdb; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ NURASES | Nur Hanım İçin ")
st.subheader("Hafif Otistik Yazılımcın Hediyesidir ") #
st.write("---")

# Dosya Yükleme
audio_file = st.file_uploader("Türkçe Ses Dosyasını Buraya Bırak (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file)
    
    # Model Seçimi (Kaliteyi buradan ayarlıyoruz)
    model_size = st.select_slider("Yapay Zeka Zeka Seviyesi (Yükseldikçe kalite artar, süre uzar)", options=["base", "small", "medium"], value="small")

    if st.button("🚀 Ver Coşguyu (Türkçe Odaklı)"):
        with st.spinner(f'Yapay Zeka ({model_size} model) Bekle Kral Çözümüyom...'):
            # Geçici kayıt
            with open("temp_audio.mp3", "wb") as f:
                f.write(audio_file.read())
            
            # 1. Zekayı Yükselttik: Seçtiğin model yüklenecek
            model = whisper.load_model(model_size)
            
            # 2. Türkçeyi Sabitledik: language="tr" komutuyla hata payını azalttık
            result = model.transcribe("temp_audio.mp3", language="tr", task="transcribe")
            text_output = result["text"]
            
            st.success("İşlem Başarılı!")
            st.text_area("Çıkarılan Net Metin:", text_output, height=300)
            
            # PDF Çıktısı (Karakter hatası almamak için temizleme yapıldı)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            safe_text = text_output.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=safe_text)
            pdf.output("rapor.pdf")
            
            st.download_button("📂 PDF Raporunu Al", open("rapor.pdf", "rb"), file_name="nurases_rapor.pdf")

st.write("---")

st.caption("Saygılarımla: Helena | Tony Stark") #


