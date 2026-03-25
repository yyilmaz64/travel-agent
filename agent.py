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
        
        LÜTFEN AŞAĞIDAKİ KURALLARA KESİNLİKLE UY:
        1. Bu şehir(ler)deki önemli tarihi mekanlar hakkında ilgi çekici bilgiler ver.
        2. ANLATTIĞIN HER TARİHİ MEKAN BAŞLIĞININ ALTINA MUTLAKA BİR FOTOĞRAF (GÖRSEL) EKLEMEK ZORUNDASIN! 
           Bunu yapmak için şu tam formatı kullan:
           `![Mekan İsmi](https://loremflickr.com/800/400/mekanın-ingilizce-adi,landmark)`
           Örnek kullanım: `![Eyfel Kulesi](https://loremflickr.com/800/400/eiffel,tower,landmark)`
           Lütfen bu adımı kesinlikle atlama, rehberin her yeri görsellerle dolu olsun!
        3. {days} günlük, saat saat tasarlanmış mantıklı bir gezi rotası (itinerary) hazırla.
        4. Bölgenin ulaşım, hava durumu ve yöresel yemekleri hakkında ipuçları ekle.
        
        Tüm yanıtını şık bir Markdown yapısında oluştur.
        """
        
        # En güncel ve hızlı modellerden biri olan gemini-2.5-flash kullanımı
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Rehber oluşturulurken bir hata oluştu: {str(e)}"
