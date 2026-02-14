"""
Advanced LLM-powered conversational chatbot for EpiControl AI
Uses Groq API (LLaMA) for intelligent responses about SEIR modeling, visualizations, and simulation features
"""

import os
import re
from typing import List, Tuple

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Comprehensive knowledge base for the chatbot
KNOWLEDGE_BASE = {
    "en": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression", "epidemic", "susceptible", "exposed", "infected", "recovered"],
            "answer": "📈 **SEIR Curve Explanation**\n\nThe SEIR curve shows the epidemic progression over time:\n\n• **S (Susceptible)**: People who can catch the disease\n• **E (Exposed)**: People infected but not yet infectious\n• **I (Infected)**: Currently infectious individuals\n• **R (Recovered)**: People with immunity\n\nThe curve helps you:\n✓ See when infections peak\n✓ Understand disease spread dynamics\n✓ Evaluate intervention effectiveness\n✓ Compare different strategies\n\nWatch how the curves flatten with better interventions!"
        },
        "heatmap": {
            "keywords": ["heatmap", "heat map", "infection", "hotspot", "geographic", "density", "location", "spatial"],
            "answer": "🗺️ **Infection Heatmap Guide**\n\nThe heatmap shows geographic infection density:\n\n• **Red zones**: High infection areas (hotspots)\n• **Yellow zones**: Moderate infection\n• **Blue zones**: Low/no infection\n\nWhat it reveals:\n✓ Where disease spreads fastest\n✓ Geographic clustering of cases\n✓ Effectiveness of local interventions\n✓ Population vulnerable areas\n\nUse this to identify regions needing targeted interventions!"
        },
        "scatter": {
            "keywords": ["scatter", "distribution", "agent", "position", "spatial distribution", "seir state"],
            "answer": "📍 **Spatial Distribution Scatter Plot**\n\nShows individual agent positions by disease state:\n\n• **Dots represent agents** in the population\n• **Color codes indicate SEIR status**:\n  - 🟢 Green: Susceptible\n  - 🟡 Yellow: Exposed\n  - 🔴 Red: Infected\n  - 🔵 Blue: Recovered\n\nThis visualization helps:\n✓ See how disease spreads geographically\n✓ Identify clustering patterns\n✓ Understand contact transmission\n✓ Visualize intervention impact\n\nWatch the color transitions as simulation progresses!"
        },
        "timeline": {
            "keywords": ["timeline", "mutation", "events", "evolution", "virus", "variant", "change"],
            "answer": "🧬 **Mutation Timeline**\n\nTracks virus evolution events during simulation:\n\n**What mutations show:**\n• When variants emerge (Day X)\n• How R₀ changes (infectivity)\n• Mortality rate shifts\n• Transmission rate modifications\n\n**Reading the timeline:**\n📌 Each marker = one mutation event\n📌 Bar length = magnitude of change\n📌 Color = type of change\n\n**Understanding mutations:**\n✓ More transmissible variants emerge\n✓ Mortality may increase or decrease\n✓ Interventions become less effective\n✓ New strategies needed for new variants\n\nRealistic epidemic dynamics!"
        },
        "manual_mode": {
            "keywords": ["manual", "mode", "control", "intervention", "mask", "school", "vaccination"],
            "answer": "🎮 **Manual Control Mode**\n\nYou decide when and how to intervene:\n\n**Available interventions:**\n• 😷 Mask Mandate: 30-50% transmission reduction\n• 🏫 School Closure: Reduces student contact\n• 💉 Vaccination Drive: Provides population immunity\n\n**How it works:**\n1. Select which interventions to apply\n2. Run the simulation\n3. Watch results in real-time\n4. See metrics: deaths, peak infections, etc.\n\n**Best for:**\n✓ Understanding intervention effectiveness\n✓ Testing different strategies\n✓ Learning cause-and-effect relationships\n✓ Policy decision making\n\nExperiment and learn!"
        },
        "ai_mode": {
            "keywords": ["ai", "mode", "artificial intelligence", "q-learning", "agent", "optimal", "automatic"],
            "answer": "🤖 **AI Control Mode (Q-Learning)**\n\nThe trained agent makes optimal decisions automatically:\n\n**How AI decides:**\n• Analyzes current epidemic state\n• Evaluates 5 possible actions:\n  1. No action\n  2. Mask mandate\n  3. School closure\n  4. Mask + School closure\n  5. Vaccination drive\n• Chooses best action to minimize deaths\n\n**Key features:**\n✓ Learns from patterns\n✓ Makes real-time decisions\n✓ Finds optimal strategies\n✓ Adapts to mutations\n\n**First time setup:**\nRun in terminal: `python rl/train.py`\n\nWatch the AI make intelligent decisions!"
        },
        "comparison": {
            "keywords": ["comparison", "compare", "policy", "strategy", "side-by-side", "effectiveness", "best"],
            "answer": "📊 **Policy Comparison Mode**\n\nAutomatically tests 5 strategies side-by-side:\n\n**Strategies tested:**\n1. No Intervention\n2. Masks Only\n3. School Closure Only\n4. Vaccination Only\n5. Full Intervention (all three)\n\n**Results shown:**\n• Peak infected count\n• Total deaths\n• Final recovered\n• Economic cost\n• Complete SEIR curves\n\n**How to use:**\n1. Configure population and days\n2. Select Policy Comparison mode\n3. Run simulation\n4. See recommendation for best strategy\n5. Compare metrics across all strategies\n\n**Best for:**\n✓ Finding optimal policies\n✓ Understanding trade-offs\n✓ Budget planning\n✓ Decision making\n\nData-driven epidemic control!"
        },
        "mutations": {
            "keywords": ["mutation", "virus", "evolution", "change", "variant", "r0", "mortality", "transmission"],
            "answer": "🧬 **Virus Mutations Explained**\n\nRealistic viral evolution during epidemics:\n\n**How mutations trigger:**\nWhen infection rate exceeds threshold → virus evolves\n\n**What changes:**\n• R₀ (infectivity): How many people one person infects\n• β (transmission rate): Speed of spread\n• Mortality rate: Deadliness of virus\n\n**Mutation effects:**\n📈 May become MORE infectious\n📉 May become LESS deadly\n⚠️ Makes old interventions less effective\n\n**Realistic features:**\n✓ Happens naturally in simulations\n✓ Reflects real epidemiology\n✓ Challenges your strategies\n✓ Requires adaptation\n\n**Enable mutations for realism!**"
        },
        "results": {
            "keywords": ["results", "interpret", "metric", "peak", "death", "recovered", "susceptible", "analysis"],
            "answer": "📊 **Understanding Simulation Results**\n\n**Key metrics explained:**\n\n• **Peak Infected**: Maximum number infected simultaneously\n  → Lower is better (less hospital overload)\n\n• **Total Deaths**: Estimated mortality count\n  → Lower is better (policy effectiveness)\n\n• **Final Recovered**: Population with immunity\n  → Higher is better (herd immunity)\n\n• **Still Susceptible**: Uninfected at end\n  → Depends on your goal\n\n**Comparing strategies:**\n1. Look at total deaths first\n2. Check peak infections (hospital capacity)\n3. Consider economic cost\n4. Review vaccination coverage\n5. Make informed decisions\n\n**Using results for policy:**\n✓ Identify best intervention combination\n✓ Predict healthcare needs\n✓ Plan vaccination campaigns\n✓ Prepare for peak periods\n\nData-driven decision making!"
        },
        "who_database": {
            "keywords": ["who", "database", "disease", "pathogen", "covid", "measles", "flu", "ebola"],
            "answer": "📚 **WHO Database Integration**\n\nAccess verified parameters from World Health Organization:\n\n**Available diseases:**\n• COVID-19: Respiratory, moderate mortality\n• SARS: Respiratory, high mortality\n• Measles: Highly contagious, childhood disease\n• Influenza: Seasonal flu variant\n• Ebola: Hemorrhagic fever, high mortality\n\n**What WHO parameters include:**\n✓ R₀ (infectivity rate)\n✓ Incubation period\n✓ Infectious duration\n✓ Mortality rate\n✓ Age-specific effects\n\n**Benefits:**\n• Scientifically verified\n• Based on real outbreak data\n• Accurate disease modeling\n• Global standards\n\n**Or use Custom Models:**\nCreate your own pathogen parameters for testing!\n\nChoose your disease and explore!"
        },
        "getting_started": {
            "keywords": ["start", "begin", "setup", "help", "how to", "guide", "tutorial"],
            "answer": "📚 **Getting Started with EpiControl AI**\n\n**Step-by-step guide:**\n\n1️⃣ **Set Parameters**\n   • Population: 200-5000 agents\n   • Duration: 30-120 days\n\n2️⃣ **Choose Disease**\n   • WHO database (verified)\n   • Custom models (experimental)\n\n3️⃣ **Enable Features**\n   • Virus mutations (realistic)\n   • Visualizations (understanding)\n   • 🆕 Symptom Prediction (ML-based)\n\n4️⃣ **Select Control Mode**\n   • Manual: You decide interventions\n   • AI: Automatic optimization\n   • Comparison: Test 5 strategies\n\n5️⃣ **Run Simulation**\n   • Click \"Run Simulation\" button\n   • Watch progress bar\n   • Analyze results\n\n6️⃣ **Explore Visualizations**\n   • SEIR curves\n   • Geographic heatmaps\n   • Mutation timeline\n   • 🆕 Predicted symptom profiles\n\n**Tips:**\n✓ Start simple, add complexity\n✓ Compare different strategies\n✓ Vary one parameter at a time\n✓ Learn from mutations\n\nLet's explore epidemiology!"
        },
        "symptom_prediction": {
            "keywords": ["symptom", "predict", "symptoms", "prediction", "ml", "machine learning", "historical", "pattern", "profile"],
            "answer": "🔬 **Symptom Prediction Engine**\n\nOur NEW ML-based feature predicts probable symptom patterns for emerging viruses!\n\n**How it works:**\n• Analyzes your virus parameters (R₀, CFR, incubation period)\n• Compares with 6 historical pandemics:\n  - COVID-19 (2019)\n  - SARS (2003)\n  - MERS (2012)\n  - H1N1 Swine Flu (2009)\n  - Ebola (2014)\n  - Seasonal Flu (2020)\n• Uses weighted similarity scoring\n• Predicts likely symptom profiles\n\n**What you get:**\n✓ Primary symptoms with prevalence estimates\n✓ Secondary symptoms and onset timelines\n✓ Severe complication predictions\n✓ Age-specific impact forecasts\n✓ Confidence scores for predictions\n✓ Similar historical pandemic matches\n\n**Based on:**\n📊 3M Approach (Monitoring-Modelling-Managing)\n📚 WHO data + CDC databases\n📖 Peer-reviewed research\n\n**Use cases:**\n• Early pandemic preparedness\n• Scenario planning\n• Resource allocation\n• Healthcare capacity planning\n\n**Enable it:**\nCheck \"Enable Symptom Predictor\" in sidebar!\n\n⚠️ **Note:** Predictions are for preparedness planning, not clinical diagnosis."
        },
        "historical_data": {
            "keywords": ["historical", "data", "pandemic", "past", "database", "reference", "covid", "sars", "mers", "h1n1", "ebola"],
            "answer": "📚 **Historical Pandemic Database**\n\nOur symptom predictor uses data from 6 major pandemics:\n\n**1. COVID-19 (2019)**\n• R₀: 2.5 | CFR: 2.3%\n• Signature: Loss of smell/taste\n• Respiratory symptoms dominant\n\n**2. SARS (2003)**\n• R₀: 3.0 | CFR: 9.6%\n• Very severe, 100% hospitalization\n• High fever, respiratory failure\n\n**3. MERS (2012)**\n• R₀: 0.7 | CFR: 34.4%\n• Limited human transmission\n• Very high mortality\n\n**4. H1N1 Swine Flu (2009)**\n• R₀: 1.5 | CFR: 0.02%\n• Affected younger populations\n• Flu-like symptoms\n\n**5. Ebola (2014)**\n• R₀: 2.0 | CFR: 50%\n• Hemorrhagic symptoms\n• Direct contact transmission\n\n**6. Seasonal Flu (2020)**\n• R₀: 1.3 | CFR: 0.1%\n• Baseline comparison\n• Common respiratory virus\n\n**Data includes:**\n✓ Epidemiological parameters\n✓ Symptom prevalence rates\n✓ Age-stratified impacts\n✓ Mutation behaviors\n✓ Transmission routes\n\n**Sources:**\nWHO, CDC, ECDC, peer-reviewed studies"
        },
        "general": {
            "answer": "Hello! I'm your EpiControl AI assistant. I can help you understand:\n\n📈 **Visualizations**: SEIR curves, heatmaps, scatter plots, timelines\n🎮 **Control Modes**: Manual, AI (Q-Learning), Policy comparison\n🧬 **Features**: Mutations, interventions, WHO database\n📊 **Results**: How to interpret metrics and make decisions\n\nJust ask me anything about epidemic simulation! Examples:\n• \"What is SEIR curve?\"\n• \"How do mutations work?\"\n• \"Explain the heatmap\"\n• \"What's the AI mode?\"\n• \"How do I get started?\"\n\nWhat would you like to know?"
        }
    },
    
    "es": {
        "seir_curve": {
            "keywords": ["seir", "curva", "progresión", "epidemia"],
            "answer": "📈 **Explicación de la Curva SEIR**\n\nLa curva SEIR muestra la progresión de la epidemia:\n\n• **S**: Susceptibles (pueden contagiarse)\n• **E**: Expuestos (infectados pero no contagiosos)\n• **I**: Infectados (contagiosos)\n• **R**: Recuperados (inmunidad)\n\n¿Qué revela?\n✓ Cuándo alcanzan pico las infecciones\n✓ Velocidad de propagación\n✓ Efectividad de intervenciones\n✓ Comparación de estrategias\n\n¡Observa cómo se aplanan las curvas con mejores intervenciones!"
        },
        "general": {
            "answer": "¡Hola! Soy tu asistente de EpiControl AI. Puedo ayudarte con:\n\n📈 Visualizaciones, 🎮 Modos de control, 🧬 Características\n\n¿Qué te gustaría saber?"
        }
    },
    
    "fr": {
        "seir_curve": {
            "keywords": ["seir", "courbe", "progression"],
            "answer": "📈 **Explication de la Courbe SEIR**\n\nLa courbe SEIR montre la progression de l'épidémie:\n\n• **S**: Susceptibles\n• **E**: Exposés\n• **I**: Infectés\n• **R**: Rétablis\n\nQu'est-ce que cela révèle?\n✓ Quand les infections atteignent le pic\n✓ Vitesse de propagation\n✓ Efficacité des interventions\n\nObservez comment les courbes s'aplatissent!"
        },
        "general": {
            "answer": "Bonjour! Je suis votre assistant EpiControl AI. Comment puis-je vous aider?"
        }
    },
    
    "de": {
        "seir_curve": {
            "keywords": ["seir", "kurve", "fortschritt"],
            "answer": "📈 **SEIR-Kurven-Erklärung**\n\nDie SEIR-Kurve zeigt den Epidemieverlauf:\n\n• **S**: Anfällig\n• **E**: Exponiert\n• **I**: Infiziert\n• **R**: Genesen\n\nWas zeigt es?\n✓ Wann Infektionen ihren Höhepunkt erreichen\n✓ Ausbreitungsgeschwindigkeit\n✓ Wirksamkeit von Interventionen\n\nBeobachten Sie die Kurven!"
        },
        "general": {
            "answer": "Hallo! Ich bin Ihr EpiControl AI Assistent. Wie kann ich dir helfen?"
        }
    },
    
    "hi": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR कर्व की व्याख्या**\n\nSEIR कर्व महामारी की प्रगति दिखाता है:\n\n• **S**: अतिसंवेदनशील (संक्रमित हो सकते हैं)\n• **E**: उजागर (संक्रमित पर संक्रामक नहीं)\n• **I**: संक्रमित (संक्रामक)\n• **R**: ठीक (प्रतिरक्षा)\n\nक्या दिखाता है?\n✓ संक्रमण कब चरम पर पहुंचते हैं\n✓ प्रसार की गति\n✓ हस्तक्षेप की प्रभावशीलता\n\nबेहतर हस्तक्षेप से कर्व कैसे समतल होते हैं!"
        },
        "general": {
            "answer": "नमस्ते! मैं आपका EpiControl AI सहायक हूं। मैं कैसे मदद कर सकता हूं?"
        }
    },
    
    "zh": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR曲线解释**\n\nSEIR曲线显示流行病的进展:\n\n• **S**: 易感者(可感染)\n• **E**: 暴露者(已感染但无传染性)\n• **I**: 感染者(有传染性)\n• **R**: 恢复者(有免疫力)\n\n它显示什么?\n✓ 感染何时达到顶峰\n✓ 传播速度\n✓ 干预措施的有效性\n\n观察更好的干预如何使曲线变平!"
        },
        "general": {
            "answer": "你好! 我是你的EpiControl AI助手。我能如何帮助你?"
        }
    },
    
    "kn": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR ಕರ್ವ್ ವಿವರಣೆ**\n\nSEIR ಕರ್ವ್ ಸಾಂಕ್ರಾಮಿಕದ ಪ್ರಗತಿಯನ್ನು ತೋರಿಸುತ್ತದೆ:\n\n• **S**: ಸೂಕ್ಷ್ಮ (ಸೋಂಕಾಗಬಹುದು)\n• **E**: ಬಹಿರಂಗ (ಸೋಂಕಿತ ಆದರೆ ಸಾಂಕ್ರಾಮಿಕವಲ್ಲ)\n• **I**: ಸೋಂಕಿತ (ಸಾಂಕ್ರಾಮಿಕ)\n• **R**: ಚೇತರಿಸಿಕೊಂಡ (ರೋಗನಿರೋಧಕ)\n\nಇದು ಏನು ತೋರಿಸುತ್ತದೆ?\n✓ ಸೋಂಕುಗಳು ಯಾವಾಗ ಗರಿಷ್ಠವಾಗುತ್ತವೆ\n✓ ಹರಡುವಿಕೆಯ ವೇಗ\n✓ ಮಧ್ಯಸ್ಥಿಕೆಗಳ ಪರಿಣಾಮಕಾರಿತ್ವ\n\nಉತ್ತಮ ಮಧ್ಯಸ್ಥಿಕೆಗಳೊಂದಿಗೆ ಕರ್ವ್‌ಗಳು ಹೇಗೆ ಚಪ್ಪಟೆಯಾಗುತ್ತವೆ ಎಂದು ನೋಡಿ!"
        },
        "general": {
            "answer": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ EpiControl AI ಸಹಾಯಕ. ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
        }
    },
    
    "mr": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR वक्र स्पष्टीकरण**\n\nSEIR वक्र साथीच्या रोगाची प्रगती दर्शवितो:\n\n• **S**: संवेदनशील (संक्रमित होऊ शकतात)\n• **E**: उघड (संक्रमित परंतु संसर्गजन्य नाही)\n• **I**: संक्रमित (संसर्गजन्य)\n• **R**: बरे झालेले (रोगप्रतिकारक)\n\nहे काय दर्शवते?\n✓ संक्रमण कधी शिखरावर पोहोचतात\n✓ प्रसाराचा वेग\n✓ हस्तक्षेपांची परिणामकारकता\n\nचांगल्या हस्तक्षेपांसह वक्र कसे सपाट होतात ते पहा!"
        },
        "general": {
            "answer": "नमस्कार! मी तुमचा EpiControl AI सहाय्यक आहे. मी कशी मदत करू शकतो?"
        }
    },
    
    "ta": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR வளைவு விளக்கம்**\n\nSEIR வளைவு தொற்றுநோய் முன்னேற்றத்தைக் காட்டுகிறது:\n\n• **S**: பாதிக்கப்படக்கூடியவை (தொற்று ஏற்படலாம்)\n• **E**: வெளிப்படுத்தப்பட்டவை (பாதிக்கப்பட்டது ஆனால் தொற்று இல்லை)\n• **I**: பாதிக்கப்பட்டவை (தொற்று)\n• **R**: மீட்கப்பட்டவை (நோய் எதிர்ப்பு)\n\nஇது என்ன காட்டுகிறது?\n✓ தொற்றுகள் எப்போது உச்சத்தை அடைகின்றன\n✓ பரவல் வேகம\n✓ தலையீடுகளின் செயல்திறன்\n\nசிறந்த தலையீடுகளுடன் வளைவுகள் எவ்வாறு தட்டையாகின்றன என்பதைப் பாருங்கள்!"
        },
        "general": {
            "answer": "வணக்கம்! நான் உங்கள் EpiControl AI உதவியாளர். நான் எப்படி உதவ முடியும்?"
        }
    },
    
    "te": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR వక్రరేఖ వివరణ**\n\nSEIR వక్రరేఖ అంటువ్యాధి పురోగతిని చూపిస్తుంది:\n\n• **S**: సెన్సిటివ్ (సోకవచ్చు)\n• **E**: బహిర్గతం (సోకినది కానీ అంటువ్యాధి కాదు)\n• **I**: సోకిన (అంటువ్యాధి)\n• **R**: కోలుకున్న (రోగనిరోధక)\n\nఇది ఏమి చూపిస్తుంది?\n✓ సోకిన వారు ఎప్పుడు శిఖరాన్ని చేరుకుంటారు\n✓ వ్యాప్తి వేగం\n✓ జోక్యాల ప్రభావం\n\nమెరుగైన జోక్యాలతో వక్రరేఖలు ఎలా చదునుగా మారతాయో చూడండి!"
        },
        "general": {
            "answer": "నమస్కారం! నేను మీ EpiControl AI సహాయకుడిని. నేను ఎలా సహాయం చేయగలను?"
        }
    },
    
    "gu": {
        "seir_curve": {
            "keywords": ["seir", "curve", "progression"],
            "answer": "📈 **SEIR વક્ર સમજૂતી**\n\nSEIR વક્ર રોગચાળાની પ્રગતિ દર્શાવે છે:\n\n• **S**: સંવેદનશીલ (ચેપ લાગી શકે)\n• **E**: ઉઘાડું (ચેપગ્રસ્ત પરંતુ ચેપી નથી)\n• **I**: ચેપગ્રસ્ત (ચેપી)\n• **R**: સ્વસ્થ (રોગપ્રતિકારક)\n\nઆ શું બતાવે છે?\n✓ ચેપ ક્યારે શિખર પર પહોંચે છે\n✓ ફેલાવાની ઝડપ\n✓ હસ્તક્ષેપની અસરકારકતા\n\nશ્રેષ્ઠ હસ્તક્ષેપ સાથે વક્રો કેવી રીતે સપાટ થાય છે તે જુઓ!"
        },
        "general": {
            "answer": "નમસ્તે! હું તમારો EpiControl AI સહાયક છું. હું કેવી રીતે મદદ કરી શકું?"
        }
    },

    "ar": {
        "seir_curve": {
            "keywords": ["seir", "منحنى", "وباء", "تقدم"],
            "answer": "📈 **شرح منحنى SEIR**\n\nيُظهر منحنى SEIR تطور الوباء عبر الزمن:\n\n• **S**: المعرضون للإصابة\n• **E**: المتعرضون (مصابون لكن غير معديين)\n• **I**: المصابون (معديون)\n• **R**: المتعافون (لديهم مناعة)\n\nماذا يكشف؟\n✓ متى تبلغ العدوى ذروتها\n✓ سرعة الانتشار\n✓ فعالية التدخلات\n\nلاحظ كيف تتسطح المنحنيات مع تدخلات أفضل!"
        },
        "general": {
            "answer": "مرحباً! أنا مساعد EpiControl AI الخاص بك. كيف يمكنني مساعدتك؟"
        }
    },

    "ja": {
        "seir_curve": {
            "keywords": ["seir", "曲線", "感染", "流行"],
            "answer": "📈 **SEIR曲線の説明**\n\nSEIR曲線は疫病の進行を示します：\n\n• **S**: 感受性者（感染する可能性あり）\n• **E**: 曝露者（感染しているが感染力なし）\n• **I**: 感染者（感染力あり）\n• **R**: 回復者（免疫あり）\n\n何がわかる？\n✓ 感染がいつピークに達するか\n✓ 拡散速度\n✓ 介入の効果\n\nより良い介入で曲線がどのように平坦化するか観察しましょう！"
        },
        "general": {
            "answer": "こんにちは！EpiControl AIアシスタントです。どのようにお手伝いできますか？"
        }
    },

    "ko": {
        "seir_curve": {
            "keywords": ["seir", "곡선", "감염", "전염병"],
            "answer": "📈 **SEIR 곡선 설명**\n\nSEIR 곡선은 전염병의 진행 과정을 보여줍니다:\n\n• **S**: 감수성자 (감염 가능)\n• **E**: 노출자 (감염되었으나 전파력 없음)\n• **I**: 감염자 (전파력 있음)\n• **R**: 회복자 (면역 보유)\n\n무엇을 알 수 있나요?\n✓ 감염이 언제 정점에 도달하는지\n✓ 확산 속도\n✓ 개입의 효과\n\n더 나은 개입으로 곡선이 어떻게 평탄화되는지 관찰하세요!"
        },
        "general": {
            "answer": "안녕하세요! EpiControl AI 어시스턴트입니다. 어떻게 도와드릴까요?"
        }
    },

    "pt": {
        "seir_curve": {
            "keywords": ["seir", "curva", "progressão", "epidemia"],
            "answer": "📈 **Explicação da Curva SEIR**\n\nA curva SEIR mostra a progressão da epidemia:\n\n• **S**: Suscetíveis (podem ser infectados)\n• **E**: Expostos (infectados mas não infecciosos)\n• **I**: Infectados (infecciosos)\n• **R**: Recuperados (imunidade)\n\nO que revela?\n✓ Quando as infecções atingem o pico\n✓ Velocidade de propagação\n✓ Eficácia das intervenções\n\nObserve como as curvas se achatam com melhores intervenções!"
        },
        "general": {
            "answer": "Olá! Sou seu assistente EpiControl AI. Como posso ajudar?"
        }
    },

    "ru": {
        "seir_curve": {
            "keywords": ["seir", "кривая", "эпидемия", "инфекция"],
            "answer": "📈 **Объяснение кривой SEIR**\n\nКривая SEIR показывает развитие эпидемии:\n\n• **S**: Восприимчивые (могут заразиться)\n• **E**: Контактные (заражены, но не заразны)\n• **I**: Инфицированные (заразны)\n• **R**: Выздоровевшие (иммунитет)\n\nЧто показывает?\n✓ Когда инфекции достигают пика\n✓ Скорость распространения\n✓ Эффективность вмешательств\n\nНаблюдайте, как кривые сглаживаются при лучших вмешательствах!"
        },
        "general": {
            "answer": "Здравствуйте! Я ваш помощник EpiControl AI. Чем могу помочь?"
        }
    }
}


