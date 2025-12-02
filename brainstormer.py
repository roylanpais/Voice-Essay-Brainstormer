import logging
import time
import random
from typing import List, Optional, Union
from google import genai
from google.genai import types
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EssayBrainstormer:
    def __init__(self, api_key: str, model_name: str = config.DEFAULT_MODEL):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.history: List[types.Content] = []
        
        self.system_prompt = config.SYSTEM_PROMPT
        
        # Add system prompt to history
        self.history.append(types.Content(role="user", parts=[types.Part.from_text(text=self.system_prompt)]))
        self.history.append(types.Content(role="model", parts=[types.Part.from_text(text="Understood. I am ready to help you brainstorm.")]))
        logger.info(f"EssayBrainstormer initialized with model: {model_name}")

    def send_message(self, user_input: Optional[str] = None, audio_bytes: Optional[bytes] = None) -> str:
        """
        Sends a message to the Gemini model and returns the response.
        Accepts text (user_input) and/or audio_bytes.
        """
        parts = []
        if user_input:
            parts.append(types.Part.from_text(text=user_input))
        
        if audio_bytes:
            parts.append(types.Part.from_bytes(data=audio_bytes, mime_type=config.AUDIO_FORMAT))
            logger.info("Audio input received.")

        if not parts:
            logger.warning("send_message called with no input.")
            return "No input provided."

        # Add user message to history
        self.history.append(types.Content(role="user", parts=parts))

        # Retry logic for 503 errors
        for attempt in range(config.MAX_RETRIES):
            try:
                # Generate response with full history
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=self.history,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt
                    )
                )
                
                response_text = response.text
                
                # Add model response to history
                self.history.append(types.Content(role="model", parts=[types.Part.from_text(text=response_text)]))
                
                return response_text
            except Exception as e:
                logger.error(f"Error communicating with Gemini (Attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
                if "503" in str(e) and attempt < config.MAX_RETRIES - 1:
                    sleep_time = config.BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                else:
                    return f"Error communicating with Gemini: {e}"
        return "Error: Failed to communicate with Gemini after multiple retries."

    def generate_structure(self) -> str:
        """
        Explicitly requests the essay structure based on the conversation so far.
        """
        logger.info("Generating essay structure.")
        prompt = "Based on our conversation, please generate a detailed essay structure breakdown by words/sections. Include an introduction, body paragraphs with specific points from our discussion, and a conclusion."
        return self.send_message(user_input=prompt)

