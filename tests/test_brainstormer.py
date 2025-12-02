import pytest
from unittest.mock import MagicMock, patch
from brainstormer import EssayBrainstormer
import config

@pytest.fixture
def mock_genai_client():
    with patch('brainstormer.genai.Client') as mock_client:
        yield mock_client

def test_initialization(mock_genai_client):
    api_key = "test_key"
    brainstormer = EssayBrainstormer(api_key)
    
    assert brainstormer.model_name == config.DEFAULT_MODEL
    assert len(brainstormer.history) == 2 # System prompt + confirmation
    mock_genai_client.assert_called_with(api_key=api_key)

def test_send_message_text(mock_genai_client):
    brainstormer = EssayBrainstormer("test_key")
    
    mock_response = MagicMock()
    mock_response.text = "AI Response"
    brainstormer.client.models.generate_content.return_value = mock_response
    
    response = brainstormer.send_message("Hello")
    
    assert response == "AI Response"
    assert len(brainstormer.history) == 4 # Initial 2 + User + Model
    brainstormer.client.models.generate_content.assert_called()

def test_send_message_no_input(mock_genai_client):
    brainstormer = EssayBrainstormer("test_key")
    response = brainstormer.send_message()
    assert response == "No input provided."

def test_generate_structure(mock_genai_client):
    brainstormer = EssayBrainstormer("test_key")
    
    mock_response = MagicMock()
    mock_response.text = "Essay Structure"
    brainstormer.client.models.generate_content.return_value = mock_response
    
    response = brainstormer.generate_structure()
    
    assert response == "Essay Structure"
