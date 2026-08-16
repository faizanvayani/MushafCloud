import streamlit as st
import requests
import html
import json

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mushaf Cloud | Quran & Hadith Platform",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Luxury Emerald & Gold CSS Design
CUSTOM_CSS = """
<style>
/* Google Fonts Import */
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Scheherazade+New:wght@400;700&display=swap');

/* Color Variables & Base Reset */
:root {
    --bg-gradient: radial-gradient(circle at 50% 0%, #0d281e 0%, #06150f 75%);
    --card-bg: rgba(14, 38, 28, 0.65);
    --card-border: rgba(212, 175, 55, 0.22);
    --card-border-hover: rgba(244, 208, 104, 0.5);
    --gold-primary: #D4AF37;
    --gold-bright: #F4D068;
    --gold-soft: #F3E5AB;
    --gold-gradient: linear-gradient(135deg, #BF953F 0%, #FCF6BA 25%, #B38728 50%, #FBF5B7 75%, #AA771C 100%);
    --text-primary: #F7F9F7;
    --text-secondary: #C3D5C9;
    --text-muted: #88A292;
    --sidebar-bg: #071912;
}

/* Global Container Styling */
.stApp {
    background: var(--bg-gradient) !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

/* Hide Default Streamlit Headers/Footers for Clean Look */
header[data-testid="stHeader"] {
    background: transparent !important;
}
footer {
    visibility: hidden;
}
#MainMenu {
    visibility: hidden;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--card-border) !important;
}

/* Glassmorphic Brand Banner */
.brand-header {
    background: rgba(212, 175, 55, 0.06);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    margin-bottom: 24px;
    backdrop-filter: blur(10px);
}
.brand-logo {
    font-size: 2.2rem;
    margin-bottom: 4px;
    display: inline-block;
}
.brand-title {
    font-size: 1.4rem;
    font-weight: 700;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.5px;
    margin: 0;
}
.brand-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Surah / Hadith Hero Header Card */
.surah-hero-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
    position: relative;
    overflow: hidden;
}
.surah-hero-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gold-gradient);
}
.surah-arabic-title {
    font-family: 'Amiri', serif;
    font-size: 3.2rem;
    color: var(--gold-bright);
    margin: 0 0 6px 0;
    text-shadow: 0 0 15px rgba(244, 208, 104, 0.25);
}
.surah-english-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.surah-meaning {
    font-size: 1rem;
    color: var(--text-secondary);
    font-style: italic;
    margin-bottom: 18px;
}
.metadata-badges {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}
.meta-badge {
    background: rgba(212, 175, 55, 0.1);
    border: 1px solid rgba(212, 175, 55, 0.25);
    color: var(--gold-soft);
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* Full Surah Audio Player Container */
.full-audio-container {
    background: rgba(212, 175, 55, 0.08);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 16px 20px;
    margin-top: 14px;
    text-align: center;
}
.full-audio-title {
    color: var(--gold-bright);
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

/* Bismillah Banner */
.bismillah-card {
    background: rgba(14, 38, 28, 0.4);
    border: 1px dashed rgba(212, 175, 55, 0.3);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    margin-bottom: 28px;
}
.bismillah-text {
    font-family: 'Amiri', serif;
    font-size: 2.3rem;
    color: var(--gold-bright);
    margin: 0;
    line-height: 1.6;
}

/* Ayah & Hadith Glassmorphic Card */
.ayah-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
.ayah-card:hover {
    border-color: var(--card-border-hover);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}
.ayah-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.1);
    padding-bottom: 10px;
}
.ayah-number-badge {
    background: var(--gold-gradient);
    color: #06150f;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.88rem;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
}
.ayah-arabic-text {
    font-family: 'Amiri', 'Scheherazade New', serif;
    color: #FFFFFF;
    direction: rtl;
    text-align: right;
    line-height: 2.2;
    margin-bottom: 18px;
    text-shadow: 0 0 2px rgba(255, 255, 255, 0.2);
    word-spacing: 2px;
}
.ayah-translation-text {
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--text-secondary);
    border-left: 3px solid var(--gold-primary);
    padding-left: 14px;
    margin-top: 12px;
}

/* Continuous Mushaf Reading Container */
.mushaf-container {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 36px 30px;
    line-height: 2.8;
    direction: rtl;
    text-align: justify;
    backdrop-filter: blur(12px);
    margin-bottom: 28px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}
.mushaf-ayah-inline {
    font-family: 'Amiri', serif;
    color: #FFFFFF;
    display: inline;
}
.mushaf-symbol {
    font-family: 'Amiri', serif;
    color: var(--gold-bright);
    margin: 0 8px;
    font-weight: bold;
    display: inline-block;
}

/* UI Elements Customization */
div[data-baseweb="select"] > div {
    background-color: rgba(14, 38, 28, 0.9) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] * {
    color: var(--text-primary) !important;
}
.stRadio label {
    color: var(--text-primary) !important;
}
.stSlider > div {
    color: var(--gold-bright) !important;
}

/* Custom Styled Audio Player */
.custom-audio-player {
    width: 100%;
    margin-top: 12px;
    border-radius: 30px;
    outline: none;
    filter: sepia(20%) saturate(140%) hue-rotate(90deg) contrast(90%);
}
</style>

<!-- Verse Cards Continuous Auto-Play JavaScript Script -->
<script>
function playNextVerse(currentNum) {
    var nextNum = currentNum + 1;
    var nextAudio = document.getElementById('audio-verse-' + nextNum);
    if (nextAudio) {
        nextAudio.play();
        var nextCard = document.getElementById('ayah-card-' + nextNum);
        if (nextCard) {
            nextCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            nextCard.style.borderColor = 'var(--gold-bright)';
            nextCard.style.boxShadow = '0 0 25px rgba(244, 208, 104, 0.4)';
        }
    }
}
</script>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# API CACHING HELPERS
# -----------------------------------------------------------------------------
BASE_URL = "https://api.alquran.cloud/v1"

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_surah_list():
    try:
        response = requests.get(f"{BASE_URL}/surah")
        if response.status_code == 200:
            return response.json().get("data", [])
    except Exception as e:
        st.error(f"Error connecting to Al-Quran Cloud API: {e}")
    return []

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_multi_edition(surah_number, editions_str):
    try:
        url = f"{BASE_URL}/surah/{surah_number}/editions/{editions_str}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", [])
    except Exception as e:
        st.error(f"Error fetching Quran data: {e}")
    return []

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_editions_by_type(edition_type):
    try:
        res = requests.get(f"{BASE_URL}/edition/type/{edition_type}")
        if res.status_code == 200:
            return res.json().get("data", [])
    except Exception as e:
        pass
    return []

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_editions_by_format(edition_format):
    try:
        res = requests.get(f"{BASE_URL}/edition/format/{edition_format}")
        if res.status_code == 200:
            return res.json().get("data", [])
    except Exception as e:
        pass
    return []

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_editions_by_language(lang):
    try:
        res = requests.get(f"{BASE_URL}/edition/language/{lang}")
        if res.status_code == 200:
            return res.json().get("data", [])
    except Exception as e:
        pass
    return []

# HADITH API CACHING
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_hadith_edition(edition_code):
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{edition_code}.min.json"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        st.error(f"Error loading Hadith edition '{edition_code}': {e}")
    return {}


# -----------------------------------------------------------------------------
# PRESET DICTIONARIES FOR QARIS, TRANSLATIONS & HADITH BOOKS
# -----------------------------------------------------------------------------
QARI_PRESETS = {
    "🎙️ Mishary Rashid Alafasy": "ar.alafasy",
    "🎙️ Abdul Basit (Murattal)": "ar.abdulbasitmurattal",
    "🎙️ Abdur-Rahman As-Sudais": "ar.abdurrahmaansudais",
    "🎙️ Ali Al-Hudhaify": "ar.hudhaify",
    "🎙️ Mohamed Siddiq El-Minshawi": "ar.minshawi",
    "🎙️ Maher Al-Muaiqly": "ar.mahermuaiqly",
    "🎙️ Abu Bakr Al-Shatri": "ar.shaatree",
    "🎙️ Sa'ad Al-Ghamadi": "ar.ghamadi",
    "🎙️ Hani Ar-Rifai": "ar.hanrifai",
    "🚫 No Recitation Audio": "none"
}

FULL_SURAH_SERVERS = {
    "ar.alafasy": "https://server8.mp3quran.net/afs/",
    "ar.abdulbasitmurattal": "https://server7.mp3quran.net/basit/",
    "ar.abdurrahmaansudais": "https://server11.mp3quran.net/sds/",
    "ar.hudhaify": "https://server9.mp3quran.net/hthfi/",
    "ar.minshawi": "https://server10.mp3quran.net/minsh/",
    "ar.mahermuaiqly": "https://server12.mp3quran.net/maher/",
    "ar.shaatree": "https://server11.mp3quran.net/shatri/",
    "ar.ghamadi": "https://server7.mp3quran.net/s_gmd/",
    "ar.hanrifai": "https://server8.mp3quran.net/hani/"
}

TRANSLATION_PRESETS = {
    "🇬🇧 English - Saheeh International": "en.sahih",
    "🇬🇧 English - Yusuf Ali": "en.yusufali",
    "🇵🇰 Urdu - Fateh Muhammad Jalandhry": "ur.jalandhry",
    "🇵🇰 Urdu - Abul A'ala Maududi": "ur.maududi",
    "🇵🇰 Urdu - Muhammad Junagarhi": "ur.junagarhi",
    "🇮🇳 Hindi - Suhel Farooq Khan": "hi.hindi",
    "🇫🇷 French - Muhammad Hamidullah": "fr.hamidullah",
    "🇹🇷 Turkish - Diyanet Isleri": "tr.diyanet",
    "🇮🇩 Indonesian - Bahasa Indonesia": "id.indonesian",
    "🇪🇸 Spanish - Julio Cortes": "es.cortes",
    "🚫 None (Arabic Only)": "none"
}

# Hadith Collections Dictionary
HADITH_COLLECTIONS = {
    "📖 Sahih al-Bukhari (صحيح البخاري)": "bukhari",
    "📖 Sahih Muslim (صحيح مسلم)": "muslim",
    "📖 Sunan Abu Dawud (سنن أبي داود)": "abudawud",
    "📖 Jami` at-Tirmidhi (جامع الترمذي)": "tirmidhi",
    "📖 Sunan an-Nasa'i (سنن النسائي)": "nasai",
    "📖 Sunan Ibn Majah (سنن ابن ماجه)": "ibnmajah",
    "📖 Muwatta Malik (موطأ مالك)": "malik",
    "📖 40 Hadith Nawawi (الأربعون النووية)": "nawawi"
}

# Hadith Languages Dictionary
HADITH_LANGUAGES = {
    "🇵🇰 Urdu (اردو)": "urd",
    "🇬🇧 English": "eng",
    "🇸🇦 Arabic Only (العربية)": "ara",
    "🇧🇩 Bengali (বাংলা)": "ben",
    "🇮🇩 Indonesian (Bahasa Indonesia)": "ind",
    "🇫🇷 French (Français)": "fra",
    "🇷🇺 Russian (Русский)": "rus",
    "🇹🇷 Turkish (Türkçe)": "tur",
    "🇮🇳 Tamil (தமிழ்)": "tam"
}


# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""<div class="brand-header">
<div class="brand-logo">📖</div>
<h1 class="brand-title">MUSHAF CLOUD</h1>
<div class="brand-subtitle">Quran & Hadith Platform</div>
</div>""", unsafe_allow_html=True)

    app_mode = st.radio(
        "Navigation",
        ["📖 Surah Reader", "📜 Hadith Explorer", "🌐 Advanced Explorer", "ℹ️ About App"],
        index=0
    )
    
    st.markdown("---")

    if app_mode == "📖 Surah Reader":
        st.subheader("⚙️ Reading Controls")
        
        # Load Surahs
        surahs = fetch_surah_list()
        surah_options = [f"{s['number']}. {s['englishName']} ({s['name']})" for s in surahs]
        
        selected_surah_idx = st.selectbox(
            "Select Surah",
            range(len(surah_options)),
            format_func=lambda i: surah_options[i] if surah_options else "Loading..."
        )
        
        selected_surah_num = selected_surah_idx + 1 if surahs else 1
        
        # Select Qari Audio
        selected_qari_label = st.selectbox("Reciter (Qari)", list(QARI_PRESETS.keys()), index=0)
        selected_qari_id = QARI_PRESETS[selected_qari_label]
        
        # Select Translation
        selected_trans_label = st.selectbox("Translation", list(TRANSLATION_PRESETS.keys()), index=0)
        selected_trans_id = TRANSLATION_PRESETS[selected_trans_label]
        
        # Typography Slider
        arabic_font_size = st.slider("Arabic Font Size (px)", min_value=24, max_value=56, value=34, step=2)
        
        # View Mode
        view_mode = st.radio("Display Mode", ["Verse Cards", "Continuous Mushaf Text"], index=0)

    elif app_mode == "📜 Hadith Explorer":
        st.subheader("⚙️ Hadith Controls")
        
        selected_book_label = st.selectbox("Hadith Collection", list(HADITH_COLLECTIONS.keys()), index=0)
        selected_book_code = HADITH_COLLECTIONS[selected_book_label]
        
        selected_lang_label = st.selectbox("Translation Language", list(HADITH_LANGUAGES.keys()), index=0)
        selected_lang_code = HADITH_LANGUAGES[selected_lang_label]
        
        hadith_font_size = st.slider("Arabic Font Size (px)", min_value=22, max_value=48, value=30, step=2)


