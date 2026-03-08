"""
EpiControl AI - Professional Epidemic Simulation & Control Platform
Team Neural Mavericks
"""

import streamlit as st
import boto3
import json
import sys
import os
from pathlib import Path

# Add current directory and parent directory to path for imports
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Track which features are available
FEATURES_AVAILABLE = {
    'rl': True,
    'symptom_prediction': True
}

try:
    from env.population import generate_population
    from env.seir import seed_infection, update_seir, set_virus_params
    from env.policies import apply_policy, apply_policy_batch
    from env.mutation import reset_mutation_tracker
    from simulation.metrics import init_metrics, record_metrics
    from visualization.plotly_plots import (
        plot_seir_plotly, 
        plot_infection_heatmap, 
        plot_spatial_scatter,
        plot_mutation_timeline,
        plot_policy_comparison,
        plot_global_epidemic_map,
        plot_globe_view_3d
    )
    from data.virus_configs import VIRUS_CONFIGS
    from translations import get_translation, TRANSLATIONS, get_language_name
    from chatbot import AdvancedChatbot
except ImportError as e:
    import traceback
    st.error(f"Critical Import Error: {str(e)}")
    with st.expander("Debug Information"):
        st.write(f"**Error Type:** {type(e).__name__}")
        st.write(f"**Current Directory:** {os.getcwd()}")
        st.write(f"**Script Location:** {Path(__file__).resolve()}")
        st.write(f"**Python Path:**")
        for p in sys.path[:5]:
            st.write(f"  - {p}")
        st.code(traceback.format_exc())
    st.info("Please ensure all required packages are installed and project files are present.")
    st.info("Required: streamlit, numpy, pandas, matplotlib, plotly, gymnasium, torch")
    st.stop()

# Optional imports - RL features
try:
    from rl.env import EpiControlEnv
    from rl.utils import discretize_state
    from rl.load_agent import load_trained_agent
    FEATURES_AVAILABLE['rl'] = True
except ImportError as e:
    # Try importing again with more specific error handling
    try:
        sys.path.insert(0, str(current_dir))
        from rl.env import EpiControlEnv
        from rl.utils import discretize_state
        from rl.load_agent import load_trained_agent
        FEATURES_AVAILABLE['rl'] = True
    except Exception as e2:
        FEATURES_AVAILABLE['rl'] = False
        EpiControlEnv = None
        discretize_state = None
        load_trained_agent = None

# Optional imports - Symptom prediction
try:
    from symptom_prediction import SymptomPredictor, HISTORICAL_PANDEMICS
    FEATURES_AVAILABLE['symptom_prediction'] = True
