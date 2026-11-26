/**
 * AI Scheme Sahayak - Multilingual Translation Engine (i18n)
 * Supports English, Hindi, Hinglish, Bengali, Marathi, Tamil, Telugu, Gujarati, Kannada, Malayalam.
 */

const translations = {
  en: {
    nav_home: "Home",
    nav_schemes: "Schemes",
    nav_how_it_works: "How It Works",
    nav_about: "About",
    nav_ai_assistant: "🤖 AI Assistant",
    btn_login: "Login",
    btn_register: "Register",
    hero_title: "The Right Government Scheme for Your Entrepreneurial Journey.",
    hero_desc: "Overcome language, literacy, and paperwork barriers. Our transparent AI analyzes your business, caste category, location, and investment stage to recommend 100% eligible central & state schemes with zero guesswork.",
    cta_find_schemes: "🎯 Find My Schemes with AI",
    cta_explore: "🔍 Browse All Schemes",
    how_it_works_title: "How AI Scheme Sahayak Works"
  },
  hi: {
    nav_home: "मुख्य पृष्ठ",
    nav_schemes: "योजनाएं",
    nav_how_it_works: "यह कैसे काम करता है",
    nav_about: "हमारे बारे में",
    nav_ai_assistant: "🤖 एआई सहायक",
    btn_login: "लॉग इन",
    btn_register: "पंजीकरण",
    hero_title: "आपकी उद्यमिता यात्रा के लिए सही सरकारी योजना।",
    hero_desc: "भाषा, साक्षरता और कागजी कार्रवाई की बाधाओं को दूर करें। हमारा पारदर्शी AI आपके व्यवसाय, श्रेणी, स्थान और निवेश के आधार पर 100% पात्र योजनाओं की सिफारिश करता है।",
    cta_find_schemes: "🎯 AI से योजना खोजें",
    cta_explore: "🔍 सभी योजनाएं देखें",
    how_it_works_title: "AI Scheme Sahayak कैसे काम करता है"
  },
  hinglish: {
    nav_home: "Home",
    nav_schemes: "Schemes",
    nav_how_it_works: "Kaise Kaam Karta Hai",
    nav_about: "About Us",
    nav_ai_assistant: "🤖 AI Assistant",
    btn_login: "Login Karein",
    btn_register: "Register Karein",
    hero_title: "Aapke Business ke liye Sahi Sarkari Scheme.",
    hero_desc: "Paperwork aur language barriers ko bhool jaiye. Humara AI system aapke business aur category ke hisaab se 100% eligible schemes dhoondhta hai.",
    cta_find_schemes: "🎯 AI se Scheme Dhoondhein",
    cta_explore: "🔍 Saari Schemes Dekhein",
    how_it_works_title: "Yeh System Kaise Kaam Karta Hai"
  },
  bn: {
    nav_home: "হোম",
    nav_schemes: "প্রকল্পসমূহ",
    nav_how_it_works: "কীভাবে কাজ করে",
    nav_about: "আমাদের সম্পর্কে",
    nav_ai_assistant: "🤖 এআই সহায়ক",
    btn_login: "লগইন",
    btn_register: "নিবন্ধন",
    hero_title: "আপনার উদ্যোগী যাত্রার জন্য সঠিক সরকারি প্রকল্প।",
    hero_desc: "আমাদের স্বচ্ছ এআই আপনার ব্যবসা এবং যোগ্যতার ভিত্তিতে সঠিক সরকারি স্কিম সুপারিশ করে।",
    cta_find_schemes: "🎯 স্কিম খুঁজুন",
    cta_explore: "🔍 সব স্কিম দেখুন",
    how_it_works_title: "কীভাবে কাজ করে"
  },
  mr: {
    nav_home: "मुख्यपृष्ठ",
    nav_schemes: "योजना",
    nav_how_it_works: "कसे कार्य करते",
    nav_about: "माहिती",
    nav_ai_assistant: "🤖 एआय सहाय्यक",
    btn_login: "लॉगिन",
    btn_register: "नोंदणी",
    hero_title: "तुमच्या उद्योजक प्रवासासाठी योग्य सरकारी योजना.",
    hero_desc: "आमची पारदर्शक AI प्रणाली तुमच्या व्यवसायानुसार योग्य सरकारी योजनांची शिफारस करते.",
    cta_find_schemes: "🎯 योजना शोधा",
    cta_explore: "🔍 सर्व योजना पहा",
    how_it_works_title: "कसे कार्य करते"
  },
  ta: {
    nav_home: "முகப்பு",
    nav_schemes: "திட்டங்கள்",
    nav_how_it_works: "எவ்வாறு செயல்படுகிறது",
    nav_about: "பற்றி",
    nav_ai_assistant: "🤖 AI உதவியாளர்",
    btn_login: "உள்நுழைய",
    btn_register: "பதிவு செய்க",
    hero_title: "உங்கள் தொழில் முனைவோர் பயணத்திற்கான சரியான அரசுத் திட்டம்.",
    hero_desc: "மொழி மற்றும் ஆவண தடைகளை உடைத்து, உங்கள் தொழிலுக்கு ஏற்ற அரசுத் திட்டங்களை கண்டறியுங்கள்.",
    cta_find_schemes: "🎯 திட்டங்களை கண்டறிக",
    cta_explore: "🔍 திட்டங்களை பார்க்க",
    how_it_works_title: "எவ்வாறு செயல்படுகிறது"
  },
  te: {
    nav_home: "హోమ్",
    nav_schemes: "పథకాలు",
    nav_how_it_works: "ఇది ఎలా పనిచేస్తుంది",
    nav_about: "గురించి",
    nav_ai_assistant: "🤖 AI సహాయకుడు",
    btn_login: "లాగిన్",
    btn_register: "నమోదు",
    hero_title: "మీ వ్యాపార ప్రయాణానికి సరైన ప్రభుత్వ పథకం.",
    hero_desc: "మీ వ్యాపారం మరియు వర్గానికి సరిపోయే ప్రభుత్వ పథకాలను పారదర్శక AI ద్వారా కనుగొనండి.",
    cta_find_schemes: "🎯 పథకాలను శోధించండి",
    cta_explore: "🔍 అన్ని పథకాలు",
    how_it_works_title: "ఇది ఎలా పనిచేస్తుంది"
  },
  gu: {
    nav_home: "મુખ્ય પૃષ્ઠ",
    nav_schemes: "યોજનાઓ",
    nav_how_it_works: "કેવી રીતે કાર્ય કરે છે",
    nav_about: "વિશે",
    nav_ai_assistant: "🤖 એઆઈ સહાયક",
    btn_login: "લૉગિન",
    btn_register: "નોંધણી",
    hero_title: "તમારી વ્યવસાય યાત્રા માટે યોગ્ય સરકારી યોજના.",
    hero_desc: "તમારા વ્યવસાય માટે યોગ્ય સરકારી યોજનાઓ સરળતાથી શોધો.",
    cta_find_schemes: "🎯 યોજના શોધો",
    cta_explore: "🔍 બધી યોજનાઓ જુઓ",
    how_it_works_title: "કેવી રીતે કાર્ય કરે છે"
  },
  kn: {
    nav_home: "ಮುಖಪುಟ",
    nav_schemes: "ಯೋಜನೆಗಳು",
    nav_how_it_works: "ಇದು ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ",
    nav_about: "ಕುರಿತು",
    nav_ai_assistant: "🤖 ಎಐ ಸಹಾಯಕ",
    btn_login: "ಲಾಗಿನ್",
    btn_register: "ನೋಂದಣಿ",
    hero_title: "ನಿಮ್ಮ ಉದ್ಯಮಶೀಲತೆಯ ಪಯಣಕ್ಕೆ ಸೂಕ್ತ ಸರ್ಕಾರಿ ಯೋಜನೆ.",
    hero_desc: "ನಿಮ್ಮ ವ್ಯಾಪಾರಕ್ಕೆ ಸೂಕ್ತವಾದ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ.",
    cta_find_schemes: "🎯 ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
    cta_explore: "🔍 ಎಲ್ಲಾ ಯೋಜನೆಗಳು",
    how_it_works_title: "ಇದು ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ"
  },
  ml: {
    nav_home: "ഹോം",
    nav_schemes: "പദ്ധതികൾ",
    nav_how_it_works: "പ്രവർത്തനം",
    nav_about: "ഞങ്ങളെ കുറിച്ച്",
    nav_ai_assistant: "🤖 എഐ സഹായി",
    btn_login: "ലോഗിൻ",
    btn_register: "രജിസ്റ്റർ ചെയ്യുക",
    hero_title: "നിങ്ങളുടെ സംരംഭക യാത്രയ്ക്ക് അനുയോജ്യമായ സർക്കാർ പദ്ധതി.",
    hero_desc: "നിങ്ങളുടെ ബിസിനസിന് ഏറ്റവും അനുയോജ്യമായ സർക്കാർ സഹായങ്ങൾ കണ്ടെത്തുക.",
    cta_find_schemes: "🎯 പദ്ധതികൾ കണ്ടെത്തുക",
    cta_explore: "🔍 എല്ലാ പദ്ധതികളും",
    how_it_works_title: "പ്രവർത്തനം"
  }
};

class I18nManager {
  constructor() {
    this.currentLang = localStorage.getItem('sahayak_lang') || 'en';
    this.init();
  }

  init() {
    this.applyTranslations(this.currentLang);
    const select = document.getElementById('lang-select') || document.getElementById('chat-lang-select');
    if (select) {
      select.value = this.currentLang;
      select.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
      });
    }
  }

  setLanguage(lang) {
    if (translations[lang]) {
      this.currentLang = lang;
      localStorage.setItem('sahayak_lang', lang);
      this.applyTranslations(lang);
    }
  }

  t(key) {
    const dict = translations[this.currentLang] || translations.en;
    return dict[key] || translations.en[key] || key;
  }

  applyTranslations(lang) {
    const dict = translations[lang] || translations.en;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });
  }
}

// Global instance
window.i18n = new I18nManager();
