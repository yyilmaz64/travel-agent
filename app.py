import streamlit as st
from agent import generate_travel_guide, generate_transport_plan, generate_hotel_plan
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
    import datetime
    today = datetime.date.today()
    dates = st.date_input("Seyahat Tarihleri", value=(today, today + datetime.timedelta(days=3)), min_value=today)
    
if dates and len(dates) == 2:
    start_date, end_date = dates
else:
    start_date = end_date = None

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
if st.button("🗺️ Planımı Oluştur!", type="primary"):
    if not cities:
        st.warning("Lütfen gitmek istediğiniz şehir veya şehirleri girin.")
    elif not start_date or not end_date:
        st.warning("Lütfen geçerli bir gidiş ve dönüş tarihi seçin.")
    elif not api_key_input:
        st.warning("Lütfen Gemini API Anahtarınızı girin.")
    else:
        st.success("Sistem çalışıyor, lütfen bekleyin... 🎉")
        st.markdown("---")
        
        # 3 Sekme (Tab) oluştur
        tab1, tab2, tab3 = st.tabs(["🗺️ Seyahat Rotası", "✈️ Ulaşım (Uçak/Tren)", "🏨 Konaklama (Otel)"])
        
        with tab1:
            with st.spinner(f"{cities} için tarihi rehber ve rota hazırlanıyor..."):
                guide_result = generate_travel_guide(cities, start_date, end_date, api_key_input)
                st.markdown(guide_result)
                
        with tab2:
            with st.spinner(f"{cities} için uçuş ve tren seçenekleri aranıyor..."):
                transport_result = generate_transport_plan(cities, start_date, end_date, api_key_input)
                st.markdown(transport_result)
                
        with tab3:
            with st.spinner(f"Otel ve konaklama fiyatları tahmin ediliyor..."):
                hotel_result = generate_hotel_plan(cities, start_date, end_date, api_key_input)
                st.markdown(hotel_result)
