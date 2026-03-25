import os
import re
import wikipedia
from google import genai

wikipedia.set_lang('en') # Aramaların daha isabetli olması için İngilizce yapıyoruz

def get_wiki_image(query: str) -> str:
    """Takes a query, searches Wikipedia, and returns a valid image URL."""
    try:
        results = wikipedia.search(query)
        if not results:
            return "https://images.unsplash.com/photo-1488646953014-c8cb89d03437?w=800&q=80" # Placeholder manzara
        
        try:
            page = wikipedia.page(results[0], auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            # Çok anlamlılık varsa ilk seçeneği al
            page = wikipedia.page(e.options[0], auto_suggest=False)
            
        for img in page.images:
            img_lower = img.lower()
            # Gerçek bir fotoğraf olduğundan emin olmak için svg ve ikonları filtreliyoruz
            if img_lower.endswith(('.jpg', '.jpeg', '.png')) and not any(x in img_lower for x in ['icon', 'logo', 'map', 'flag', 'symbol', 'coat_of_arms']):
                return img
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1488646953014-c8cb89d03437?w=800&q=80"

def generate_travel_guide(cities: str, days: int, api_key: str) -> str:
    """
    Generates a travel guide using the Gemini API and injects Wikipedia images.
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
           Sistemimizin gerçek fotoğrafları çekebilmesi için şu FORMATI KESİNLİKLE KULLAN:
           `![Mekan İsmi](WIKI_RESIM:Mekanin_Ingilizce_Adi)`
           Örnek kullanım: `![Eyfel Kulesi](WIKI_RESIM:Eiffel Tower)` veya `![Kolezyum](WIKI_RESIM:Colosseum)`
           Lütfen normal url (http...) YAZMA. Sadece `WIKI_RESIM:Arama_Kelimesi` formatını kullan.
        3. {days} günlük, saat saat tasarlanmış mantıklı bir gezi rotası (itinerary) hazırla.
        4. Bölgenin ulaşım, hava durumu ve yöresel yemekleri hakkında ipuçları ekle.
        
        Tüm yanıtını şık bir Markdown yapısında oluştur.
        """
        
        # En güncel ve hızlı modellerden biri olan gemini-2.5-flash kullanımı
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        text = response.text
        
        # WIKI_RESIM etiketlerini bulup gerçek Wikipedia görselleri ile değiştiriyoruz
        def replace_image(match):
            alt_text = match.group(1)
            query = match.group(2)
            img_url = get_wiki_image(query)
            return f"![{alt_text}]({img_url})"

        text = re.sub(r'!\[([^\]]+)\]\(WIKI_RESIM:([^\)]+)\)', replace_image, text)
        
        return text
    except Exception as e:
        return f"Rehber oluşturulurken bir hata oluştu: {str(e)}"