# -----------------------------------------------------------------------------
# MAIN CONTENT AREA
# -----------------------------------------------------------------------------
if app_mode == "📖 Surah Reader":
    surahs = fetch_surah_list()
    
    if not surahs:
        st.warning("Fetching Quran data from server... Please check your internet connection if loading persists.")
        st.stop()
        
    current_surah_info = surahs[selected_surah_num - 1]

    # Build multi-editions request string
    editions_to_fetch = ["quran-uthmani"]
    if selected_trans_id != "none":
        editions_to_fetch.append(selected_trans_id)
    if selected_qari_id != "none":
        editions_to_fetch.append(selected_qari_id)
        
    editions_str = ",".join(editions_to_fetch)
    
    with st.spinner("Loading Surah verses..."):
        multi_data = fetch_multi_edition(selected_surah_num, editions_str)

    # Extract datasets accurately by format & type
    quran_data = None
    trans_data = None
    audio_data = None

    if multi_data:
        for ed in multi_data:
            ed_info = ed.get("edition", {})
            format_type = ed_info.get("format", "")
            ed_type = ed_info.get("type", "")
            identifier = ed_info.get("identifier", "")

            if format_type == "text" and ed_type == "quran":
                quran_data = ed
            elif ed_type == "translation" or identifier == selected_trans_id:
                trans_data = ed
            elif format_type == "audio" or identifier == selected_qari_id:
                audio_data = ed

    # -------------------------------------------------------------------------
    # SURAH HERO BANNER & FULL SURAH RECITATION AUDIO PLAYER
    # -------------------------------------------------------------------------
    arabic_name = current_surah_info.get("name", "")
    english_name = current_surah_info.get("englishName", "")
    english_meaning = current_surah_info.get("englishNameTranslation", "")
    revelation = current_surah_info.get("revelationType", "").upper()
    total_ayahs = current_surah_info.get("numberOfAyahs", 0)
    rev_icon = "🕋" if revelation == "MECCAN" else "🕌"

    # Single Full Surah Audio Stream URL
    full_surah_audio_url = ""
    if selected_qari_id in FULL_SURAH_SERVERS:
        surah_3digit = f"{selected_surah_num:03d}"
        full_surah_audio_url = f"{FULL_SURAH_SERVERS[selected_qari_id]}{surah_3digit}.mp3"

    full_audio_html = ""
    if full_surah_audio_url:
        full_audio_html = f"""<div class="full-audio-container">
<div class="full-audio-title">▶️ Play Full Complete Surah Continuously ({selected_qari_label})</div>
<audio src="{full_surah_audio_url}" controls class="custom-audio-player" preload="metadata"></audio>
</div>"""

    hero_html = f"""<div class="surah-hero-card">
<h1 class="surah-arabic-title">{arabic_name}</h1>
<div class="surah-english-title">{english_name}</div>
<div class="surah-meaning">"{english_meaning}"</div>
<div class="metadata-badges">
<span class="meta-badge">📖 Surah No. {selected_surah_num}</span>
<span class="meta-badge">{rev_icon} {revelation}</span>
<span class="meta-badge">✨ {total_ayahs} Verses</span>
</div>
{full_audio_html}
</div>"""

    st.markdown(hero_html, unsafe_allow_html=True)

    # Bismillah Banner (Show for all except Surah 9 At-Tawbah)
    if selected_surah_num != 9:
        st.markdown("""<div class="bismillah-card">
<div class="bismillah-text">بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</div>
</div>""", unsafe_allow_html=True)

    if quran_data and "ayahs" in quran_data:
        ayahs = quran_data["ayahs"]
        trans_ayahs = trans_data.get("ayahs", []) if trans_data else []
        audio_ayahs = audio_data.get("ayahs", []) if audio_data else []

        # Continuous Mushaf Mode
        if view_mode == "Continuous Mushaf Text":
            mushaf_html_parts = ['<div class="mushaf-container">']
            for i, ayah in enumerate(ayahs):
                ayah_text = ayah.get("text", "")
                
                # Strip Bismillah prefix for Surah 1 & general verses if repeated
                if selected_surah_num != 1 and i == 0 and ayah_text.startswith("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"):
                    ayah_text = ayah_text.replace("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", "").strip()

                num_in_surah = ayah.get("numberInSurah", i + 1)
                mushaf_html_parts.append(
                    f'<span class="mushaf-ayah-inline" style="font-size:{arabic_font_size}px;">{html.escape(ayah_text)}</span>'
                    f'<span class="mushaf-symbol" style="font-size:{int(arabic_font_size * 0.75)}px;"> ۝{num_in_surah} </span>'
                )
            mushaf_html_parts.append('</div>')
            st.markdown("".join(mushaf_html_parts), unsafe_allow_html=True)

            # Also show translations below if selected
            if trans_ayahs:
                st.markdown("<h3 style='color:var(--gold-soft); margin-top:24px;'>Translations</h3>", unsafe_allow_html=True)
                for i, tayah in enumerate(trans_ayahs):
                    num = tayah.get("numberInSurah", i + 1)
                    ttext = tayah.get("text", "")
                    st.markdown(f"**[{num}]** {ttext}")

        # Verse Cards Mode
        else:
            for i, ayah in enumerate(ayahs):
                num_in_surah = ayah.get("numberInSurah", i + 1)
                arabic_text = ayah.get("text", "")

                # Remove Bismillah from first verse if not Surah Fatiha
                if selected_surah_num != 1 and i == 0 and arabic_text.startswith("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"):
                    arabic_text = arabic_text.replace("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", "").strip()

                # Translation text for this verse
                t_text = ""
                if i < len(trans_ayahs):
                    t_text = trans_ayahs[i].get("text", "")

                # Audio URL for this verse
                a_url = ""
                if i < len(audio_ayahs):
                    a_url = audio_ayahs[i].get("audio", "")

                audio_tag_html = f'<audio id="audio-verse-{num_in_surah}" src="{a_url}" controls class="custom-audio-player" onended="playNextVerse({num_in_surah})"></audio>' if a_url else ''
                translation_tag_html = f'<div class="ayah-translation-text">{html.escape(t_text)}</div>' if t_text else ''

                card_html = f"""<div class="ayah-card" id="ayah-card-{num_in_surah}">
<div class="ayah-header-row">
<div class="ayah-number-badge">{num_in_surah}</div>
<div style="color:var(--text-muted); font-size:0.85rem; font-weight:600;">AYAH {num_in_surah}</div>
</div>
<div class="ayah-arabic-text" style="font-size: {arabic_font_size}px;">{html.escape(arabic_text)}</div>
{translation_tag_html}
{audio_tag_html}
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)

elif app_mode == "📜 Hadith Explorer":
    st.markdown(f"""<div class="surah-hero-card">