class AdvancedChatbot:
    def __init__(self, language: str = "en"):
        self.language = language
        self.conversation_history: List[Tuple[str, str]] = []
        self.knowledge_base = KNOWLEDGE_BASE.get(language, KNOWLEDGE_BASE["en"])
        self.groq_client = None
        if GROQ_AVAILABLE and GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception:
                self.groq_client = None

    def _build_system_prompt(self) -> str:
        """Build a system prompt with knowledge base context"""
        lang_names = {"en": "English", "es": "Spanish", "fr": "French", "de": "German",
                      "hi": "Hindi", "zh": "Chinese", "kn": "Kannada", "mr": "Marathi",
                      "ta": "Tamil", "te": "Telugu", "gu": "Gujarati",
                      "ar": "Arabic", "ja": "Japanese", "ko": "Korean",
                      "pt": "Portuguese", "ru": "Russian"}
        lang_name = lang_names.get(self.language, "English")

        kb_summary = ""
        for topic, content in self.knowledge_base.items():
            if "answer" in content:
                kb_summary += f"\n--- {topic} ---\n{content['answer']}\n"

        return f"""You are the EpiControl AI Assistant, a helpful and knowledgeable chatbot embedded in the EpiControl AI epidemic simulation platform.

Respond in {lang_name}. Be concise but thorough. Use emojis where appropriate to make responses engaging.

Key knowledge about the platform:
{kb_summary}

Guidelines:
- Answer questions about SEIR models, epidemic simulation, visualizations, interventions, mutations, AI mode, etc.
- If the user asks something outside the scope of EpiControl AI, politely redirect them to relevant topics.
- Keep responses well-formatted with markdown (bold, bullet points, etc.).
- Be friendly and educational.
- If you don't know something specific about the platform, use your general epidemiology knowledge to give a helpful answer.
- If the user writes in a language different from {lang_name}, auto-detect their language and respond in that language instead.
- You support 16 languages: English, Spanish, French, German, Hindi, Chinese, Kannada, Marathi, Tamil, Telugu, Gujarati, Arabic, Japanese, Korean, Portuguese, and Russian.
"""

    def _call_groq(self, user_message: str) -> str:
        """Call Groq API for LLM response"""
        messages = [{"role": "system", "content": self._build_system_prompt()}]

        # Add recent conversation history (last 10 exchanges for context)
        for role, msg in self.conversation_history[-20:]:
            messages.append({
                "role": "user" if role == "user" else "assistant",
                "content": msg
            })

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        response = self.groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    
    def find_best_match(self, user_query: str) -> Tuple[str, str]:
        """Find best knowledge base match for user question (fallback)"""
        query_lower = user_query.lower()
        best_match = ("general", 0)
        
        for topic, content in self.knowledge_base.items():
            match_score = 0
            keywords = content.get("keywords", [])
            
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    match_score += 1
            
            if match_score > best_match[1]:
                best_match = (topic, match_score)
        
        topic = best_match[0]
        answer = self.knowledge_base[topic].get("answer", self.knowledge_base["general"]["answer"])
        return topic, answer
    
    def respond(self, user_message: str) -> str:
        """Generate response using Groq LLM, with keyword fallback"""
        # Add to conversation history
        self.conversation_history.append(("user", user_message))
        
        # Try Groq API first
        if self.groq_client:
            try:
                response = self._call_groq(user_message)
                self.conversation_history.append(("assistant", response))
                return response
            except Exception:
                pass

        # Fallback to keyword matching
        topic, response = self.find_best_match(user_message)
        self.conversation_history.append(("assistant", response))
        return response
    
    def set_language(self, language: str):
        """Change language"""
        self.language = language
        self.knowledge_base = KNOWLEDGE_BASE.get(language, KNOWLEDGE_BASE["en"])
        # Clear history when changing language
        self.conversation_history = []
    
    def get_history(self) -> List[Tuple[str, str]]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def format_chat_message(role: str, message: str) -> str:
    """Format chat message for display"""
    if role == "user":
        return f"👤 **You**: {message}"
    else:
        return f"🤖 **Assistant**: {message}"

