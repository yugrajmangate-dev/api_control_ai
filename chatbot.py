"""
Advanced conversational chatbot for EpiControl AI.
Uses AWS Bedrock Converse for multi-turn responses with a local knowledge-base fallback.
"""

import os
import re
from typing import List, Tuple

import boto3

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "eu-north-1")
BEDROCK_MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID",
    "arn:aws:bedrock:eu-north-1:420859418876:inference-profile/eu.anthropic.claude-opus-4-5-20251101-v1:0",
)
BEDROCK_MAX_TOKENS = int(os.environ.get("BEDROCK_MAX_TOKENS", "500"))
BEDROCK_TEMPERATURE = float(os.environ.get("BEDROCK_TEMPERATURE", "0.5"))
BEDROCK_TOP_K = int(os.environ.get("BEDROCK_TOP_K", "250"))

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
    "zh": "Chinese",
    "kn": "Kannada",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "ar": "Arabic",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
}

LOCALIZED_FALLBACKS = {
    "en": {
        "math_result": "The result is **{result}**.",
        "math_bridge": "If you want, we can bring that same analytical thinking back to EpiControl AI by exploring outbreak metrics, intervention comparisons, or SEIR trends.",
        "greeting": "Hello. I can answer general questions briefly and also help you explore the EpiControl AI platform.",
        "greeting_bridge": "If you want to stay on-theme, ask about SEIR modeling, outbreak control strategies, virus mutations, symptom prediction, or how to interpret the dashboard.",
        "identity": "I am the EpiControl AI assistant. I can help with general questions in a short form, but I am primarily designed to support epidemic simulation, public health decision-making, and this app's features.",
        "identity_bridge": "You can ask me about outbreak protocols, intervention strategies, SEIR curves, or how to use the platform effectively.",
        "python": "Python is a high-level programming language widely used for web apps, automation, data science, machine learning, and scientific computing because it is readable and has a large ecosystem of libraries.",
        "python_bridge": "In this app's context, Python powers the EpiControl AI simulation engine, dashboard logic, and chatbot integration.",
        "who": "WHO stands for the **World Health Organization**, the United Nations agency focused on international public health, disease surveillance, and health guidance.",
        "who_bridge": "That connects directly to this app because EpiControl AI uses WHO-style epidemiological concepts and verified disease parameters for simulation and planning.",
        "help": "I can help with both quick general guidance and the main topics in this app.",
        "help_bridge": "For the best experience here, ask about epidemic spread, policy comparison, AI control mode, mutation behavior, or symptom prediction so I can connect the answer to the dashboard.",
        "generic": "Here is a brief general response: I can usually give a short answer to broad questions, but this assistant is most useful when connecting information back to epidemic intelligence and decision support.",
        "generic_bridge": "If you want, ask your question again in relation to disease spread, public health planning, interventions, or the EpiControl AI features shown in this app.",
    },
    "es": {
        "math_result": "El resultado es **{result}**.",
        "math_bridge": "Si quieres, podemos llevar ese mismo pensamiento analitico a EpiControl AI explorando metricas de brotes, comparacion de intervenciones o tendencias SEIR.",
        "greeting": "Hola. Puedo responder preguntas generales brevemente y tambien ayudarte a explorar la plataforma EpiControl AI.",
        "greeting_bridge": "Si quieres mantenerte en el tema, pregunta sobre modelado SEIR, estrategias de control de brotes, mutaciones del virus, prediccion de sintomas o como interpretar el panel.",
        "identity": "Soy el asistente de EpiControl AI. Puedo ayudar con preguntas generales de forma breve, pero estoy disenado principalmente para apoyar simulacion epidemica, toma de decisiones en salud publica y las funciones de esta app.",
        "identity_bridge": "Puedes preguntarme sobre protocolos de brotes, estrategias de intervencion, curvas SEIR o como usar la plataforma eficazmente.",
        "python": "Python es un lenguaje de programacion de alto nivel muy usado para aplicaciones web, automatizacion, ciencia de datos, aprendizaje automatico y computacion cientifica por su claridad y su amplio ecosistema de librerias.",
        "python_bridge": "En esta app, Python impulsa el motor de simulacion de EpiControl AI, la logica del panel y la integracion del chatbot.",
        "who": "WHO significa **World Health Organization**; en espanol, la Organizacion Mundial de la Salud, la agencia de las Naciones Unidas centrada en salud publica internacional, vigilancia de enfermedades y orientacion sanitaria.",
        "who_bridge": "Eso se conecta directamente con esta app porque EpiControl AI usa conceptos epidemiologicos de estilo OMS y parametros verificados para simulacion y planificacion.",
        "help": "Puedo ayudar tanto con orientacion general rapida como con los temas principales de esta app.",
        "help_bridge": "Para una mejor experiencia aqui, pregunta sobre propagacion epidemica, comparacion de politicas, modo de control con IA, comportamiento de mutaciones o prediccion de sintomas.",
        "generic": "Aqui tienes una respuesta general breve: normalmente puedo responder preguntas amplias, pero este asistente es mas util cuando conecta la informacion con inteligencia epidemica y apoyo a decisiones.",
        "generic_bridge": "Si quieres, vuelve a hacer tu pregunta en relacion con propagacion de enfermedades, planificacion de salud publica, intervenciones o las funciones de EpiControl AI.",
    },
    "fr": {
        "math_result": "Le resultat est **{result}**.",
        "math_bridge": "Si vous voulez, nous pouvons ramener cette meme logique analytique vers EpiControl AI en explorant les metriques d'epidemie, la comparaison des interventions ou les tendances SEIR.",
        "greeting": "Bonjour. Je peux repondre brievement a des questions generales et aussi vous aider a explorer la plateforme EpiControl AI.",
        "greeting_bridge": "Si vous voulez rester dans le theme, posez des questions sur la modelisation SEIR, le controle des epidemies, les mutations virales, la prediction des symptomes ou l'interpretation du tableau de bord.",
        "identity": "Je suis l'assistant EpiControl AI. Je peux aider pour des questions generales de facon breve, mais je suis surtout concu pour la simulation epidemique, la prise de decision en sante publique et les fonctionnalites de cette application.",
        "identity_bridge": "Vous pouvez me demander des informations sur les protocoles d'epidemie, les strategies d'intervention, les courbes SEIR ou l'utilisation efficace de la plateforme.",
        "python": "Python est un langage de programmation de haut niveau tres utilise pour les applications web, l'automatisation, la science des donnees, l'apprentissage automatique et le calcul scientifique grace a sa lisibilite et a son vaste ecosysteme.",
        "python_bridge": "Dans cette application, Python alimente le moteur de simulation EpiControl AI, la logique du tableau de bord et l'integration du chatbot.",
        "who": "WHO signifie **World Health Organization**; en francais, l'Organisation mondiale de la Sante, l'agence des Nations Unies consacree a la sante publique internationale, a la surveillance des maladies et aux recommandations sanitaires.",
        "who_bridge": "Cela est directement lie a cette application car EpiControl AI utilise des concepts epidemiologiques de type OMS et des parametres verifies pour la simulation et la planification.",
        "help": "Je peux aider a la fois pour des conseils generaux rapides et pour les principaux sujets de cette application.",
        "help_bridge": "Pour une meilleure experience ici, posez des questions sur la propagation des epidemies, la comparaison des politiques, le mode IA, le comportement des mutations ou la prediction des symptomes.",
        "generic": "Voici une breve reponse generale: je peux habituellement repondre a des questions larges, mais cet assistant est surtout utile lorsqu'il relie l'information a l'intelligence epidemique et a l'aide a la decision.",
        "generic_bridge": "Si vous voulez, reformulez votre question en lien avec la propagation des maladies, la planification sanitaire, les interventions ou les fonctionnalites d'EpiControl AI.",
    },
    "de": {
        "math_result": "Das Ergebnis ist **{result}**.",
        "math_bridge": "Wenn Sie moechten, koennen wir dieses analytische Denken wieder auf EpiControl AI beziehen, etwa ueber Ausbruchsmetriken, Interventionsvergleiche oder SEIR-Trends.",
        "greeting": "Hallo. Ich kann allgemeine Fragen kurz beantworten und Ihnen auch helfen, die EpiControl AI Plattform zu erkunden.",
        "greeting_bridge": "Wenn Sie beim Thema bleiben moechten, fragen Sie nach SEIR-Modellierung, Ausbruchskontrolle, Virusmutationen, Symptomvorhersage oder der Interpretation des Dashboards.",
        "identity": "Ich bin der EpiControl AI Assistent. Ich kann allgemeine Fragen kurz beantworten, bin aber in erster Linie fuer Epidemiesimulation, Entscheidungen im Bereich Public Health und die Funktionen dieser App gedacht.",
        "identity_bridge": "Sie koennen mich zu Ausbruchsprotokollen, Interventionsstrategien, SEIR-Kurven oder zur effektiven Nutzung der Plattform befragen.",
        "python": "Python ist eine Programmiersprache auf hohem Niveau, die wegen ihrer guten Lesbarkeit und ihres grossen Oekosystems haeufig fuer Webanwendungen, Automatisierung, Data Science, Machine Learning und wissenschaftliches Rechnen eingesetzt wird.",
        "python_bridge": "In dieser App treibt Python die Simulationsengine von EpiControl AI, die Dashboard-Logik und die Chatbot-Integration an.",
        "who": "WHO steht fuer **World Health Organization**; auf Deutsch die Weltgesundheitsorganisation, die UN-Organisation fuer internationale oeffentliche Gesundheit, Krankheitsueberwachung und Gesundheitsrichtlinien.",
        "who_bridge": "Das passt direkt zu dieser App, weil EpiControl AI WHO-nahe epidemiologische Konzepte und verifizierte Krankheitsparameter fuer Simulation und Planung nutzt.",
        "help": "Ich kann sowohl bei kurzen allgemeinen Fragen als auch bei den Kernthemen dieser App helfen.",
        "help_bridge": "Fuer die beste Erfahrung hier fragen Sie nach Krankheitsausbreitung, Politikvergleich, KI-Steuerungsmodus, Mutationsverhalten oder Symptomvorhersage.",
        "generic": "Hier ist eine kurze allgemeine Antwort: Ich kann meist auch breite Fragen beantworten, bin aber besonders nuetzlich, wenn Informationen mit epidemischer Intelligenz und Entscheidungsunterstuetzung verknuepft werden.",
        "generic_bridge": "Wenn Sie moechten, stellen Sie Ihre Frage erneut im Zusammenhang mit Krankheitsausbreitung, Gesundheitsplanung, Interventionen oder den Funktionen von EpiControl AI.",
    },
    "hi": {
        "math_result": "परिणाम **{result}** है।",
        "math_bridge": "यदि आप चाहें, तो हम इसी विश्लेषणात्मक सोच को EpiControl AI में outbreak metrics, intervention comparison या SEIR trends से जोड़ सकते हैं।",
        "greeting": "नमस्ते। मैं सामान्य प्रश्नों का संक्षिप्त उत्तर दे सकता हूं और EpiControl AI प्लेटफॉर्म को समझने में भी मदद कर सकता हूं।",
        "greeting_bridge": "यदि आप इसी विषय पर रहना चाहते हैं, तो SEIR modeling, outbreak control strategies, virus mutations, symptom prediction या dashboard interpretation के बारे में पूछें।",
        "identity": "मैं EpiControl AI सहायक हूं। मैं सामान्य प्रश्नों में संक्षिप्त मदद कर सकता हूं, लेकिन मेरा मुख्य उद्देश्य epidemic simulation, public health decision-making और इस app की features में सहायता करना है।",
        "identity_bridge": "आप मुझसे outbreak protocols, intervention strategies, SEIR curves या platform का प्रभावी उपयोग कैसे करें, यह पूछ सकते हैं।",
        "python": "Python एक high-level programming language है, जिसका उपयोग web apps, automation, data science, machine learning और scientific computing में इसकी readability और बड़े library ecosystem के कारण व्यापक रूप से किया जाता है।",
        "python_bridge": "इस app में Python, EpiControl AI simulation engine, dashboard logic और chatbot integration को चलाता है।",
        "who": "WHO का अर्थ **World Health Organization** है, यानी विश्व स्वास्थ्य संगठन, जो international public health, disease surveillance और health guidance पर काम करने वाली संयुक्त राष्ट्र संस्था है।",
        "who_bridge": "यह सीधे इस app से जुड़ता है क्योंकि EpiControl AI simulation और planning के लिए WHO-style epidemiological concepts और verified disease parameters का उपयोग करता है।",
        "help": "मैं तेज सामान्य मार्गदर्शन और इस app के मुख्य विषयों दोनों में मदद कर सकता हूं।",
        "help_bridge": "बेहतर अनुभव के लिए epidemic spread, policy comparison, AI control mode, mutation behavior या symptom prediction के बारे में पूछें।",
        "generic": "यह एक संक्षिप्त सामान्य उत्तर है: मैं व्यापक प्रश्नों का छोटा उत्तर दे सकता हूं, लेकिन यह सहायक तब सबसे उपयोगी होता है जब जानकारी को epidemic intelligence और decision support से जोड़ा जाए।",
        "generic_bridge": "यदि आप चाहें, तो अपना प्रश्न disease spread, public health planning, interventions या EpiControl AI features के संदर्भ में फिर से पूछें।",
    },
    "zh": {
        "math_result": "结果是 **{result}**。",
        "math_bridge": "如果你愿意，我们可以把这种分析思路带回 EpiControl AI，例如查看疫情指标、干预比较或 SEIR 趋势。",
        "greeting": "你好。我可以简短回答一般问题，也可以帮助你了解 EpiControl AI 平台。",
        "greeting_bridge": "如果你想回到主题，可以询问 SEIR 建模、疫情控制策略、病毒变异、症状预测或如何解读仪表板。",
        "identity": "我是 EpiControl AI 助手。我可以简短回答一般问题，但我的主要用途是支持流行病模拟、公共卫生决策以及本应用的功能使用。",
        "identity_bridge": "你可以问我暴发应对流程、干预策略、SEIR 曲线，或如何更有效地使用这个平台。",
        "python": "Python 是一种高级编程语言，因其可读性强和生态丰富，被广泛用于 Web 应用、自动化、数据科学、机器学习和科学计算。",
        "python_bridge": "在这个应用中，Python 驱动 EpiControl AI 的模拟引擎、仪表板逻辑和聊天机器人集成。",
        "who": "WHO 是 **World Health Organization**，即世界卫生组织，是联合国负责国际公共卫生、疾病监测和健康指导的机构。",
        "who_bridge": "这与本应用直接相关，因为 EpiControl AI 在模拟和规划中使用了 WHO 风格的流行病学概念和经过验证的疾病参数。",
        "help": "我既可以提供简短的一般帮助，也可以帮助你了解本应用的核心主题。",
        "help_bridge": "为了获得更好的体验，你可以询问疾病传播、政策比较、AI 控制模式、变异行为或症状预测。",
        "generic": "这里给你一个简短的一般回答：我通常可以回答宽泛问题，但当问题与流行病智能和决策支持相关时，我会更有帮助。",
        "generic_bridge": "如果你愿意，可以把问题放到疾病传播、公共卫生规划、干预措施或 EpiControl AI 功能的背景下再问一次。",
    },
    "kn": {
        "math_result": "ಫಲಿತಾಂಶ **{result}** ಆಗಿದೆ.",
        "math_bridge": "ನಿಮಗೆ ಬೇಕಿದ್ದರೆ, ಇದೇ ವಿಶ್ಲೇಷಣಾತ್ಮಕ ಚಿಂತನೆ ಅನ್ನು EpiControl AI ನಲ್ಲಿ outbreak metrics, intervention comparison ಅಥವಾ SEIR trends ಕಡೆಗೆ ತೆಗೆದುಕೊಂಡು ಹೋಗಬಹುದು.",
        "greeting": "ನಮಸ್ಕಾರ. ನಾನು ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳಿಗೆ ಚುಟುಕು ಉತ್ತರ ನೀಡಬಹುದು ಮತ್ತು EpiControl AI ವೇದಿಕೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಹಾಯ ಮಾಡಬಹುದು.",
        "greeting_bridge": "ವಿಷಯದಲ್ಲೇ ಮುಂದುವರೆಯಲು SEIR modeling, outbreak control strategies, virus mutations, symptom prediction ಅಥವಾ dashboard interpretation ಬಗ್ಗೆ ಕೇಳಿ.",
        "identity": "ನಾನು EpiControl AI ಸಹಾಯಕ. ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳಿಗೆ ಚುಟುಕು ಸಹಾಯ ಮಾಡಬಹುದು, ಆದರೆ ನನ್ನ ಮುಖ್ಯ ಉದ್ದೇಶ epidemic simulation, public health decision-making ಮತ್ತು ಈ app ನ ವೈಶಿಷ್ಟ್ಯಗಳಿಗೆ ಬೆಂಬಲ ನೀಡುವುದಾಗಿದೆ.",
        "identity_bridge": "ನೀವು outbreak protocols, intervention strategies, SEIR curves ಅಥವಾ platform ಅನ್ನು ಹೇಗೆ ಬಳಸುವುದು ಎಂಬುದನ್ನು ಕೇಳಬಹುದು.",
        "python": "Python ಒಂದು high-level programming language ಆಗಿದ್ದು, readability ಮತ್ತು ದೊಡ್ಡ library ecosystem ಕಾರಣದಿಂದ web apps, automation, data science, machine learning ಮತ್ತು scientific computing ನಲ್ಲಿ ವ್ಯಾಪಕವಾಗಿ ಬಳಸಲಾಗುತ್ತದೆ.",
        "python_bridge": "ಈ app ನಲ್ಲಿ Python, EpiControl AI simulation engine, dashboard logic ಮತ್ತು chatbot integration ಅನ್ನು ಚಾಲನೆ ಮಾಡುತ್ತದೆ.",
        "who": "WHO ಎಂದರೆ **World Health Organization**, ಅಂದರೆ ವಿಶ್ವ ಆರೋಗ್ಯ ಸಂಸ್ಥೆ, ಇದು international public health, disease surveillance ಮತ್ತು health guidance ಮೇಲೆ ಕೆಲಸ ಮಾಡುವ ಸಂಸ್ಥೆಯಾಗಿದೆ.",
        "who_bridge": "ಇದು ಈ app ಗೆ ನೇರವಾಗಿ ಸಂಬಂಧಿಸಿದೆ, ಏಕೆಂದರೆ EpiControl AI simulation ಮತ್ತು planning ಗಾಗಿ WHO-style epidemiological concepts ಮತ್ತು verified disease parameters ಅನ್ನು ಬಳಸುತ್ತದೆ.",
        "help": "ನಾನು ಚುಟುಕು ಸಾಮಾನ್ಯ ಮಾರ್ಗದರ್ಶನಕ್ಕೂ, ಈ app ನ ಮುಖ್ಯ ವಿಷಯಗಳಿಗೂ ಸಹಾಯ ಮಾಡಬಹುದು.",
        "help_bridge": "ಉತ್ತಮ ಅನುಭವಕ್ಕಾಗಿ epidemic spread, policy comparison, AI control mode, mutation behavior ಅಥವಾ symptom prediction ಬಗ್ಗೆ ಕೇಳಿ.",
        "generic": "ಇದು ಒಂದು ಚುಟುಕು ಸಾಮಾನ್ಯ ಉತ್ತರ: ನಾನು ವಿಶಾಲ ಪ್ರಶ್ನೆಗಳಿಗೆ ಸಹ ಚಿಕ್ಕ ಉತ್ತರ ನೀಡಬಹುದು, ಆದರೆ epidemic intelligence ಮತ್ತು decision support ಜೊತೆ ಸಂಪರ್ಕಿಸಿದಾಗ ನಾನು ಹೆಚ್ಚು ಉಪಯುಕ್ತನಾಗುತ್ತೇನೆ.",
        "generic_bridge": "ನೀವು ಬೇಕಿದ್ದರೆ, disease spread, public health planning, interventions ಅಥವಾ EpiControl AI features ಸಂಬಂಧಿಸಿ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಮತ್ತೆ ಕೇಳಿ.",
    },
    "mr": {
        "math_result": "उत्तर **{result}** आहे.",
        "math_bridge": "तुम्हाला हवे असल्यास, आपण हीच विश्लेषणात्मक पद्धत EpiControl AI मधील outbreak metrics, intervention comparison किंवा SEIR trends कडे वळवू शकतो.",
        "greeting": "नमस्कार. मी सामान्य प्रश्नांची थोडक्यात उत्तरे देऊ शकतो आणि EpiControl AI प्लॅटफॉर्म समजून घेण्यास मदत करू शकतो.",
        "greeting_bridge": "विषयावरच राहायचे असल्यास SEIR modeling, outbreak control strategies, virus mutations, symptom prediction किंवा dashboard interpretation बद्दल विचारा.",
        "identity": "मी EpiControl AI सहाय्यक आहे. मी सामान्य प्रश्नांना थोडक्यात मदत करू शकतो, पण माझे मुख्य काम epidemic simulation, public health decision-making आणि या app च्या features मध्ये मदत करणे आहे.",
        "identity_bridge": "तुम्ही मला outbreak protocols, intervention strategies, SEIR curves किंवा platform कसा वापरायचा याबद्दल विचारू शकता.",
        "python": "Python ही एक high-level programming language आहे. readability आणि मोठ्या library ecosystem मुळे ती web apps, automation, data science, machine learning आणि scientific computing मध्ये मोठ्या प्रमाणावर वापरली जाते.",
        "python_bridge": "या app मध्ये Python, EpiControl AI simulation engine, dashboard logic आणि chatbot integration चालवते.",
        "who": "WHO म्हणजे **World Health Organization**, म्हणजेच जागतिक आरोग्य संघटना, जी international public health, disease surveillance आणि health guidance वर काम करणारी संयुक्त राष्ट्र संस्था आहे.",
        "who_bridge": "हे या app शी थेट संबंधित आहे कारण EpiControl AI simulation आणि planning साठी WHO-style epidemiological concepts आणि verified disease parameters वापरते.",
        "help": "मी झटपट सामान्य मार्गदर्शन आणि या app मधील मुख्य विषय दोन्हींसाठी मदत करू शकतो.",
        "help_bridge": "चांगल्या अनुभवासाठी epidemic spread, policy comparison, AI control mode, mutation behavior किंवा symptom prediction बद्दल विचारा.",
        "generic": "ही एक थोडक्यात सामान्य प्रतिक्रिया आहे: मी विस्तृत प्रश्नांनाही उत्तर देऊ शकतो, पण epidemic intelligence आणि decision support शी जोडल्यास मी अधिक उपयुक्त ठरतो.",
        "generic_bridge": "तुम्हाला हवे असल्यास disease spread, public health planning, interventions किंवा EpiControl AI features च्या संदर्भात प्रश्न पुन्हा विचारा.",
    },
    "ta": {
        "math_result": "பதில் **{result}** ஆகும்.",
        "math_bridge": "நீங்கள் விரும்பினால், இதே பகுப்பாய்வு சிந்தனையை EpiControl AI இல் outbreak metrics, intervention comparison அல்லது SEIR trends உடன் இணைக்கலாம்.",
        "greeting": "வணக்கம். நான் பொது கேள்விகளுக்கு சுருக்கமாக பதிலளிக்கலாம், மேலும் EpiControl AI தளத்தை புரிந்து கொள்ள உதவவும் முடியும்.",
        "greeting_bridge": "தீமையிலேயே இருக்க விரும்பினால் SEIR modeling, outbreak control strategies, virus mutations, symptom prediction அல்லது dashboard interpretation பற்றி கேளுங்கள்.",
        "identity": "நான் EpiControl AI உதவியாளர். நான் பொது கேள்விகளுக்கு சுருக்கமாக உதவ முடியும், ஆனால் epidemic simulation, public health decision-making மற்றும் இந்த app இன் features க்கு ஆதரவு அளிப்பதே என் முக்கிய நோக்கம்.",
        "identity_bridge": "நீங்கள் outbreak protocols, intervention strategies, SEIR curves அல்லது platform ஐ எப்படி பயன்படுத்துவது பற்றி கேட்கலாம்.",
        "python": "Python என்பது ஒரு high-level programming language ஆகும். அதன் readability மற்றும் பெரிய library ecosystem காரணமாக web apps, automation, data science, machine learning மற்றும் scientific computing இல் பரவலாக பயன்படுத்தப்படுகிறது.",
        "python_bridge": "இந்த app இல் Python, EpiControl AI simulation engine, dashboard logic மற்றும் chatbot integration ஐ இயக்குகிறது.",
        "who": "WHO என்பது **World Health Organization**, அதாவது உலக சுகாதார நிறுவனம். இது international public health, disease surveillance மற்றும் health guidance மீது கவனம் செலுத்தும் அமைப்பு.",
        "who_bridge": "இது இந்த app உடன் நேரடியாக தொடர்புடையது, ஏனெனில் EpiControl AI simulation மற்றும் planning க்காக WHO-style epidemiological concepts மற்றும் verified disease parameters ஐ பயன்படுத்துகிறது.",
        "help": "நான் விரைவான பொது வழிகாட்டலும் இந்த app இன் முக்கிய தலைப்புகளுக்கும் உதவ முடியும்.",
        "help_bridge": "சிறந்த அனுபவத்திற்கு epidemic spread, policy comparison, AI control mode, mutation behavior அல்லது symptom prediction பற்றி கேளுங்கள்.",
        "generic": "இது ஒரு சுருக்கமான பொது பதில்: நான் பரந்த கேள்விகளுக்கும் பதில் அளிக்க முடியும், ஆனால் epidemic intelligence மற்றும் decision support உடன் இணைந்தால் நான் அதிக பயனுள்ளவனாக இருப்பேன்.",
        "generic_bridge": "நீங்கள் விரும்பினால் disease spread, public health planning, interventions அல்லது EpiControl AI features தொடர்பாக உங்கள் கேள்வியை மீண்டும் கேளுங்கள்.",
    },
    "te": {
        "math_result": "ఫలితం **{result}**.",
        "math_bridge": "మీకు ఇష్టమైతే, ఇదే విశ్లేషణాత్మక ఆలోచనను EpiControl AI లో outbreak metrics, intervention comparison లేదా SEIR trends తో కలుపుకోవచ్చు.",
        "greeting": "నమస్కారం. నేను సాధారణ ప్రశ్నలకు సంక్షిప్తంగా సమాధానం చెప్పగలను, అలాగే EpiControl AI వేదికను అర్థం చేసుకోవడంలో సహాయపడగలను.",
        "greeting_bridge": "విషయానికి కట్టుబడి ఉండాలనుకుంటే SEIR modeling, outbreak control strategies, virus mutations, symptom prediction లేదా dashboard interpretation గురించి అడగండి.",
        "identity": "నేను EpiControl AI సహాయకుడిని. నేను సాధారణ ప్రశ్నలకు చిన్న సహాయం చేయగలను, కానీ నా ప్రధాన పని epidemic simulation, public health decision-making మరియు ఈ app features కు మద్దతు ఇవ్వడం.",
        "identity_bridge": "మీరు outbreak protocols, intervention strategies, SEIR curves లేదా platform ను ఎలా ఉపయోగించాలో అడగవచ్చు.",
        "python": "Python ఒక high-level programming language. readability మరియు పెద్ద library ecosystem వల్ల ఇది web apps, automation, data science, machine learning మరియు scientific computing లో విస్తృతంగా ఉపయోగించబడుతుంది.",
        "python_bridge": "ఈ app లో Python, EpiControl AI simulation engine, dashboard logic మరియు chatbot integration ను నడిపిస్తుంది.",
        "who": "WHO అంటే **World Health Organization**, అంటే ప్రపంచ ఆరోగ్య సంస్థ. ఇది international public health, disease surveillance మరియు health guidance పై పనిచేస్తుంది.",
        "who_bridge": "ఇది ఈ app కు నేరుగా సంబంధించినది, ఎందుకంటే EpiControl AI simulation మరియు planning కోసం WHO-style epidemiological concepts మరియు verified disease parameters ను ఉపయోగిస్తుంది.",
        "help": "నేను త్వరిత సాధారణ మార్గదర్శకంతో పాటు ఈ app యొక్క ప్రధాన విషయాల్లో కూడా సహాయం చేయగలను.",
        "help_bridge": "మంచి అనుభవం కోసం epidemic spread, policy comparison, AI control mode, mutation behavior లేదా symptom prediction గురించి అడగండి.",
        "generic": "ఇది ఒక సంక్షిప్త సాధారణ సమాధానం: నేను విస్తృతమైన ప్రశ్నలకు కూడా జవాబు ఇవ్వగలను, కానీ epidemic intelligence మరియు decision support తో అనుసంధానించినప్పుడు నేను మరింత ఉపయోగకరంగా ఉంటాను.",
        "generic_bridge": "మీకు ఇష్టమైతే disease spread, public health planning, interventions లేదా EpiControl AI features సందర్భంలో మీ ప్రశ్నను మళ్లీ అడగండి.",
    },
    "gu": {
        "math_result": "પરિણામ **{result}** છે.",
        "math_bridge": "જો તમે ઇચ્છો, તો આપણે આ જ વિશ્લેષણાત્મક વિચારને EpiControl AI માં outbreak metrics, intervention comparison અથવા SEIR trends સાથે જોડીએ.",
        "greeting": "નમસ્તે. હું સામાન્ય પ્રશ્નોના ટૂંકા જવાબ આપી શકું છું અને EpiControl AI પ્લેટફોર્મ સમજવામાં મદદ કરી શકું છું.",
        "greeting_bridge": "જો તમે વિષયમાં જ રહેવા માંગતા હો, તો SEIR modeling, outbreak control strategies, virus mutations, symptom prediction અથવા dashboard interpretation વિશે પૂછો.",
        "identity": "હું EpiControl AI સહાયક છું. હું સામાન્ય પ્રશ્નોમાં ટૂંકી મદદ કરી શકું છું, પરંતુ મારું મુખ્ય કામ epidemic simulation, public health decision-making અને આ app ની features માટે સહાય કરવાનું છે.",
        "identity_bridge": "તમે outbreak protocols, intervention strategies, SEIR curves અથવા platform નો અસરકારક ઉપયોગ કેવી રીતે કરવો તે વિશે પૂછો.",
        "python": "Python એક high-level programming language છે, જે readability અને મોટા library ecosystem ના કારણે web apps, automation, data science, machine learning અને scientific computing માં વ્યાપક રીતે વપરાય છે.",
        "python_bridge": "આ app માં Python, EpiControl AI simulation engine, dashboard logic અને chatbot integration ને ચલાવે છે.",
        "who": "WHO નો અર્થ **World Health Organization** થાય છે, એટલે કે વિશ્વ આરોગ્ય સંસ્થા, જે international public health, disease surveillance અને health guidance પર કામ કરે છે.",
        "who_bridge": "આ સીધું આ app સાથે જોડાયેલું છે, કારણ કે EpiControl AI simulation અને planning માટે WHO-style epidemiological concepts અને verified disease parameters નો ઉપયોગ કરે છે.",
        "help": "હું ઝડપી સામાન્ય માર્ગદર્શન અને આ app ના મુખ્ય વિષયો બંનેમાં મદદ કરી શકું છું.",
        "help_bridge": "વધુ સારું અનુભવ મેળવવા epidemic spread, policy comparison, AI control mode, mutation behavior અથવા symptom prediction વિશે પૂછો.",
        "generic": "આ એક ટૂંકો સામાન્ય જવાબ છે: હું વ્યાપક પ્રશ્નોના જવાબ આપી શકું છું, પરંતુ epidemic intelligence અને decision support સાથે જોડાય ત્યારે હું વધુ ઉપયોગી બનું છું.",
        "generic_bridge": "જો તમે ઇચ્છો, તો disease spread, public health planning, interventions અથવા EpiControl AI features ના સંદર્ભમાં ફરી પ્રશ્ન પૂછો.",
    },
    "ar": {
        "math_result": "النتيجة هي **{result}**.",
        "math_bridge": "إذا أردت، يمكننا ربط هذا التفكير التحليلي مرة أخرى بـ EpiControl AI من خلال مقاييس التفشي أو مقارنة التدخلات أو اتجاهات SEIR.",
        "greeting": "مرحباً. يمكنني الإجابة باختصار عن الأسئلة العامة، كما يمكنني مساعدتك في استكشاف منصة EpiControl AI.",
        "greeting_bridge": "إذا كنت تريد البقاء ضمن موضوع التطبيق، فاسأل عن نمذجة SEIR أو استراتيجيات السيطرة على التفشي أو طفرات الفيروس أو التنبؤ بالأعراض أو كيفية تفسير لوحة المعلومات.",
        "identity": "أنا مساعد EpiControl AI. أستطيع المساعدة بإجابات قصيرة على الأسئلة العامة، لكن هدفي الأساسي هو دعم محاكاة الأوبئة واتخاذ القرار في الصحة العامة وميزات هذا التطبيق.",
        "identity_bridge": "يمكنك سؤالي عن بروتوكولات التفشي أو استراتيجيات التدخل أو منحنيات SEIR أو كيفية استخدام المنصة بفعالية.",
        "python": "Python هي لغة برمجة عالية المستوى تُستخدم على نطاق واسع في تطبيقات الويب والأتمتة وعلوم البيانات والتعلم الآلي والحوسبة العلمية بسبب سهولة قراءتها وتوفر مكتبات كثيرة لها.",
        "python_bridge": "في هذا التطبيق، تشغل Python محرك المحاكاة في EpiControl AI ومنطق لوحة المعلومات وتكامل روبوت الدردشة.",
        "who": "WHO تعني **World Health Organization**، أي منظمة الصحة العالمية، وهي الجهة التابعة للأمم المتحدة المختصة بالصحة العامة الدولية وترصد الأمراض والإرشاد الصحي.",
        "who_bridge": "وهذا يرتبط مباشرة بهذا التطبيق لأن EpiControl AI يستخدم مفاهيم وبائية على نمط WHO ومعلمات أمراض موثقة لأغراض المحاكاة والتخطيط.",
        "help": "يمكنني المساعدة في الإرشاد العام السريع وكذلك في الموضوعات الأساسية داخل هذا التطبيق.",
        "help_bridge": "لأفضل تجربة هنا، اسأل عن انتشار المرض أو مقارنة السياسات أو وضع التحكم بالذكاء الاصطناعي أو سلوك الطفرات أو التنبؤ بالأعراض.",
        "generic": "إليك إجابة عامة مختصرة: أستطيع عادةً الرد على الأسئلة الواسعة، لكنني أكون أكثر فائدة عندما يرتبط السؤال بذكاء الأوبئة ودعم القرار.",
        "generic_bridge": "إذا أردت، أعد طرح سؤالك في سياق انتشار الأمراض أو تخطيط الصحة العامة أو التدخلات أو ميزات EpiControl AI.",
    },
    "ja": {
        "math_result": "結果は **{result}** です。",
        "math_bridge": "必要であれば、この分析的な考え方を EpiControl AI に戻して、流行指標、介入比較、SEIR トレンドに結び付けることができます。",
        "greeting": "こんにちは。一般的な質問に短く答えることもできますし、EpiControl AI プラットフォームの案内もできます。",
        "greeting_bridge": "テーマに戻したい場合は、SEIR モデリング、流行対策、ウイルス変異、症状予測、ダッシュボードの見方について聞いてください。",
        "identity": "私は EpiControl AI アシスタントです。一般的な質問にも短く答えられますが、主な役割は流行シミュレーション、公衆衛生の意思決定、このアプリの機能支援です。",
        "identity_bridge": "流行対応プロトコル、介入戦略、SEIR 曲線、プラットフォームの使い方について質問できます。",
        "python": "Python は高水準のプログラミング言語で、読みやすさと豊富なライブラリエコシステムにより、Web アプリ、自動化、データサイエンス、機械学習、科学技術計算で広く使われています。",
        "python_bridge": "このアプリでは、Python が EpiControl AI のシミュレーションエンジン、ダッシュボードロジック、チャットボット連携を動かしています。",
        "who": "WHO は **World Health Organization**、つまり世界保健機関のことです。国際公衆衛生、疾病監視、健康指針を担う国連機関です。",
        "who_bridge": "これはこのアプリと直接関係しており、EpiControl AI はシミュレーションや計画に WHO 型の疫学概念と検証済みの疾患パラメータを使っています。",
        "help": "一般的な短い案内と、このアプリの主要テーマの両方を手伝えます。",
        "help_bridge": "より良い体験のために、感染拡大、政策比較、AI 制御モード、変異挙動、症状予測について質問してください。",
        "generic": "簡単な一般回答です。幅広い質問にも答えられますが、流行知能や意思決定支援に結び付く質問のときに最も役立ちます。",
        "generic_bridge": "必要であれば、感染拡大、公衆衛生計画、介入、EpiControl AI の機能に関連付けて質問し直してください。",
    },
    "ko": {
        "math_result": "결과는 **{result}** 입니다.",
        "math_bridge": "원하시면 이 분석적 사고를 다시 EpiControl AI 와 연결해서 유행 지표, 개입 비교, SEIR 추세를 살펴볼 수 있습니다.",
        "greeting": "안녕하세요. 일반 질문에 짧게 답할 수 있고 EpiControl AI 플랫폼을 이해하는 데도 도움을 드릴 수 있습니다.",
        "greeting_bridge": "주제에 맞게 이어가고 싶다면 SEIR 모델링, 유행 통제 전략, 바이러스 변이, 증상 예측, 대시보드 해석에 대해 물어보세요.",
        "identity": "저는 EpiControl AI 도우미입니다. 일반 질문에도 짧게 답할 수 있지만, 주된 목적은 유행 시뮬레이션, 공중보건 의사결정, 그리고 이 앱의 기능을 지원하는 것입니다.",
        "identity_bridge": "유행 대응 프로토콜, 개입 전략, SEIR 곡선, 플랫폼 사용법에 대해 질문할 수 있습니다.",
        "python": "Python 은 가독성이 높고 라이브러리 생태계가 풍부한 고급 프로그래밍 언어로, 웹 앱, 자동화, 데이터 과학, 머신러닝, 과학 계산에 널리 사용됩니다.",
        "python_bridge": "이 앱에서는 Python 이 EpiControl AI 시뮬레이션 엔진, 대시보드 로직, 챗봇 통합을 구동합니다.",
        "who": "WHO 는 **World Health Organization**, 즉 세계보건기구를 의미하며 국제 공중보건, 질병 감시, 건강 지침을 담당하는 기관입니다.",
        "who_bridge": "이는 이 앱과 직접 연결되는데, EpiControl AI 가 시뮬레이션과 계획에 WHO 방식의 역학 개념과 검증된 질병 파라미터를 사용하기 때문입니다.",
        "help": "빠른 일반 안내와 이 앱의 핵심 주제 모두를 도와드릴 수 있습니다.",
        "help_bridge": "더 좋은 경험을 위해 질병 확산, 정책 비교, AI 제어 모드, 변이 행동, 증상 예측에 대해 물어보세요.",
        "generic": "짧은 일반 답변입니다. 저는 폭넓은 질문에도 답할 수 있지만, 유행 인텔리전스와 의사결정 지원과 연결될 때 가장 유용합니다.",
        "generic_bridge": "원하시면 질병 확산, 공중보건 계획, 개입, 또는 EpiControl AI 기능과 관련해 다시 질문해 주세요.",
    },
    "pt": {
        "math_result": "O resultado e **{result}**.",
        "math_bridge": "Se quiser, podemos trazer esse mesmo raciocinio analitico de volta ao EpiControl AI explorando metricas de surtos, comparacao de intervencoes ou tendencias SEIR.",
        "greeting": "Ola. Posso responder perguntas gerais de forma breve e tambem ajudar voce a explorar a plataforma EpiControl AI.",
        "greeting_bridge": "Se quiser manter o foco no tema, pergunte sobre modelagem SEIR, estrategias de controle de surtos, mutacoes de virus, previsao de sintomas ou interpretacao do painel.",
        "identity": "Sou o assistente do EpiControl AI. Posso ajudar com perguntas gerais de forma curta, mas fui projetado principalmente para apoiar simulacao epidemica, tomada de decisao em saude publica e os recursos deste app.",
        "identity_bridge": "Voce pode me perguntar sobre protocolos de surtos, estrategias de intervencao, curvas SEIR ou como usar a plataforma de forma eficaz.",
        "python": "Python e uma linguagem de programacao de alto nivel amplamente usada para aplicativos web, automacao, ciencia de dados, aprendizado de maquina e computacao cientifica por causa de sua legibilidade e grande ecossistema de bibliotecas.",
        "python_bridge": "Neste app, Python alimenta o mecanismo de simulacao do EpiControl AI, a logica do painel e a integracao do chatbot.",
        "who": "WHO significa **World Health Organization**; em portugues, Organizacao Mundial da Saude, a agencia das Nacoes Unidas focada em saude publica internacional, vigilancia de doencas e orientacao em saude.",
        "who_bridge": "Isso se conecta diretamente com este app porque o EpiControl AI usa conceitos epidemiologicos no estilo WHO e parametros de doencas verificados para simulacao e planejamento.",
        "help": "Posso ajudar tanto com orientacao geral rapida quanto com os principais temas deste app.",
        "help_bridge": "Para a melhor experiencia aqui, pergunte sobre propagacao epidemica, comparacao de politicas, modo de controle por IA, comportamento de mutacoes ou previsao de sintomas.",
        "generic": "Aqui vai uma resposta geral breve: normalmente posso responder perguntas amplas, mas este assistente e mais util quando conecta a informacao com inteligencia epidemica e apoio a decisao.",
        "generic_bridge": "Se quiser, faca sua pergunta novamente em relacao a propagacao de doencas, planejamento de saude publica, intervencoes ou recursos do EpiControl AI.",
    },
    "ru": {
        "math_result": "Результат: **{result}**.",
        "math_bridge": "Если хотите, мы можем связать этот аналитический подход с EpiControl AI, например с метриками вспышки, сравнением вмешательств или трендами SEIR.",
        "greeting": "Здравствуйте. Я могу кратко отвечать на общие вопросы и также помочь вам разобраться с платформой EpiControl AI.",
        "greeting_bridge": "Если хотите остаться в теме приложения, спросите о моделировании SEIR, стратегиях контроля вспышек, мутациях вируса, прогнозировании симптомов или интерпретации панели.",
        "identity": "Я помощник EpiControl AI. Я могу кратко помогать с общими вопросами, но моя основная задача связана с моделированием эпидемий, поддержкой решений в общественном здравоохранении и функциями этого приложения.",
        "identity_bridge": "Вы можете спросить меня о протоколах вспышек, стратегиях вмешательства, кривых SEIR или о том, как эффективно использовать платформу.",
        "python": "Python — это высокоуровневый язык программирования, который широко используется для веб-приложений, автоматизации, data science, машинного обучения и научных вычислений благодаря читаемости и большой экосистеме библиотек.",
        "python_bridge": "В этом приложении Python обеспечивает работу симуляционного движка EpiControl AI, логики панели и интеграции чат-бота.",
        "who": "WHO означает **World Health Organization**, то есть Всемирная организация здравоохранения, международная структура ООН по общественному здравоохранению, мониторингу заболеваний и медицинским рекомендациям.",
        "who_bridge": "Это напрямую связано с приложением, потому что EpiControl AI использует эпидемиологические концепции в стиле WHO и проверенные параметры заболеваний для моделирования и планирования.",
        "help": "Я могу помочь как с быстрыми общими подсказками, так и с основными темами этого приложения.",
        "help_bridge": "Для лучшего опыта здесь спросите о распространении заболеваний, сравнении политик, режиме AI control, поведении мутаций или прогнозировании симптомов.",
        "generic": "Вот краткий общий ответ: я обычно могу отвечать и на широкие вопросы, но наиболее полезен, когда информация связана с эпидемической аналитикой и поддержкой решений.",
        "generic_bridge": "Если хотите, задайте вопрос снова в контексте распространения болезней, планирования здравоохранения, вмешательств или функций EpiControl AI.",
    },
}

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
            "keywords": ["world health organization", "who database", "disease", "pathogen", "covid", "measles", "flu", "ebola"],
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
        self.bedrock_client = None
        try:
            self.bedrock_client = boto3.client(
                service_name="bedrock-runtime",
                region_name=BEDROCK_REGION,
            )
        except Exception:
            self.bedrock_client = None

    def _build_system_prompt(self) -> str:
        """Build a system prompt with knowledge base context"""
        lang_name = LANGUAGE_NAMES.get(self.language, "English")

        kb_summary = ""
        for topic, content in self.knowledge_base.items():
            if "answer" in content:
                kb_summary += f"\n--- {topic} ---\n{content['answer']}\n"

        return f"""You are the EpiControl AI Assistant, a helpful and knowledgeable chatbot embedded in the EpiControl AI epidemic simulation platform.

Respond in {lang_name}. Be concise but thorough. Use emojis where appropriate to make responses engaging.

Key knowledge about the platform:
{kb_summary}

Guidelines:
- Always answer the user's actual question directly.
- Always respond in {lang_name}. The selected app language is authoritative.
- Answer questions about SEIR models, epidemic simulation, visualizations, interventions, mutations, AI mode, and related public health topics with strong detail.
- If the user asks something outside the scope of EpiControl AI, still give a short and useful answer first, then gently connect the conversation back to epidemic intelligence, outbreak response, public health, simulation, or the features of this app.
- Never say that you can only answer in-scope questions.
- For out-of-context questions, keep the off-topic answer brief, then add a bridging sentence that brings attention back to the website or app theme.
- Keep responses well-formatted with markdown (bold, bullet points, etc.).
- Be friendly and educational.
- If you don't know something specific about the platform, use your general epidemiology knowledge to give a helpful answer.
- Do not switch to another language unless the user explicitly asks to change the answer language.
- You support 16 languages: English, Spanish, French, German, Hindi, Chinese, Kannada, Marathi, Tamil, Telugu, Gujarati, Arabic, Japanese, Korean, Portuguese, and Russian.
"""

    def _fallback_messages(self) -> dict:
        """Return localized fallback copy for the selected language."""
        return LOCALIZED_FALLBACKS.get(self.language, LOCALIZED_FALLBACKS["en"])

    def _compose_fallback(self, key: str, **kwargs) -> str:
        """Compose a localized fallback response with a theme bridge."""
        messages = self._fallback_messages()
        body = messages.get(key, LOCALIZED_FALLBACKS["en"][key]).format(**kwargs)
        bridge_key = "math_bridge" if key == "math_result" else f"{key}_bridge"
        bridge = messages.get(bridge_key, LOCALIZED_FALLBACKS["en"].get(bridge_key, ""))
        return f"{body}\n\n{bridge}" if bridge else body

    def _build_bedrock_messages(self) -> List[dict]:
        """Convert local conversation history into Bedrock Converse message format."""
        return [
            {"role": role, "content": [{"text": message}]}
            for role, message in self.conversation_history[-20:]
        ]

    def _call_bedrock(self) -> str:
        """Call AWS Bedrock Converse for a multi-turn response."""
        response = self.bedrock_client.converse(
            modelId=BEDROCK_MODEL_ID,
            system=[{"text": self._build_system_prompt()}],
            messages=self._build_bedrock_messages(),
            inferenceConfig={
                "temperature": BEDROCK_TEMPERATURE,
                "maxTokens": BEDROCK_MAX_TOKENS,
            },
            additionalModelRequestFields={"top_k": BEDROCK_TOP_K},
        )
        return response["output"]["message"]["content"][0]["text"]

    def _keyword_matches_query(self, keyword: str, query: str) -> bool:
        """Match keywords conservatively to avoid false positives from substrings."""
        normalized_keyword = keyword.strip().lower()
        normalized_query = query.strip().lower()

        if not normalized_keyword:
            return False

        if " " in normalized_keyword:
            pattern = r"\b" + re.escape(normalized_keyword).replace(r"\ ", r"\s+") + r"\b"
            return re.search(pattern, normalized_query) is not None

        return re.search(r"\b" + re.escape(normalized_keyword) + r"\b", normalized_query) is not None
    
    def find_best_match(self, user_query: str) -> Tuple[str, str, int]:
        """Find best knowledge base match for user question (fallback)."""
        query_lower = user_query.lower()
        best_match = ("general", 0)
        
        for topic, content in self.knowledge_base.items():
            match_score = 0
            keywords = content.get("keywords", [])
            
            for keyword in keywords:
                if self._keyword_matches_query(keyword, query_lower):
                    match_score += 1
            
            if match_score > best_match[1]:
                best_match = (topic, match_score)
        
        topic = best_match[0]
        answer = self.knowledge_base[topic].get("answer", self.knowledge_base["general"]["answer"])
        return topic, answer, best_match[1]

    def _build_soft_redirect_fallback(self, user_message: str) -> str:
        """Provide a brief answer for broad questions, then guide back to the app theme."""
        message = user_message.strip().lower()

        if re.fullmatch(r"[0-9\s\+\-\*\/\(\)\.]+", message):
            try:
                result = eval(message, {"__builtins__": {}}, {})
                return self._compose_fallback("math_result", result=result)
            except Exception:
                pass

        if any(word in message for word in ["hello", "hi", "hey", "namaste", "bonjour", "hola"]):
            return self._compose_fallback("greeting")

        if "who are you" in message or "what are you" in message:
            return self._compose_fallback("identity")

        if "python" in message:
            return self._compose_fallback("python")

        if "what is who" in message or "who full form" in message or "world health organization" in message:
            return self._compose_fallback("who")

        if "help" in message:
            return self._compose_fallback("help")

        return self._compose_fallback("generic")
    
    def respond(self, user_message: str) -> str:
        """Generate a response using Bedrock Converse, with keyword fallback."""
        cleaned_message = user_message.strip()
        if not cleaned_message:
            return ""

        self.conversation_history.append(("user", cleaned_message))

        if self.bedrock_client:
            try:
                response = self._call_bedrock()
                self.conversation_history.append(("assistant", response))
                return response
            except Exception:
                pass

        # Fallback to keyword matching
        topic, response, score = self.find_best_match(cleaned_message)
        if score == 0:
            response = self._build_soft_redirect_fallback(cleaned_message)
        self.conversation_history.append(("assistant", response))
        return response
    
    def set_language(self, language: str):
        """Change language"""
        if language == self.language:
            return
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