<h1 class="surah-arabic-title">الْأَحَادِيثُ النَّبَوِيَّةُ</h1>
<div class="surah-english-title">{selected_book_label}</div>
<div class="surah-meaning">Language: {selected_lang_label}</div>
</div>""", unsafe_allow_html=True)

    with st.spinner(f"Loading {selected_book_label}..."):
        # Fetch Arabic Hadith Edition
        ara_edition_code = f"ara-{selected_book_code}"
        ara_data = fetch_hadith_edition(ara_edition_code)
        ara_hadiths = ara_data.get("hadiths", [])

        # Fetch Translated Hadith Edition
        tr_hadiths = []
        if selected_lang_code != "ara":
            tr_edition_code = f"{selected_lang_code}-{selected_book_code}"
            tr_data = fetch_hadith_edition(tr_edition_code)
            tr_hadiths = tr_data.get("hadiths", [])

    total_hadith_count = max(len(ara_hadiths), len(tr_hadiths))

    if total_hadith_count == 0:
        st.warning(f"No Hadith records found for {selected_book_label} in {selected_lang_label}. Please select another language or collection.")
        st.stop()

    # Search & Filter Bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search Hadiths by Keyword", "")
    with col2:
        items_per_page = st.selectbox("Per Page", [10, 20, 50, 100], index=1)
    with col3:
        jump_hadith_num = st.number_input("Jump to Hadith #", min_value=1, max_value=total_hadith_count, value=1)

    # Filter Hadiths by Search Query or Jump Number
    filtered_indices = []
    if search_query.strip():
        q_clean = search_query.strip().lower()
        for idx in range(total_hadith_count):
            a_text = ara_hadiths[idx].get("text", "") if idx < len(ara_hadiths) else ""
            t_text = tr_hadiths[idx].get("text", "") if idx < len(tr_hadiths) else ""
            if q_clean in a_text.lower() or q_clean in t_text.lower():
                filtered_indices.append(idx)
    else:
        filtered_indices = list(range(total_hadith_count))

    st.markdown(f"<div style='color:var(--gold-soft); margin-bottom:16px; font-weight:600;'>Showing {len(filtered_indices)} of {total_hadith_count} Hadiths</div>", unsafe_allow_html=True)

    # Pagination
    total_pages = max(1, (len(filtered_indices) + items_per_page - 1) // items_per_page)
    
    # Calculate initial page if jump number specified
    default_page = 1
    if jump_hadith_num > 1 and not search_query:
        default_page = min(total_pages, max(1, (jump_hadith_num - 1) // items_per_page + 1))

    current_page = st.number_input("Page", min_value=1, max_value=total_pages, value=default_page)

    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_indices))

    # Render Hadith Cards
    for i in range(start_idx, end_idx):
        h_idx = filtered_indices[i]
        
        ara_item = ara_hadiths[h_idx] if h_idx < len(ara_hadiths) else {}
        tr_item = tr_hadiths[h_idx] if h_idx < len(tr_hadiths) else {}

        hadith_num = ara_item.get("hadithnumber") or tr_item.get("hadithnumber") or (h_idx + 1)
        arabic_text = ara_item.get("text", "")
        trans_text = tr_item.get("text", "")

        # Hadith Grade/Status (if available)
        grades = ara_item.get("grades", []) or tr_item.get("grades", [])
        grade_html = ""
        if grades:
            g_name = grades[0].get("grade", "")
            if g_name:
                grade_html = f'<span style="background:rgba(212,175,55,0.15); border:1px solid var(--card-border); color:var(--gold-soft); padding:3px 10px; border-radius:20px; font-size:0.75rem; margin-left:8px;">✨ {html.escape(g_name)}</span>'

        trans_tag_html = f'<div class="ayah-translation-text">{html.escape(trans_text)}</div>' if trans_text and selected_lang_code != "ara" else ''

        hadith_card_html = f"""<div class="ayah-card">
