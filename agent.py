import os
import re
from duckduckgo_search import DDGS
from google import genai

def get_real_photo(query: str) -> str:
    """Takes a query, searches DuckDuckGo Images specifically for photography, and returns a valid image URL."""
    try:
        # Arama terimine "travel photography" ekleyerek tabloları ve çizimleri eliyoruz
        search_query = f"{query} landmark travel high quality photo"
        with DDGS(timeout=10) as ddgs:
            results = ddgs.images(
                keywords=search_query,
                region="wt-wt",
                safesearch="on",
                max_results=1,
            )
            if results and len(results) > 0:
                return results[0].get("image")
    except Exception:
        pass
    # Hata durumunda (veya limit aşımında) varsayılan manzara fotoğrafı
    return "https://images.unsplash.com/photo-1488646953014-c8cb89d03437?w=800&q=80"

def generate_travel_guide(start_city: str, cities: str, start_date, end_date, api_key: str) -> str:
    """
    Generates a travel guide using the Gemini API and injects DuckDuckGo high quality images.
    """
    days = (end_date - start_date).days + 1
    if not api_key:
        return "Hata: Lütfen geçerli bir Gemini API Anahtarı girin."
        
    try:
        # Gemini API istemcisini başlat
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Sen profesyonel bir tur rehberi ve tarihi seyahat planlayıcısısın. 
        Kullanıcı '{start_city}' şehrinden yola çıkarak şu şehir(leri) ziyaret edecek: {cities}
        Tarihler: {start_date} ile {end_date} arası. (Toplam {days} gün)
        
        LÜTFEN AŞAĞIDAKİ KURALLARA KESİNLİKLE UY:
        1. Bu şehir(ler)deki önemli tarihi mekanlar hakkında ilgi çekici bilgiler ver.
        2. ANLATTIĞIN HER TARİHİ MEKAN BAŞLIĞININ ALTINA MUTLAKA BİR FOTOĞRAF (GÖRSEL) EKLEMEK ZORUNDASIN! 
           Sistemimizin gerçek fotoğrafları çekebilmesi için şu FORMATI KESİNLİKLE KULLAN:
           `![Mekan İsmi](WIKI_RESIM:Mekanin_Ingilizce_Adi)`
           Lütfen normal url (http...) YAZMA. Sadece `WIKI_RESIM:Arama_Kelimesi` formatını kullan.
        3. {start_city} çıkışlı {days} günlük mantıklı ve saatli bir gezi rotası (itinerary) hazırla.
        4. Bölgenin ulaşım, hava durumu ve yöresel yemekleri hakkında ipuçları ekle.
        
        Tüm yanıtını şık bir Markdown yapısında oluştur.
        """
        
        # En güncel ve hızlı modellerden biri olan gemini-2.5-flash kullanımı
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        text = response.text
        
        # WIKI_RESIM etiketlerini bulup DuckDuckGo gerçek görselleri ile değiştiriyoruz
        def replace_image(match):
            alt_text = match.group(1)
            query = match.group(2)
            img_url = get_real_photo(query)
            return f"![{alt_text}]({img_url})"

        text = re.sub(r'!\[([^\]]+)\]\(WIKI_RESIM:([^\)]+)\)', replace_image, text)
        
        return text
    except Exception as e:
        return f"Rehber oluşturulurken bir hata oluştu: {str(e)}"

def generate_transport_plan(start_city: str, cities: str, start_date, end_date, api_key: str) -> str:
    """
    Generates flight and train recommendations with estimated prices originating from a specified start_city.
    """
    if not api_key:
        return "Hata: Lütfen geçerli bir Gemini API Anahtarı girin."
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Sen uzman bir seyahat acentesi ve ulaşım planlayıcısısın.
        Kullanıcının Yolculuk Başlangıç Şehri (Nereden): {start_city}
        Kullanıcının Ziyaret Edeceği Lokasyonlar (Nereye): {cities}
        Gidiş Tarihi: {start_date}
        Dönüş Tarihi: {end_date}
        
        Lütfen şunları yap:
        1. İlk seyahat başlangıcı olan '{start_city}' şehrinden başlayarak, tur planındaki '{cities}' lokasyonlarına ulaşımı tarih sırasına göre adım adım planla.
        2. Her adım için tahmini uçak, tren veya otobüs seferi seçeneklerini sun. Gerçekçi, ortalama güncel fiyat tahminleri ver (USD veya EUR cinsinden). Dönüş biletini de {end_date} için tekrar hesapla.
        3. Havalimanından/Gardan şehir merkezine veya ilkotele ulaşım hakkında bilgi ver.
        4. Birden fazla şehir varsa, şehirler arası geçiş için en mantıklı ulaşım yolunu (tren/otobüs/uçak) ve maliyetini belirt.
        
        Yanıtını şık bir Markdown formatında, tablolar veya maddeler kullanarak Türkçe olarak ver.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Ulaşım planı oluşturulurken bir hata oluştu: {str(e)}"

def generate_hotel_plan(start_city: str, cities: str, start_date, end_date, api_key: str) -> str:    
    """
    Generates hotel recommendations contextualized by tour locations.
    """
    if not api_key:
        return "Hata: Lütfen geçerli bir Gemini API Anahtarı girin."
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Sen uzman bir otel rezervasyon danışmanısın.
        Kullanıcının Yolculuğa Başlayacağı Şehir: {start_city}
        Kullanıcının Tur Planında Konaklayacağı Şehirler: {cities}
        Giriş (Gidiş) Tarihi: {start_date}
        Çıkış (Dönüş) Tarihi: {end_date}
        
        Lütfen şunları yap:
        1. Konaklanacak olan {cities} lokasyonları için gidiş tarihlerine ve rotaya en mantıklı uyacak şekilde 3 farklı bütçe kategorisinde otel/konaklama önerileri sun:
           - Lüks (5 Yıldız)
           - Orta Segment (3-4 Yıldız / Butik)
           - Bütçe Dostu (Hostel / Uygun Fiyatlı / Airbnb)
        2. Her bütçe için tavsiye edilen bölgeleri (şehir merkezine ve havalimanına/tren garına ulaşım kolaylığı olan yerleri) açıkla.
        3. Tüm bu {start_date} ile {end_date} arasındaki tatil süresi boyunca toplam tahmini ortalama konaklama fiyatlarını (USD/EUR cinsinden) tablo olarak belirt.
        
        Yanıtını şık bir Markdown formatında, tablolar veya maddeler kullanarak Türkçe olarak ver.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Konaklama planı oluşturulurken bir hata oluştu: {str(e)}"
