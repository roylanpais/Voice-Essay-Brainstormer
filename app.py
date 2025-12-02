import streamlit as st
import logging
from brainstormer import EssayBrainstormer
from audio_utils import text_to_speech
from streamlit_mic_recorder import mic_recorder
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Voice Essay Brainstormer", page_icon="🎙️")

st.title("🎙️ Voice-Based Essay Brainstormer")

# Sidebar for API Key
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    selected_model = st.selectbox("Choose AI Model", config.AVAILABLE_MODELS, index=1) # Default to gemini-2.0-flash

    if not api_key:
        st.warning("Please enter your Gemini API Key to continue.")
        st.stop()

def initialize_brainstormer(api_key, model_name):
    """Initializes or re-initializes the brainstormer and session state."""
    st.session_state.brainstormer = EssayBrainstormer(api_key, model_name)
    st.session_state.messages = []
    initial_msg = f"Switched to {model_name}. " + config.INITIAL_GREETING if "brainstormer" in st.session_state else config.INITIAL_GREETING
    if "brainstormer" in st.session_state: # Re-init
         initial_msg = f"Switched to {model_name}. " + config.INITIAL_GREETING
    else:
         initial_msg = config.INITIAL_GREETING

    st.session_state.messages.append({"role": "assistant", "content": initial_msg})
    audio_bytes = text_to_speech(initial_msg)
    if audio_bytes:
        st.session_state.last_audio = audio_bytes
    logger.info(f"Brainstormer initialized with model {model_name}")

# Initialize Session State
if "brainstormer" not in st.session_state:
    st.session_state.brainstormer = EssayBrainstormer(api_key, selected_model)
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": config.INITIAL_GREETING})
    audio_bytes = text_to_speech(config.INITIAL_GREETING)
    if audio_bytes:
        st.session_state.last_audio = audio_bytes

# Check if model changed
if st.session_state.brainstormer.model_name != selected_model:
     initialize_brainstormer(api_key, selected_model)
     st.rerun()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Play Audio for the last assistant message
if "last_audio" in st.session_state and st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.audio(st.session_state.last_audio, format="audio/mp3", autoplay=True)

# User Input
# Option 1: Text Input
user_input = st.chat_input("Type your answer here...")

# Option 2: Voice Input
audio = mic_recorder(start_prompt="🎤 Record", stop_prompt="⏹️ Stop", key='recorder')

def handle_response(response_text):
    """Helper to handle AI response and audio generation."""
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.write(response_text)
    
    audio_bytes_out = text_to_speech(response_text)
    if audio_bytes_out:
        st.session_state.last_audio = audio_bytes_out
        st.rerun()

if audio:
    # Check if we've already processed this audio to prevent loops
    if "last_processed_audio_id" not in st.session_state:
        st.session_state.last_processed_audio_id = None

    current_audio_id = audio.get('id', audio['bytes']) # Fallback to bytes if ID missing
    
    if current_audio_id != st.session_state.last_processed_audio_id:
        st.session_state.last_processed_audio_id = current_audio_id
        
        # Process audio directly with Gemini
        audio_bytes = audio['bytes']
        
        # Add a placeholder for user audio message
        st.session_state.messages.append({"role": "user", "content": "🎤 [Audio Message]"})
        with st.chat_message("user"):
            st.write("🎤 [Audio Message]")
            st.audio(audio_bytes)

        # Get AI response
        with st.spinner("Thinking..."):
            response_text = st.session_state.brainstormer.send_message(user_input=None, audio_bytes=audio_bytes)
        
        handle_response(response_text)

if user_input:
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    with st.spinner("Thinking..."):
        response_text = st.session_state.brainstormer.send_message(user_input)
    
    handle_response(response_text)

# Button to Generate Structure
if st.button("Generate Essay Structure"):
    with st.spinner("Generating structure..."):
        structure = st.session_state.brainstormer.generate_structure()
        st.session_state.messages.append({"role": "assistant", "content": structure})
        with st.chat_message("assistant"):
            st.write(structure)