<div class="ayah-header-row">
<div class="ayah-number-badge">HADITH #{hadith_num}</div>
<div>{grade_html}</div>
</div>
<div class="ayah-arabic-text" style="font-size: {hadith_font_size}px;">{html.escape(arabic_text)}</div>
{trans_tag_html}
</div>"""
        st.markdown(hadith_card_html, unsafe_allow_html=True)

elif app_mode == "🌐 Advanced Explorer":
    st.markdown("""<div style="text-align:center; padding: 20px; margin-bottom: 20px;">
<h1 style="color:var(--gold-bright);">🌐 Advanced Quran Edition Explorer</h1>
<p style="color:var(--text-secondary);">Filter and explore all available translations, tafsirs, audio recitations, and formats across languages.</p>
</div>""", unsafe_allow_html=True)

    filter_by = st.selectbox("Explore Editions By:", ["Type", "Format", "Language"])

    if filter_by == "Type":
        st.subheader("Filter by Edition Type")
        ed_types = ["quran", "translation", "tafsir", "transliteration", "versebyverse"]
        selected_type = st.selectbox("Select Type", ed_types)
        
        with st.spinner("Fetching editions..."):
            items = fetch_editions_by_type(selected_type)
            
        if items:
            st.success(f"Found {len(items)} editions for type: {selected_type}")
            for item in items:
                st.markdown(f"""<div class="ayah-card">
