# Voice Essay Brainstormer

A voice-enabled interactive assistant designed to help you brainstorm and structure your essays using Google's Gemini LLM.

## Overview

The **Voice Essay Brainstormer** is a Streamlit application that acts as an expert essay strategist. It interviews you about your life stories, experiences, and opinions related to your chosen topic. Through a natural conversation (via voice or text), it gathers the necessary context to generate a detailed, word-count-specific essay structure.

## Features

-   **Voice Interaction**: Speak directly to the assistant and hear its responses using Text-to-Speech (TTS).
-   **Gemini Powered**: Utilizes the latest **Gemini 2.0 Flash** models for deep understanding and creative strategizing.
-   **Interactive Interview**: The AI asks probing questions to uncover unique angles for your essay.
-   **Structure Generation**: Automatically generates a detailed essay outline with word count breakdowns for each section.
-   **Multi-Modal**: Supports both voice and text inputs seamlessly.

## Prerequisites

-   **Python 3.8+**
-   **Gemini API Key**: You need a valid API key from Google AI Studio.

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to install system-level dependencies for `pydub` (like `ffmpeg`) depending on your OS.*

## Usage

1.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

2.  **Enter your API Key**:
    -   On the sidebar, enter your **Gemini API Key**.

3.  **Start Brainstorming**:
    -   **Select Model**: Choose your preferred Gemini model (default: `gemini-2.0-flash`).
    -   **Interact**: Type your answers or use the "🎤 Record" button to speak.
    -   **Generate Structure**: Once you've discussed enough, click the "Generate Essay Structure" button to get your detailed outline.

## Configuration

You can customize the application behavior in `config.py`:

-   **`AVAILABLE_MODELS`**: List of supported Gemini models.
-   **`SYSTEM_PROMPT`**: The core instructions for the AI interviewer.
-   **`INITIAL_GREETING`**: The starting message from the assistant.
-   **`AUDIO_FORMAT`**: Audio format for voice interactions.

## Project Structure

-   `app.py`: Main Streamlit application file.
-   `brainstormer.py`: Core logic for managing the Gemini session and history.
-   `config.py`: Configuration settings and constants.
-   `audio_utils.py`: Utilities for Text-to-Speech conversion.
-   `requirements.txt`: Python dependencies.
