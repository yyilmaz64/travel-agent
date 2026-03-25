import os
from google import genai

def generate_travel_guide(cities: str, days: int, api_key: str) -> str:
    """
    Generates a travel guide using the Gemini API.
    """
    if not api_key:
        return "Hata: Lütfen geçerli bir Gemini API Anahtarı girin."
        
    try:
        # Gemini API istemcisini başlat
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Sen profesyonel bir tur rehberi ve tarihi seyahat planlayıcısısın. 
        Kullanıcı şu şehir(leri) ziyaret edecek: {cities}
        Kullanıcının bu seyahat için ayırdığı toplam süre: {days} gün.
        
        Lütfen şunları yap:
        1. Bu şehir(ler)deki en önemli tarihi mekanlar ve kültürel miraslar hakkında kısa, ilgi çekici ve doyurucu bilgiler ver.
        2. {days} günlük, lojistik açıdan mantıklı bir gezi rotası (itinerary) hazırla.
        3. Turistlerin bilmesi gereken ulaşım, hava durumu, yöresel yemekler veya yerel kültür hakkında "Seyahat İpuçları" bölümü ekle.
        
        Yanıtını Markdown formatında, okunaklı başlıklar, alt başlıklar ve maddeler kullanarak Türkçe olarak ver.
        Kullanıcıyı yolculuğa heyecanlandıracak, pozitif ve motive edici bir ton kullan!
        """
        
        # En güncel ve hızlı modellerden biri olan gemini-2.5-flash kullanımı
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Rehber oluşturulurken bir hata oluştu: {str(e)}"