<h4 style="color:var(--gold-soft); margin:0 0 6px 0;">{item.get('name')} ({item.get('englishName')})</h4>
<div style="color:var(--text-secondary); font-size:0.9rem;">
<b>Identifier:</b> <code>{item.get('identifier')}</code> | 
<b>Language:</b> {item.get('language')} | 
<b>Format:</b> {item.get('format')}
</div>
</div>""", unsafe_allow_html=True)

    elif filter_by == "Format":
        st.subheader("Filter by Edition Format")
        selected_format = st.selectbox("Select Format", ["text", "audio"])
        
        with st.spinner("Fetching editions..."):
            items = fetch_editions_by_format(selected_format)
            
        if items:
            st.success(f"Found {len(items)} editions for format: {selected_format}")
            for item in items:
                st.markdown(f"""<div class="ayah-card">
<h4 style="color:var(--gold-soft); margin:0 0 6px 0;">{item.get('name')} ({item.get('englishName')})</h4>
<div style="color:var(--text-secondary); font-size:0.9rem;">
<b>Identifier:</b> <code>{item.get('identifier')}</code> | 
<b>Language:</b> {item.get('language')} | 
<b>Type:</b> {item.get('type')}
</div>
</div>""", unsafe_allow_html=True)

    elif filter_by == "Language":
        st.subheader("Filter by Language")
        languages = ["en", "ur", "ar", "fr", "es", "tr", "id", "hi", "bn", "zh", "ru", "de"]
        selected_lang = st.selectbox("Select Language Code", languages)
        
        with st.spinner("Fetching editions..."):
            items = fetch_editions_by_language(selected_lang)
            
        if items:
            st.success(f"Found {len(items)} editions for language: {selected_lang}")
            for item in items:
                st.markdown(f"""<div class="ayah-card">
