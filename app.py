import streamlit as st
from agent import generate_travel_guide
import os
from dotenv import load_dotenv

# .env dosyasındaki ortam değişkenlerini (varsa) yükle
load_dotenv()

# Streamlit sayfa ayarları
st.set_page_config(page_title="AI Tur Rehberi", page_icon="🌍", layout="centered")

# CSS ile biraz görsel zenginlik katalım
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌍 AI Tur Rehberi & Planlayıcı</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Tüm dünyadan tarihi şehirleri keşfedin ve saniyeler içinde kişisel seyahat rotanızı oluşturun!</div>', unsafe_allow_html=True)

# Kullanıcı Girdi Alanları (Ana Ekranda)
st.markdown("### ✈️ Seyahat Detayları")
col1, col2 = st.columns([3, 1])
with col1:
    cities = st.text_input("Gidilecek Şehir(ler)", placeholder="Örn: İstanbul, Roma, Tokyo")
with col2:
    days = st.number_input("Gün Sayısı", min_value=1, max_value=30, value=3)

st.markdown("### 🔑 API Ayarları")
api_key_input = st.text_input(
    "Google Gemini API Anahtarı", 
    type="password", 
    value=os.getenv("GEMINI_API_KEY", ""),
    help="Kendi Google Gemini API anahtarınızı buraya girin. Eğer bir .env dosyanız varsa otomatik olarak yüklenecektir."
)
st.caption("[Buradan API anahtarı alabilirsiniz](https://aistudio.google.com/app/apikey)")

st.info("Bu uygulama, yapay zeka desteğiyle gidilecek yerlerdeki **tarihi mekanlar** hakkında bilgiler verir ve size özel günlük **gezi planı (itinerary)** çıkarır.")
st.markdown("<br>", unsafe_allow_html=True)

# Ana Buton ve Sonuç Gösterimi
if st.button("🗺️ Rehberimi Oluştur!", type="primary"):
    if not cities:
        st.warning("Lütfen gitmek istediğiniz şehir veya şehirleri girin.")
    elif not api_key_input:
        st.warning("Lütfen Gemini API Anahtarınızı girin.")
    else:
        with st.spinner(f"{cities} için {days} günlük harika bir plan hazırlanıyor..."):
            # Ajanımızdan yanıtı al
            guide_result = generate_travel_guide(cities, days, api_key_input)
            
            st.success("Rehberiniz Hazır! İyi yolculuklar! 🎉")
            
            # Sonucu bir kutu içinde Markdown olarak göster
            st.markdown("---")
            st.markdown(guide_result)