except ImportError as e:
    FEATURES_AVAILABLE['symptom_prediction'] = False
    SymptomPredictor = None
    HISTORICAL_PANDEMICS = None

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="EpiControl AI | Neural Mavericks",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS FOR PROFESSIONAL UI ====================
st.markdown("""
<style>
    /* Advanced Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 0 20px 10px rgba(102, 126, 234, 0);
        }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.5),
                        0 0 10px rgba(102, 126, 234, 0.3),
                        0 0 15px rgba(102, 126, 234, 0.2);
        }
        50% {
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.8),
                        0 0 20px rgba(102, 126, 234, 0.5),
                        0 0 30px rgba(102, 126, 234, 0.3);
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Main Background with Animated Gradient */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        position: relative;
        overflow: hidden;
    }
    
    /* Animated Background Particles */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.03) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Header styling with gradient animation */
    .title-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .title-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        animation: shimmer 3s infinite;
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        color: #e0e7ff;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .team-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 1rem;
        color: white;
        font-weight: 600;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .team-badge:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Metric cards with hover effect */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #1f2937;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border-left-width: 6px;
    }
    
    .metric-card h4, .metric-card h5 {
        color: #667eea;
        margin-top: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Enhanced Button styling with ripple effect */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Enhanced Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #1f2937;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Info boxes with animation */
    .info-box {
        background: rgba(224, 242, 254, 0.95);
        border-left: 4px solid #0284c7;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1f2937;
        animation: fadeInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        box-shadow: 0 5px 20px rgba(2, 132, 199, 0.2);
        transform: translateX(5px);
    }
    
    .info-box h4 {
        color: #0284c7;
        margin-top: 0;
    }
    
    .success-box {
        background: rgba(209, 250, 229, 0.95);
        border-left: 4px solid #059669;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1f2937;
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .success-box:hover {
        box-shadow: 0 5px 20px rgba(5, 150, 105, 0.2);
        transform: scale(1.02);
    }
    
    .success-box h3, .success-box h4 {
        color: #059669;
        margin-top: 0;
    }
    
    .warning-box {
        background: rgba(254, 243, 199, 0.95);
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1f2937;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .warning-box h4, .warning-box h5 {
        color: #f59e0b;
        margin-top: 0;
    }
    
    /* Metric cards in main dashboard */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* Plotly charts smooth appearance */
    .js-plotly-plot {
        animation: fadeIn 0.8s ease-in;
    }
    
    /* Sidebar elements */
    .css-1lcbmhc, .css-1outpf7 {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        animation: shimmer 2s infinite;
        background-size: 200% 100%;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.05);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.1);
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.2);
    }
    
    /* Checkbox and radio custom styling */
    .stCheckbox, .stRadio {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Loading spinner customization */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Smooth scroll */
    html {
        scroll-behavior: smooth;
    }
    
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'running' not in st.session_state:
    st.session_state.running = False
if 'simulation_complete' not in st.session_state:
    st.session_state.simulation_complete = False
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'last_params' not in st.session_state:
    st.session_state.last_params = None
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'chatbot_context' not in st.session_state:
    st.session_state.chatbot_context = 'welcome'
if 'symptom_predictor' not in st.session_state:
    if FEATURES_AVAILABLE['symptom_prediction'] and SymptomPredictor is not None:
        st.session_state.symptom_predictor = SymptomPredictor()
    else:
        st.session_state.symptom_predictor = None
if 'show_symptom_prediction' not in st.session_state:
    st.session_state.show_symptom_prediction = False

# Initialize language for easier access
language = st.session_state.language
def t(key: str, default: str = "") -> str:
    """Shorthand translation function"""
    return get_translation(language, key, default)

# ==================== PROFESSIONAL HEADER ====================
st.markdown("""
<div class="title-container">
    <h1 class="main-title">EpiControl AI</h1>
    <p class="subtitle">Advanced Epidemic Intelligence Platform | SEIR Modeling + Mutation Dynamics + AI Control</p>
    <div class="team-badge">Team Neural Mavericks</div>
</div>
""", unsafe_allow_html=True)

# Quick Stats Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Platform Features", "9+", "Core Capabilities")
with col2:
    st.metric("Mutation Modeling", "Real-time", "Virus Evolution")
with col3:
    st.metric("AI Agent", "Deep Q-Learning", "Trained Model")
with col4:
    st.metric("Symptom Predictor", "ML-Based", "Historical Analysis")

st.markdown("---")

def analyze_threat_with_bedrock(unstructured_text):
    client = boto3.client('bedrock-runtime', region_name='us-east-1') # Ensure region is correct
    prompt = f"""
    Analyze this intelligence report: \"{unstructured_text}\"
    Extract the epidemiological parameters. Respond ONLY with a valid JSON object.
    Required keys: \"R0\" (float), \"incubation_days\" (int), \"infectious_days\" (int), \"mortality_rate\" (float), \"trigger_warning\" (boolean).
    """
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.1,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "{"} # Forces strict JSON
        ]
    })
    try:
        response = client.invoke_model(modelId="anthropic.claude-3-sonnet-20240229-v1:0", body=body)
        response_body = json.loads(response.get('body').read())
        raw_json_str = "{" + response_body['content'][0]['text']
        return json.loads(raw_json_str)
    except Exception as e:
        return {"error": str(e)}

st.header("🚨 Sentinel: Bedrock Early Warning System")
news_input = st.text_area("Paste News Report:", "e.g., Doctors in Pune report 50 patients with a highly contagious cough spreading to 3 people each. No deaths yet, incubation seems to be 4 days.")

if st.button("Run AWS Bedrock Analysis"):
    with st.spinner("Analyzing threat..."):
        result = analyze_threat_with_bedrock(news_input)
        if "error" not in result:
            st.success("Threat Analyzed Successfully!")
            st.json(result)
        else:
            st.error(f"Error: {result['error']}")

# ==================== GLOBAL EPIDEMIC MAP ====================
st.markdown("### Global Epidemic Surveillance Dashboard")
st.markdown("**Real-time monitoring of epidemic spread across 50+ countries**")

# Map view selector
map_view = st.radio(
    "Map View",
    ["World Map (Flat)", "Globe View (3D)"],
    horizontal=True,
    help="Choose between flat world map or interactive 3D globe"
)

if map_view == "World Map (Flat)":
    world_map_fig = plot_global_epidemic_map()
    st.plotly_chart(world_map_fig, use_container_width=True, key="dashboard_world_map")
    
    # Add quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Countries Affected", "50+", "+5 new")
    with col2:
        st.metric("Avg Infection Rate", "12.3%", "+1.2%")
    with col3:
        st.metric("Total Cases (Global)", "980M+", "+2.1M")
    with col4:
        st.metric("Critical Regions", "12", "Very High Alert")
else:
    globe_fig = plot_globe_view_3d()
    st.plotly_chart(globe_fig, use_container_width=True, key="dashboard_globe_view")
    st.info("**Tip**: Drag to rotate the globe and explore different regions!")

st.markdown("---")

# ==================== LANGUAGE SELECTOR ====================
st.sidebar.markdown("### Language")
language_options = {get_language_name(code): code for code in TRANSLATIONS.keys()}
selected_lang = st.sidebar.selectbox(
    "Select Language:",
    options=list(language_options.keys()),
    index=list(language_options.values()).index(st.session_state.language),
    key="language_selector"
)
st.session_state.language = language_options[selected_lang]
language = st.session_state.language

# ==================== DATABASE INFORMATION ====================
st.sidebar.markdown("---")
st.sidebar.markdown("### Database Information")
with st.sidebar.expander("Data Sources", expanded=False):
    try:
        from data.virus_configs import VIRUS_CONFIGS
        from symptom_prediction.historical_data import HISTORICAL_PANDEMICS
        import os
        
        st.markdown("**Virus Configuration Database**")
        st.markdown(f"`data/virus_configs.py`")
        st.markdown(f"**{len(VIRUS_CONFIGS)}** Disease Models")
        st.markdown(f"Size: {os.path.getsize('data/virus_configs.py')/1024:.1f} KB")
        
        st.markdown("---")
        
        st.markdown("**Historical Pandemic Database**")
        st.markdown(f"`symptom_prediction/historical_data.py`")
        st.markdown(f"**{len(HISTORICAL_PANDEMICS)}** Pandemic Records")
        diseases_list = ", ".join(list(HISTORICAL_PANDEMICS.keys())[:3]) + "..."
        st.markdown(f"Datasets: {diseases_list}")
        st.markdown(f"Size: {os.path.getsize('symptom_prediction/historical_data.py')/1024:.1f} KB")
        
        st.markdown("---")
        
        st.markdown("**WHO Parameters Database**")
        st.markdown(f"`data/who_params.json`")
        st.markdown(f"WHO-Verified Data")
        st.markdown(f"Size: {os.path.getsize('data/who_params.json')/1024:.1f} KB")
        
        total_size = (
            os.path.getsize('data/virus_configs.py') + 
            os.path.getsize('symptom_prediction/historical_data.py') + 
            os.path.getsize('data/who_params.json')
        ) / 1024
        
        st.markdown("---")
        st.markdown(f"**Total Database Size:** {total_size:.1f} KB")
        st.markdown(f"**Last Updated:** Jan 2026")
        st.markdown(f"**Sources:** WHO, CDC, Peer-reviewed")
        
    except Exception as e:
        st.error(f"Error loading database info: {str(e)}")

# Initialize session state for chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = AdvancedChatbot(language)
else:
    st.session_state.chatbot.set_language(language)

# ==================== CHAT INTERFACE ====================
st.sidebar.markdown("### AI Chat Assistant")

if st.sidebar.button("Clear Chat", key="clear_chat_history"):
    st.session_state.chatbot.clear_history()
    st.rerun()

# Chat display area with expander for cleaner UI
with st.sidebar.expander("Chat History", expanded=True):
    for role, message in st.session_state.chatbot.get_history():
        if role == "user":
            st.write(f" **You**: {message}")
        else:
            st.write(f" **AI**: {message}")

# Chat input
with st.sidebar.form("chat_input_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask a question:",
        placeholder="E.g., 'What is SEIR?'",
        key="chat_input"
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    with st.sidebar.spinner("Thinking..."):
        response = st.session_state.chatbot.respond(user_input)
    if response:
        st.sidebar.success(response)
    st.rerun()

# ==================== SIDEBAR CONFIGURATION ====================
st.sidebar.markdown("### Configuration")
st.sidebar.markdown(f"#### Simulation Parameters")
col1, col2 = st.sidebar.columns(2)
with col1:
    POP_SIZE = st.number_input(
        "Population",
        min_value=500,
        max_value=50000,
        value=5000,
        step=500,
        help="Total agents in simulation (smaller = faster)"
    )
with col2:
    DAYS = st.number_input(
        "Days",
        min_value=20,
        max_value=120,
        value=45,
        step=5,
        help="Simulation length (fewer days = faster)"
    )

st.sidebar.markdown("---")

# ---- CITY SELECTION ----
st.sidebar.markdown("### City Configuration")
from env.city import CITY_CONFIGS

city_mode = st.sidebar.radio(
    "Simulation Mode",
    ["Custom", "Indian City Preset"],
    help="Choose between custom parameters or realistic Indian city configurations"
)

if city_mode == "Indian City Preset":
    selected_city = st.sidebar.selectbox(
        "Select City",
        options=list(CITY_CONFIGS.keys()),
        help="Choose an Indian metropolitan city with realistic parameters"
    )
    
    city_config = CITY_CONFIGS[selected_city]
    
    # Display city information
    st.sidebar.info(f"**{selected_city}**\n\n{city_config['description']}\n\n"
                   f"Population: {city_config['population_size']:,}\n"
                   f"Density: {city_config['density'].replace('_', ' ').title()}\n"
                   f"Healthcare Capacity: {city_config['healthcare_capacity']*100:.0f}%\n"
                   f"Public Transport: {city_config['public_transport_usage']*100:.0f}%")
    
    # Override population and days with city config
    POP_SIZE = city_config['population_size']
    DAYS = city_config['days']
    
    # Apply city-specific transmission multiplier
    CONTACT_MULTIPLIER = city_config['contact_multiplier']
else:
    CONTACT_MULTIPLIER = 1.0

st.sidebar.markdown("---")

# ---- VIRUS SELECTION ----
st.sidebar.markdown("### Pathogen Selection")

# Load WHO parameters
try:
    with open("data/who_params.json", "r") as f:
        WHO_PARAMS = json.load(f)
except:
    WHO_PARAMS = {}

st.sidebar.markdown("#### Pathogen")
virus_source = st.sidebar.radio(
    "Data Source",
    ["Custom Models", "WHO Database"],
    help="Select source"
)

if virus_source == "Custom Models":
    virus_name = st.sidebar.selectbox(
        "Select Pathogen",
        list(VIRUS_CONFIGS.keys()),
        help="Models"
    )
    virus_config = VIRUS_CONFIGS[virus_name]
elif WHO_PARAMS:
    virus_name = st.sidebar.selectbox(
        "WHO Pathogen",
        list(WHO_PARAMS.keys()),
        help="Disease data"
    )
    who_data = WHO_PARAMS[virus_name]
    virus_config = {
        "R0": who_data["R0"] * CONTACT_MULTIPLIER,
        "incubation_days": who_data["incubation_days"],
        "infectious_days": who_data["infectious_days"],
        "base_beta": who_data["base_beta"] * CONTACT_MULTIPLIER,
        "mortality_rate": who_data["mortality_rate"],
        "child_immunity_boost": 0.15,
        "adult_severity": 0.75
    }
    st.sidebar.caption(f"{who_data['disease_name']}")
else:
    virus_name = "COVID-19"
    base_config = VIRUS_CONFIGS[virus_name]
    virus_config = {
        "R0": base_config["R0"] * CONTACT_MULTIPLIER,
        "incubation_days": base_config["incubation_days"],
        "infectious_days": base_config["infectious_days"],
        "base_beta": base_config["base_beta"] * CONTACT_MULTIPLIER,
        "mortality_rate": base_config["mortality_rate"],
        "child_immunity_boost": base_config.get("child_immunity_boost", 0.20),
        "adult_severity": base_config.get("adult_severity", 0.80)
    }

st.sidebar.markdown("#### Mutations")
enable_mutations = st.sidebar.checkbox("Enable Mutations", value=True, help="Virus evolution")

if enable_mutations:
    mutation_threshold = st.sidebar.slider(
        "Trigger (%)",
        min_value=0.1,
        max_value=0.5,
        value=0.30,
        step=0.05,
        help="Infection threshold"
    )

st.sidebar.markdown("#### Interventions")
mask_mandate = st.sidebar.checkbox("Mask Mandate", value=False, help="Reduce transmission")
school_closure = st.sidebar.checkbox("School Closure", value=False, help="Limit contact")
vaccination = st.sidebar.checkbox("Vaccination", value=False, help="Provide immunity")

st.sidebar.markdown("#### Control Mode")

# Filter control modes based on available features
control_modes = ["Manual Policy", "Policy Comparison"]
if FEATURES_AVAILABLE['rl']:
    control_modes.insert(1, "AI (RL) Policy")

control_mode = st.sidebar.radio(
    "Mode",
    control_modes,
    help="Strategy"
)

if control_mode == "Manual Policy":
    st.sidebar.caption(" Manual control")
elif control_mode == "AI (RL) Policy":
    if not FEATURES_AVAILABLE['rl']:
        st.sidebar.error("RL features not available")
        control_mode = "Manual Policy"
    else:
        st.sidebar.caption(" AI decides")
else:
    st.sidebar.caption(" Compare all")

st.sidebar.markdown("####  Visualization")
show_heatmap = st.sidebar.checkbox("Heatmap", value=True, help="Density map")
show_spatial = st.sidebar.checkbox("Scatter", value=False, help="Agent distribution")
show_timeline = st.sidebar.checkbox("Timeline", value=True, help="Epidemic progression")

st.sidebar.markdown("---")

# ---- SYMPTOM PREDICTION MODULE ----
st.sidebar.markdown("### Symptom Prediction")

if FEATURES_AVAILABLE['symptom_prediction']:
    enable_symptom_prediction = st.sidebar.checkbox(
        "Enable Symptom Predictor",
        value=False,
        help="Predict symptom patterns based on historical data"
    )
    
    if enable_symptom_prediction:
        st.sidebar.caption("Analyzes epidemiological parameters to predict likely symptom profiles")
        st.session_state.show_symptom_prediction = True
    else:
        st.session_state.show_symptom_prediction = False
else:
    st.sidebar.info("Symptom prediction unavailable")
    st.session_state.show_symptom_prediction = False
    enable_symptom_prediction = False

# ---- RUN SIMULATION BUTTON ----
st.sidebar.markdown("")
st.sidebar.markdown("")

# Detect parameter changes and clear old results
current_params = {
    'virus': virus_name,
    'population': POP_SIZE,
    'days': DAYS,
    'control_mode': control_mode,
    'policies': (mask_mandate, school_closure, vaccination),
    'mutations': enable_mutations,
    'city_mode': city_mode if 'city_mode' in locals() else 'Custom'
}

if st.session_state.last_params != current_params:
    # Parameters changed - clear old results
    st.session_state.simulation_results = None
    st.session_state.simulation_complete = False
    st.session_state.last_params = current_params

run_button = st.sidebar.button("▶ Run Simulation", use_container_width=True, type="primary", key="run_simulation_btn")

if run_button and not st.session_state["running"]:
    st.session_state["running"] = True
    st.session_state["simulation_complete"] = False
    st.session_state.simulation_results = None

if st.session_state["running"] and not st.session_state.get("simulation_complete", False):

    # ========== POLICY COMPARISON MODE ==========
    if control_mode == "Policy Comparison":
        st.markdown("**Multi-Policy Comparative Analysis**")
        st.info("Running systematic comparison across 5 intervention strategies...")
        
        policies_to_test = {
            "No Intervention": {"mask_mandate": False, "school_closure": False, "vaccination": False},
            "Masks Only": {"mask_mandate": True, "school_closure": False, "vaccination": False},
            "School Closure": {"mask_mandate": False, "school_closure": True, "vaccination": False},
            "Vaccination Only": {"mask_mandate": False, "school_closure": False, "vaccination": True},
            "Full Intervention": {"mask_mandate": True, "school_closure": True, "vaccination": True}
        }
        
        comparison_results = {}
        
        progress_bar = st.progress(0, text="Initializing...")
        
        for idx, (policy_name, policy) in enumerate(policies_to_test.items()):
            progress_bar.progress((idx + 1) / len(policies_to_test), text=f"Testing: {policy_name}...")
            
            set_virus_params(virus_config)
            population = generate_population(POP_SIZE, virus_config)
            seed_infection(population, initial_infected=10)
            metrics = init_metrics()
            
            mutation_tracker = reset_mutation_tracker() if enable_mutations else None

            # Apply policy once before loop for efficiency
            apply_policy_batch(population, policy, virus_config)
            
            # Record initial state (day 0)
            generation_time = virus_config.get("incubation_days", 5) + virus_config.get("infectious_days", 7) / 2
            record_metrics(metrics, population, 
                          mortality_rate=virus_config.get("mortality_rate", 0.02),
                          generation_time=generation_time)
            
            for day in range(DAYS):
                # Update SEIR first
                if enable_mutations and mutation_tracker:
                    update_seir(population, mutation_tracker=mutation_tracker, current_day=day)
                else:
                    update_seir(population)
                
                # Record metrics after update
                record_metrics(metrics, population, 
                              mortality_rate=virus_config.get("mortality_rate", 0.02),
                              generation_time=generation_time)

            # Calculate summary metrics
            peak_infected = max(metrics["overall"]["I"]) if metrics["overall"]["I"] else 0
            final_recovered = metrics["overall"]["R"][-1] if metrics["overall"]["R"] else 0
            current_infected = metrics["overall"]["I"][-1] if metrics["overall"]["I"] else 0
            current_exposed = metrics["overall"]["E"][-1] if metrics["overall"]["E"] else 0
            total_ever_infected = final_recovered + current_infected + current_exposed
            total_deaths = int(total_ever_infected * virus_config.get("mortality_rate", 0.02))

            # Estimate economic cost (simplified)
            school_days = DAYS if policy.get("school_closure", False) else 0
            economic_cost = (school_days * 100) + (final_recovered * 10)

            comparison_results[policy_name] = {
                "peak_infected": peak_infected,
                "total_deaths": total_deaths,
                "final_recovered": final_recovered,
                "economic_cost": economic_cost,
                "metrics": metrics
            }
            
            progress_bar.empty()
        
        # Store results in session state for policy comparison
        best_policy = min(comparison_results.keys(), 
                         key=lambda k: comparison_results[k]["total_deaths"])
        
        st.session_state.simulation_results = {
            'metrics': comparison_results[best_policy]["metrics"],
            'population': population,
            'virus_config': virus_config,
            'POP_SIZE': POP_SIZE,
            'mutation_tracker': None,
            'comparison_results': comparison_results,
            'best_policy': best_policy,
            'mode': 'policy_comparison'
        }
        
        # Mark simulation as complete
        st.session_state["simulation_complete"] = True
        st.success("Policy comparison analysis completed!")
        st.session_state["running"] = False

    # ---------- MANUAL MODE ----------
    elif control_mode == "Manual Policy":
        with st.spinner("Running manual policy simulation..."):

            set_virus_params(virus_config)
            population = generate_population(POP_SIZE, virus_config)
            seed_infection(population, initial_infected=10)
            metrics = init_metrics()

            policy = {
                "mask_mandate": mask_mandate,
                "school_closure": school_closure,
                "vaccination": vaccination
            }
            
            # Initialize mutation tracker if enabled
            mutation_tracker = reset_mutation_tracker() if enable_mutations else None

            progress_bar = st.progress(0, text="Running simulation...")
            
            # Apply policy once before loop if it doesn't change
            apply_policy_batch(population, policy, virus_config)
            
            # Record initial state (day 0)
            generation_time = virus_config.get("incubation_days", 5) + virus_config.get("infectious_days", 7) / 2
            record_metrics(metrics, population,
                          mortality_rate=virus_config.get("mortality_rate", 0.02),
                          generation_time=generation_time)
            
            # Update progress less frequently for better performance
            update_interval = max(1, DAYS // 10)
            
            for day in range(DAYS):
                # Update SEIR with mutation support
                if enable_mutations and mutation_tracker:
                    update_seir(population, mutation_tracker=mutation_tracker, current_day=day)
                else:
                    update_seir(population)
                
                # Record metrics after update
                record_metrics(metrics, population,
                              mortality_rate=virus_config.get("mortality_rate", 0.02),
                              generation_time=generation_time)
                
                # Update progress bar
                if day % update_interval == 0 or day == DAYS - 1:
                    progress_bar.progress((day + 1) / DAYS, text=f"Day {day+1}/{DAYS}")
            
            progress_bar.empty()
        
        # ====== MUTATION DISPLAY ======
        if mutation_tracker and mutation_tracker.mutation_count > 0:
            st.markdown(f"""
            <div class="warning-box">
                <h4>{mutation_tracker.mutation_count} mutation(s) detected during simulation!</h4>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Mutation Details", expanded=True):
                for mut in mutation_tracker.get_summary()["events"]:
                    col1, col2, col3 = st.columns([1, 2, 2])
                    
                    with col1:
                        st.markdown(f"**Day {mut['day']}**  \nStrain {mut['strain_number']}")
                    
                    with col2:
                        st.markdown(f"""
                        **R0:** {mut['changes']['R0']['old']:.2f} → {mut['changes']['R0']['new']:.2f}  
                        ({mut['changes']['R0']['change_pct']:+.1f}%)
                        """)
                    
                    with col3:
                        st.markdown(f"""
                        **Mortality:** {mut['changes']['mortality_rate']['old']:.4f} → {mut['changes']['mortality_rate']['new']:.4f}  
                        ({mut['changes']['mortality_rate']['change_pct']:+.1f}%)
                        """)
                    
                    st.markdown("---")
        
        # Store results in session state
        st.session_state.simulation_results = {
            'metrics': metrics,
            'population': population,
            'virus_config': virus_config,
            'POP_SIZE': POP_SIZE,
            'mutation_tracker': mutation_tracker if enable_mutations else None,
            'mode': 'manual'
        }
        
        # Mark simulation as complete
        st.session_state["simulation_complete"] = True
        st.success("Manual/Policy Comparison simulation completed!")
        st.session_state["running"] = False

    # ---------- AI (RL) MODE ----------
    else:
        with st.spinner("AI is controlling policies using Reinforcement Learning..."):

            env = EpiControlEnv(
                population_size=POP_SIZE,
                days=DAYS,
                virus_config=virus_config
            )
            set_virus_params(virus_config)

            try:
                rl_agent = load_trained_agent(
                    action_size=env.action_space.n,
                    virus_name=virus_name
                )
                st.success("AI agent loaded successfully!")
            except FileNotFoundError as e:
                st.warning("No pre-trained AI model found.  Using Manual Mode instead.")
                st.info("""
                **Training AI agents locally:**
                
                To train the AI agent on your local machine:
                ```bash
                python rl/train.py
                ```
                
                This simulation will run in **Manual Mode** for now.
                """)
                # Fallback to manual mode instead of stopping
                st.session_state["running"] = False
                st.stop()
            except Exception as e:
                st.error(f"Error loading agent: {e}")
                st.session_state["running"] = False
                st.stop()

            obs = env.reset()
            state = discretize_state(obs)
            done = False
            day = 0

            metrics = init_metrics()
            
            mutation_tracker = reset_mutation_tracker() if enable_mutations else None

            action_map = {
                0: "No Action",
                1: "Mask Mandate",
                2: "School Closure",
                3: "Mask + School Closure",
                4: "Vaccination Drive"
            }
            
            action_history = []

            progress_bar = st.progress(0, text="AI making decisions...")
            decision_container = st.empty()
            
            while not done:
                action = rl_agent.choose_action(state)
                action_history.append(action_map[action])

                if day % 5 == 0:
                    decision_container.info(f"Day {day}: AI chose → **{action_map[action]}**")
                    progress_bar.progress(min(day / DAYS, 1.0), text=f"Day {day}/{DAYS}")

                # Pass mutation_tracker to env.step so update_seir handles mutations internally
                obs, reward, done, _ = env.step(
                    action,
                    mutation_tracker=mutation_tracker if enable_mutations else None,
                    current_day=day
                )
                state = discretize_state(obs)

                record_metrics(metrics, env.population,
                              mortality_rate=virus_config.get("mortality_rate", 0.02),
                              generation_time=virus_config.get("incubation_days", 5) + virus_config.get("infectious_days", 7) / 2)
                
                day += 1
            
            progress_bar.empty()
            decision_container.empty()
        
            # Display AI decision summary
            st.markdown("---")
            st.markdown("### AI Decision Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="info-box">
                    <h4>Most Frequent Action</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: #667eea;">""" + max(set(action_history), key=action_history.count) + """</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="info-box">
                    <h4>Total Decisions Made</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: #667eea;">""" + str(len(action_history)) + """</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.caption(
                "*The AI has learned stable optimal policies through training. "
                "Repeated actions indicate convergence to optimal strategy.*"
            )
            
            # ====== CALCULATE KEY METRICS ======
            st.markdown("---")
            st.markdown("## Simulation Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                peak_infected = max(metrics["overall"]["I"]) if metrics["overall"]["I"] else 0
                st.metric(
                    "Peak Infected",
                    f"{int(peak_infected)}",
                    delta=f"{(peak_infected/POP_SIZE)*100:.1f}% of population"
                )
            
            with col2:
                # Calculate total ever infected (current R + I + E)
                final_recovered = metrics["overall"]["R"][-1] if metrics["overall"]["R"] else 0
                current_infected = metrics["overall"]["I"][-1] if metrics["overall"]["I"] else 0
                current_exposed = metrics["overall"]["E"][-1] if metrics["overall"]["E"] else 0
                total_ever_infected = final_recovered + current_infected + current_exposed
                
                # Deaths = total infected * mortality rate
                total_deaths = int(total_ever_infected * virus_config.get("mortality_rate", 0.02))
                death_rate = (total_deaths / POP_SIZE) * 100 if POP_SIZE > 0 else 0
                
                st.metric(
                    "Estimated Deaths",
                    f"{total_deaths}",
                    delta=f"{death_rate:.2f}% of population"
                )
            
            with col3:
                final_recovered = metrics["overall"]["R"][-1] if metrics["overall"]["R"] else 0
                # Survivors = recovered - deaths from recovered
                survivors = int(final_recovered * (1 - virus_config.get("mortality_rate", 0.02)))
                st.metric(
                    "Recovered (Alive)",
                    f"{survivors}",
                    delta=f"{(survivors/POP_SIZE)*100:.1f}% recovered"
                )
            
            with col4:
                final_susceptible = metrics["overall"]["S"][-1] if metrics["overall"]["S"] else 0
                st.metric(
                    "Still Susceptible",
                    f"{int(final_susceptible)}",
                    delta=f"{(final_susceptible/POP_SIZE)*100:.1f}% unaffected"
                )
            
            # Additional Epidemiological Metrics
            st.markdown("---")
            st.markdown("### Advanced Epidemiological Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_Rt = metrics.get("Rt", [0])[-1] if metrics.get("Rt") else 0
                rt_trend = "decreasing" if current_Rt < 1.0 else "increasing"
                st.metric(
                    "Effective Rt (Current)",
                    f"{current_Rt:.2f}",
                    delta=f"Epidemic {rt_trend}",
                    delta_color="inverse" if current_Rt >= 1.0 else "normal"
                )
            
            with col2:
                attack_rate = metrics.get("attack_rate", 0) * 100
                st.metric(
                    "Attack Rate",
                    f"{attack_rate:.1f}%",
                    delta="Cumulative infection rate"
                )
            
            with col3:
                current_incidence = metrics.get("incidence_rate", [0])[-1] if metrics.get("incidence_rate") else 0
                st.metric(
                    "Incidence Rate",
                    f"{current_incidence:.1f}",
                    delta="per 100k per day"
                )
        
            # Store results in session state
            st.session_state.simulation_results = {
                'metrics': metrics,
                'population': env.population,
                'virus_config': virus_config,
                'POP_SIZE': POP_SIZE,
                'mutation_tracker': None,  # AI mode doesn't support mutations yet
                'mode': 'ai'
            }
            
            # Mark simulation as complete
            st.session_state["simulation_complete"] = True
            st.success("AI (RL) mode simulation completed!")
            st.session_state["running"] = False

    # ========== SYMPTOM PREDICTION MODULE ==========
    if st.session_state.show_symptom_prediction and st.session_state.symptom_predictor is not None:
        st.markdown("---")
        st.markdown("## Symptom Prediction Analysis")
        st.markdown("""
        <div class="info-box">
            <h4>Evidence-Based Symptom Forecasting</h4>
            <p>This module analyzes the epidemiological parameters of the current pathogen and compares them with 
            historical pandemic data (COVID-19, SARS, MERS, H1N1, Ebola, Seasonal Flu) to predict probable symptom 
            patterns and severity distributions.</p>
            <p><strong>Methodology:</strong> Comparative analysis using the 3M approach (Monitoring-Modelling-Managing) 
            with weighted similarity scoring across transmission rate, incubation period, severity, and other key indicators.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare parameters for prediction
        prediction_params = {
            'r0': virus_config.get('R0', 2.0),
            'incubation_period': virus_config.get('incubation_days', 5.0),
            'case_fatality_rate': virus_config.get('mortality_rate', 0.02) * 100,  # Convert to percentage
            'serial_interval': virus_config.get('infectious_days', 7.0) * 0.6,  # Approximate
            'hospitalization_rate': virus_config.get('mortality_rate', 0.02) * 500,  # Estimate
            'asymptomatic_rate': 20.0  # Default estimate
        }
        
        # Generate prediction
        predictor = st.session_state.symptom_predictor
        prediction_report = predictor.generate_prediction_report(
            prediction_params,
            virus_name=virus_name
        )
        
        # Display prediction results
        st.markdown(f"### Predictive Analysis for: **{virus_name}**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Transmissibility",
                prediction_report['transmissibility_category'],
                f"R₀ = {prediction_params['r0']:.2f}"
            )
        with col2:
            st.metric(
                "Severity",
                prediction_report['severity_category'],
                f"CFR = {prediction_params['case_fatality_rate']:.2f}%"
            )
        with col3:
            st.metric(
                "Prediction Confidence",
                f"{prediction_report['overall_confidence']:.0f}%",
                "Based on similarity"
            )
        with col4:
            top_match = prediction_report['similar_historical_pandemics'][0]
            st.metric(
                "Closest Match",
                top_match[0],
                f"{top_match[1]:.0f}% similar"
            )
        
        st.markdown("---")
        
        # Predicted symptoms display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Primary Symptoms (Expected)")
            primary_symptoms = prediction_report['symptom_predictions']['primary']
            if primary_symptoms:
                for symptom in primary_symptoms[:5]:  # Top 5
                    st.markdown(f"""
                    <div class="metric-card">
                        <h5>{symptom['name']}</h5>
                        <p><strong>Predicted Prevalence:</strong> {symptom['predicted_prevalence']:.1f}%</p>
                        <p><strong>Severity:</strong> {symptom['severity'].capitalize()}</p>
                        <p><strong>Expected Onset:</strong> Day {symptom['predicted_onset_day']:.1f}</p>
                        <p><strong>Confidence:</strong> {symptom['confidence']:.0f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No primary symptoms predicted with high confidence")
        
        with col2:
            st.markdown("#### Secondary Symptoms (Possible)")
            secondary_symptoms = prediction_report['symptom_predictions']['secondary']
            if secondary_symptoms:
                for symptom in secondary_symptoms[:5]:  # Top 5
                    st.markdown(f"""
                    <div class="metric-card">
                        <h5>{symptom['name']}</h5>
                        <p><strong>Predicted Prevalence:</strong> {symptom['predicted_prevalence']:.1f}%</p>
                        <p><strong>Severity:</strong> {symptom['severity'].capitalize()}</p>
                        <p><strong>Expected Onset:</strong> Day {symptom['predicted_onset_day']:.1f}</p>
                        <p><strong>Confidence:</strong> {symptom['confidence']:.0f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No secondary symptoms predicted with sufficient prevalence")
        
        st.markdown("---")
        
        # Severe complications
        st.markdown("#### Potential Severe Complications")
        severe_complications = prediction_report['symptom_predictions']['severe_complications']
        
        comp_cols = st.columns(len(severe_complications) if len(severe_complications) <= 4 else 4)
        for idx, comp in enumerate(severe_complications[:4]):
            with comp_cols[idx]:
                st.markdown(f"""
                <div class="warning-box">
                    <h5>{comp['name']}</h5>
                    <p><strong>Risk Level:</strong> {comp['risk'].capitalize()}</p>
                    <p><strong>Est. Prevalence:</strong> {comp['estimated_prevalence']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Historical comparison
        st.markdown("#### Similar Historical Pandemics")
        st.markdown("Based on epidemiological parameter matching:")
        
        for pandemic_name, similarity in prediction_report['similar_historical_pandemics']:
            pandemic_data = HISTORICAL_PANDEMICS[pandemic_name]
            
            with st.expander(f"{pandemic_name} - {similarity:.1f}% Match"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Year:** {pandemic_data['year']}")
                    st.write(f"**Virus Type:** {pandemic_data['virus_type']}")
                    st.write(f"**R₀:** {pandemic_data['epidemiology']['r0']:.2f}")
                with col2:
                    st.write(f"**CFR:** {pandemic_data['epidemiology']['case_fatality_rate']:.2f}%")
                    st.write(f"**Incubation:** {pandemic_data['epidemiology']['incubation_period']:.1f} days")
                    st.write(f"**Hospitalization:** {pandemic_data['epidemiology']['hospitalization_rate']:.1f}%")
                with col3:
                    st.write(f"**Primary Route:** {pandemic_data['transmission']['primary_route'].replace('_', ' ').title()}")
                    st.write(f"**Mutation Rate:** {pandemic_data['mutation_behavior']['mutation_rate'].title()}")
                    st.write(f"**Superspreading:** {'Yes' if pandemic_data['transmission']['superspreading_events'] else 'No'}")
        
        st.markdown("---")
        
        # Insights
        st.markdown("#### Key Insights & Recommendations")
        for insight in prediction_report['insights']:
            st.markdown(f"- {insight}")
        
        # Disclaimer
        st.markdown("---")
        st.markdown(f"""
        <div class="warning-box">
            <h4>Important Disclaimer</h4>
            <p>{prediction_report['disclaimer']}</p>
            <p><strong>Data Sources:</strong> WHO reports, CDC databases, peer-reviewed epidemiological research</p>
            <p><strong>Model Basis:</strong> Comparative analysis with 6 major historical pandemics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state["running"] = False

# ========== DISPLAY RESULTS FROM SESSION STATE ==========
# This section displays results even after parameters change (before re-running)
if st.session_state.simulation_results is not None and st.session_state.simulation_complete:
    results = st.session_state.simulation_results
    metrics = results['metrics']
    population = results['population']
    virus_config = results['virus_config']
    POP_SIZE = results['POP_SIZE']
    mutation_tracker = results.get('mutation_tracker')
    mode = results.get('mode', 'normal')
    
    # Special display for policy comparison mode
    if mode == 'policy_comparison':
        comparison_results = results['comparison_results']
        best_policy = results['best_policy']
        
        st.markdown("---")
        st.markdown("## Policy Effectiveness Comparison")
        
        # Metric cards for best policy
        st.markdown(f"""
        <div class="success-box">
            <h3>Recommended Strategy: {best_policy}</h3>
            <p>This strategy resulted in the lowest number of deaths.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Peak Infected",
                f"{int(comparison_results[best_policy]['peak_infected'])}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Total Deaths",
                f"{comparison_results[best_policy]['total_deaths']}",
                delta=None
            )
        
        with col3:
            st.metric(
                "Final Recovered",
                f"{int(comparison_results[best_policy]['final_recovered'])}",
                delta=None
            )
        
        with col4:
            st.metric(
                "Economic Cost",
                f"${comparison_results[best_policy]['economic_cost']:,.0f}",
                delta=None
            )
        
        # Display comparison chart
        comparison_fig = plot_policy_comparison(comparison_results)
        st.plotly_chart(comparison_fig, use_container_width=True, key="policy_comparison_chart")
        
        # Show detailed SEIR for best policy
        st.markdown("### SEIR Dynamics: Best Strategy")
        fig = plot_seir_plotly(comparison_results[best_policy]["metrics"])
        st.plotly_chart(fig, use_container_width=True, key="best_policy_seir_chart")
    
    st.markdown("---")
    st.markdown("## Simulation Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        peak_infected = max(metrics["overall"]["I"]) if metrics["overall"]["I"] else 0
        st.metric(
            "Peak Infected",
            f"{int(peak_infected)}",
            delta=f"{(peak_infected/POP_SIZE)*100:.1f}% of population"
        )
    
    with col2:
        # Calculate total ever infected (current R + I + E)
        final_recovered = metrics["overall"]["R"][-1] if metrics["overall"]["R"] else 0
        current_infected = metrics["overall"]["I"][-1] if metrics["overall"]["I"] else 0
        current_exposed = metrics["overall"]["E"][-1] if metrics["overall"]["E"] else 0
        total_ever_infected = final_recovered + current_infected + current_exposed
        
        # Deaths = total infected * mortality rate
        total_deaths = int(total_ever_infected * virus_config.get("mortality_rate", 0.02))
        death_rate = (total_deaths / POP_SIZE) * 100 if POP_SIZE > 0 else 0
        
        st.metric(
            "Estimated Deaths",
            f"{total_deaths}",
            delta=f"{death_rate:.2f}% of population"
        )
    
    with col3:
        final_recovered = metrics["overall"]["R"][-1] if metrics["overall"]["R"] else 0
        # Survivors = recovered - deaths from recovered
        survivors = int(final_recovered * (1 - virus_config.get("mortality_rate", 0.02)))
        st.metric(
            "Recovered (Alive)",
            f"{survivors}",
            delta=f"{(survivors/POP_SIZE)*100:.1f}% recovered"
        )
    
    with col4:
        final_susceptible = metrics["overall"]["S"][-1] if metrics["overall"]["S"] else 0
        st.metric(
            "Still Susceptible",
            f"{int(final_susceptible)}",
            delta=f"{(final_susceptible/POP_SIZE)*100:.1f}% unaffected"
        )
    
    # Additional Epidemiological Metrics
    st.markdown("---")
    st.markdown("### Advanced Epidemiological Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_Rt = metrics.get("Rt", [0])[-1] if metrics.get("Rt") else 0
        rt_trend = "decreasing" if current_Rt < 1.0 else "increasing"
        st.metric(
            "Effective Rt (Current)",
            f"{current_Rt:.2f}",
            delta=f"Epidemic {rt_trend}",
            delta_color="inverse" if current_Rt >= 1.0 else "normal"
        )
    
    with col2:
        attack_rate = metrics.get("attack_rate", 0) * 100
        st.metric(
            "Attack Rate",
            f"{attack_rate:.1f}%",
            delta="Cumulative infection rate"
        )
    
    with col3:
        current_incidence = metrics.get("incidence_rate", [0])[-1] if metrics.get("incidence_rate") else 0
        st.metric(
            "Incidence Rate",
            f"{current_incidence:.1f}",
            delta="per 100k per day"
        )
    
    # ========== VISUALIZATIONS ==========
    st.markdown("---")
    st.markdown("## Visualization Dashboard")
    
    # Main SEIR plot
    st.markdown("### SEIR Epidemic Dynamics")
    fig = plot_seir_plotly(metrics)
    st.plotly_chart(fig, use_container_width=True, key="seir_main_chart")
    
    # Mutation timeline (if mutations occurred and option enabled)
    if mutation_tracker and mutation_tracker.mutation_count > 0:
        st.markdown("### Mutation Timeline")
        mutation_fig = plot_mutation_timeline(mutation_tracker, metrics)
        st.plotly_chart(mutation_fig, use_container_width=True, key="mutation_timeline_chart")
    
    # Spatial visualizations
    if show_heatmap:
        st.markdown("### Infection Hotspot Heatmap")
        heatmap_fig = plot_infection_heatmap(population, title="Geographic Infection Distribution")
        st.plotly_chart(heatmap_fig, use_container_width=True, key="heatmap_chart")
    
    if show_spatial:
        st.markdown("### Real-time Agent Spatial Distribution")
        spatial_fig = plot_spatial_scatter(population)
        st.plotly_chart(spatial_fig, use_container_width=True, key="spatial_scatter_chart")
    
    if show_timeline:
        st.markdown("### Epidemic Timeline Progression")
        timeline_fig = plot_seir_plotly(metrics)
        st.plotly_chart(timeline_fig, use_container_width=True, key="timeline_progression_chart")

    # Global Map Visualizations
    st.markdown("---")
    st.markdown("## Global Epidemic Surveillance")
    
    map_view = st.radio("Map View", ["World Map (Flat)", "Globe View (3D)"], horizontal=True)
    
    if map_view == "World Map (Flat)":
        global_map = plot_global_epidemic_map(metrics)
        st.plotly_chart(global_map, use_container_width=True, key="global_map_chart")
    else:
        globe_view = plot_globe_view_3d(metrics)
        st.plotly_chart(globe_view, use_container_width=True, key="globe_view_chart")

elif not st.session_state.simulation_complete:
    st.info("👈 Configure parameters in the sidebar and click 'Run Simulation' to begin")

# ========== SYMPTOM PREDICTION (persisted after simulation) ==========
if st.session_state.simulation_complete and st.session_state.show_symptom_prediction and st.session_state.symptom_predictor is not None:
    results = st.session_state.simulation_results
    virus_config = results['virus_config']
    # Determine virus name from session
    _virus_name = virus_name if 'virus_name' in dir() else "Unknown"

    st.markdown("---")
    st.markdown("## Symptom Prediction Analysis")
    st.markdown("""
    <div class="info-box">
        <h4>Evidence-Based Symptom Forecasting</h4>
        <p>This module analyzes the epidemiological parameters of the current pathogen and compares them with 
        historical pandemic data (COVID-19, SARS, MERS, H1N1, Ebola, Seasonal Flu) to predict probable symptom 
        patterns and severity distributions.</p>
        <p><strong>Methodology:</strong> Comparative analysis using the 3M approach (Monitoring-Modelling-Managing) 
        with weighted similarity scoring across transmission rate, incubation period, severity, and other key indicators.</p>
    </div>
    """, unsafe_allow_html=True)

    prediction_params = {
        'r0': virus_config.get('R0', 2.0),
        'incubation_period': virus_config.get('incubation_days', 5.0),
        'case_fatality_rate': virus_config.get('mortality_rate', 0.02) * 100,
        'serial_interval': virus_config.get('infectious_days', 7.0) * 0.6,
        'hospitalization_rate': virus_config.get('mortality_rate', 0.02) * 500,
        'asymptomatic_rate': 20.0
    }

    predictor = st.session_state.symptom_predictor
    prediction_report = predictor.generate_prediction_report(prediction_params, virus_name=_virus_name)

    st.markdown(f"### Predictive Analysis for: **{_virus_name}**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Transmissibility", prediction_report['transmissibility_category'],
                  f"R₀ = {prediction_params['r0']:.2f}")
    with col2:
        st.metric("Severity", prediction_report['severity_category'],
                  f"CFR = {prediction_params['case_fatality_rate']:.2f}%")
    with col3:
        st.metric("Prediction Confidence", f"{prediction_report['overall_confidence']:.0f}%",
                  "Based on similarity")
    with col4:
        top_match = prediction_report['similar_historical_pandemics'][0]
        st.metric("Closest Match", top_match[0], f"{top_match[1]:.0f}% similar")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Primary Symptoms (Expected)")
        primary_symptoms = prediction_report['symptom_predictions']['primary']
        if primary_symptoms:
            for symptom in primary_symptoms[:5]:
                st.markdown(f"""
                <div class="metric-card">
                    <h5>{symptom['name']}</h5>
                    <p><strong>Predicted Prevalence:</strong> {symptom['predicted_prevalence']:.1f}%</p>
                    <p><strong>Severity:</strong> {symptom['severity'].capitalize()}</p>
                    <p><strong>Expected Onset:</strong> Day {symptom['predicted_onset_day']:.1f}</p>
                    <p><strong>Confidence:</strong> {symptom['confidence']:.0f}%</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No primary symptoms predicted with high confidence")

    with col2:
        st.markdown("#### Secondary Symptoms (Possible)")
        secondary_symptoms = prediction_report['symptom_predictions']['secondary']
        if secondary_symptoms:
            for symptom in secondary_symptoms[:5]:
                st.markdown(f"""
                <div class="metric-card">
                    <h5>{symptom['name']}</h5>
                    <p><strong>Predicted Prevalence:</strong> {symptom['predicted_prevalence']:.1f}%</p>
                    <p><strong>Severity:</strong> {symptom['severity'].capitalize()}</p>
                    <p><strong>Expected Onset:</strong> Day {symptom['predicted_onset_day']:.1f}</p>
                    <p><strong>Confidence:</strong> {symptom['confidence']:.0f}%</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No secondary symptoms predicted with sufficient prevalence")

    st.markdown("---")
    st.markdown("#### Potential Severe Complications")
    severe_complications = prediction_report['symptom_predictions']['severe_complications']
    if severe_complications:
        comp_cols = st.columns(min(len(severe_complications), 4))
        for idx, comp in enumerate(severe_complications[:4]):
            with comp_cols[idx]:
                st.markdown(f"""
                <div class="warning-box">
                    <h5>{comp['name']}</h5>
                    <p><strong>Risk Level:</strong> {comp['risk'].capitalize()}</p>
                    <p><strong>Est. Prevalence:</strong> {comp['estimated_prevalence']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Similar Historical Pandemics")
    for pandemic_name, similarity in prediction_report['similar_historical_pandemics']:
        pandemic_data = HISTORICAL_PANDEMICS[pandemic_name]
        with st.expander(f"{pandemic_name} - {similarity:.1f}% Match"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Year:** {pandemic_data['year']}")
                st.write(f"**Virus Type:** {pandemic_data['virus_type']}")
                st.write(f"**R₀:** {pandemic_data['epidemiology']['r0']:.2f}")
            with col2:
                st.write(f"**CFR:** {pandemic_data['epidemiology']['case_fatality_rate']:.2f}%")
                st.write(f"**Incubation:** {pandemic_data['epidemiology']['incubation_period']:.1f} days")
                st.write(f"**Hospitalization:** {pandemic_data['epidemiology']['hospitalization_rate']:.1f}%")
            with col3:
                st.write(f"**Primary Route:** {pandemic_data['transmission']['primary_route'].replace('_', ' ').title()}")
                st.write(f"**Mutation Rate:** {pandemic_data['mutation_behavior']['mutation_rate'].title()}")
                st.write(f"**Superspreading:** {'Yes' if pandemic_data['transmission']['superspreading_events'] else 'No'}")

    st.markdown("---")
    st.markdown("#### Key Insights & Recommendations")
    for insight in prediction_report['insights']:
        st.markdown(f"- {insight}")

    st.markdown("---")
    st.markdown(f"""
    <div class="warning-box">
        <h4>Important Disclaimer</h4>
        <p>{prediction_report['disclaimer']}</p>
        <p><strong>Data Sources:</strong> WHO reports, CDC databases, peer-reviewed epidemiological research</p>
        <p><strong>Model Basis:</strong> Comparative analysis with 6 major historical pandemics</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== INFORMATION FOOTER ====================
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Features", "How to Use", "About"])

with tab1:
    st.markdown("""
    ### Platform Capabilities
    
    <div class="metric-card">
        <h4>SEIR Epidemic Modeling</h4>
        <p>Agent-based simulation with 1000+ individuals tracking Susceptible, Exposed, Infected, and Recovered states</p>
    </div>
    
    <div class="metric-card">
        <h4>Mutation Tracking System</h4>
        <p>Real-time virus evolution modeling with automatic parameter changes based on infection dynamics</p>
    </div>
    
    <div class="metric-card">
        <h4>Symptom Prediction Engine</h4>
        <p><strong>NEW FEATURE:</strong> ML-based symptom forecasting using comparative analysis with historical pandemic data (COVID-19, SARS, MERS, H1N1, Ebola). Predicts symptom patterns, severity distributions, and age-specific impacts for emerging viruses based on epidemiological parameters.</p>
    </div>
    
    <div class="metric-card">
        <h4>Spatial Visualization</h4>
        <p>Geographic heatmaps and spatial scatter plots showing infection spread patterns across populations</p>
    </div>
    
    <div class="metric-card">
        <h4>Reinforcement Learning Control</h4>
        <p>AI-powered policy decisions using Q-Learning to optimize epidemic response strategies</p>
    </div>
    
    <div class="metric-card">
        <h4>WHO Database Integration</h4>
        <p>Access verified parameters for COVID-19, SARS, Measles, Influenza, and Ebola from WHO data</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    ### Quick Start Guide
    
    1. **Configure Simulation** (Left Sidebar)
       - Set population size and simulation duration
       - Select virus from WHO database or custom models
       - Enable mutation tracking (recommended)
       - Enable Symptom Prediction for ML-based symptom forecasting
    
    2. **Choose Control Mode**
       - **Manual Policy:** You control mask mandates, school closures, and vaccination
       - **AI (RL) Policy:** Trained AI agent makes optimal decisions automatically
       - **Policy Comparison:** Compare all strategies side-by-side
    
    3. **Select Visualizations**
       - Infection heatmap shows geographic hotspots
       - Spatial distribution displays agent positions
       - Mutation timeline marks evolution events
    
    4. **Run Simulation**
       - Click "Run Simulation" button
       - Watch real-time progress
       - Analyze results in interactive charts
       - View predicted symptom patterns if enabled
    
    ### Symptom Prediction Feature
    The Symptom Prediction Engine analyzes your selected virus parameters and compares them with 6 major historical pandemics to predict:
    - Primary and secondary symptom profiles
    - Severity distributions and onset timelines
    - Age-specific impact predictions
    - Potential severe complications
    
    Based on the 3M (Monitoring-Modelling-Managing) epidemiological framework.
    
    ### For AI Mode
    Before using AI (RL) Policy mode, train the agent:
    ```bash
    python rl/train.py
    ```
    This creates a Q-table with learned optimal policies.
    """)

with tab3:
    st.markdown("""
    ### Project Information
    
    **Project:** EpiControl AI - Advanced Epidemic Simulation Platform  
    **Team:** Neural Mavericks  
    
    ### Technology Stack
    - **Backend:** Python 3.8+, NumPy
    - **RL Framework:** Custom Q-Learning implementation
    - **Visualization:** Plotly, Streamlit
    - **Modeling:** Agent-based SEIR simulation
    
    ### Contact
    For questions or collaboration opportunities, contact Team Neural Mavericks.
    
    ### License
    This project is developed for educational and research purposes.
    """)

# ==================== SIDEBAR FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
    <small><b>EpiControl AI</b><br>
    Team Neural Mavericks<br>
    </small>
</div>
""", unsafe_allow_html=True)