<h4 style="color:var(--gold-soft); margin:0 0 6px 0;">{item.get('name')} ({item.get('englishName')})</h4>
<div style="color:var(--text-secondary); font-size:0.9rem;">
<b>Identifier:</b> <code>{item.get('identifier')}</code> | 
<b>Format:</b> {item.get('format')} | 
<b>Type:</b> {item.get('type')}
</div>
</div>""", unsafe_allow_html=True)

elif app_mode == "ℹ️ About App":
    st.markdown("""<div class="surah-hero-card" style="text-align:left;">
<h2 style="color:var(--gold-bright); text-align:center;">About Mushaf Cloud Platform</h2>
<p style="color:var(--text-primary); font-size:1.05rem; line-height:1.8;">
<b>Mushaf Cloud</b> is a state-of-the-art digital Quran & Hadith web application 
designed with a modern, high-performance, and luxury Islamic visual design system.
</p>
<h3 style="color:var(--gold-soft); margin-top:20px;">Features Key Highlights:</h3>
<ul style="color:var(--text-secondary); line-height:1.8;">
<li><b>Authentic Quranic & Hadith Typography:</b> High-definition rendering powered by Amiri & Scheherazade fonts.</li>
<li><b>Complete Hadith Collections:</b> Access Sahih al-Bukhari, Sahih Muslim, Sunan Abu Dawud, Jami` at-Tirmidhi, Sunan an-Nasa'i, Sunan Ibn Majah, Muwatta Malik, 40 Hadith Nawawi.</li>
<li><b>Multi-Language Hadith Translations:</b> Urdu, English, Arabic, Bengali, Indonesian, French, Russian, Turkish, Tamil.</li>
<li><b>Multi-Qari Audio Recitations:</b> High-quality audio from world-renowned Qaris (Mishary Alafasy, Sudais, Abdul Basit, Hudhaify, Minshawi, etc.).</li>
<li><b>Full Surah Single-Stream Audio:</b> Plays complete 100% full Surah audio continuously from start to finish for all Qaris.</li>
<li><b>Parallel Translations:</b> Synchronized Ayah-by-Ayah translations in English, Urdu, Hindi, French, Turkish, and more.</li>
<li><b>Customizable Font Slider:</b> Adjustable Arabic text scaling for maximum reading comfort.</li>
</ul>
</div>""", unsafe_allow_html=True)