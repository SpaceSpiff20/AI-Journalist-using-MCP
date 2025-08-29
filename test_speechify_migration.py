"""
Test suite for Speechify TTS migration.
Tests the new Speechify integration while ensuring backward compatibility.
"""

import os
import pytest
import base64
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import the functions to test
from utils import (
    text_to_audio_speechify,
    get_speechify_voices,
    filter_voice_models,
    text_to_audio_elevenlabs_sdk,
    tts_to_audio
)


class TestSpeechifyTTS:
    """Test cases for Speechify TTS functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_text = "Testing Speechify migration"
        self.test_api_key = "test_speechify_api_key"
        self.audio_dir = Path("audio")
        self.audio_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Clean up test files."""
        # Clean up any test audio files
        for file in self.audio_dir.glob("test_*.mp3"):
            file.unlink()
    
    @patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"})
    @patch('utils.Speechify')
    def test_speechify_tts_success(self, mock_speechify):
        """Test successful Speechify TTS generation."""
        # Mock the Speechify client and response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode()
        mock_client.tts.audio.speech.return_value = mock_response
        mock_speechify.return_value = mock_client
        
        # Test the function
        result = text_to_audio_speechify(
            text=self.test_text,
            voice_id="scott",
            model="simba-english",
            audio_format="mp3",
            language="en-US"
        )
        
        # Verify the result
        assert result is not None
        assert Path(result).exists()
        assert result.endswith(".mp3")
        
        # Verify the API was called correctly
        mock_client.tts.audio.speech.assert_called_once()
        call_args = mock_client.tts.audio.speech.call_args
        assert call_args[1]["input"] == self.test_text
        assert call_args[1]["voice_id"] == "scott"
        assert call_args[1]["model"] == "simba-english"
        assert call_args[1]["audio_format"] == "mp3"
        assert call_args[1]["language"] == "en-US"
    
    def test_speechify_tts_no_api_key(self):
        """Test Speechify TTS fails gracefully when no API key is provided."""
        with pytest.raises(ValueError, match="Speechify API key is required"):
            text_to_audio_speechify(text=self.test_text)
    
    @patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"})
    @patch('utils.Speechify')
    def test_speechify_tts_api_error(self, mock_speechify):
        """Test Speechify TTS handles API errors gracefully."""
        # Mock the Speechify client to raise an exception
        mock_client = Mock()
        mock_client.tts.audio.speech.side_effect = Exception("API Error")
        mock_speechify.return_value = mock_client
        
        with pytest.raises(Exception, match="API Error"):
            text_to_audio_speechify(text=self.test_text)
    
    @patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"})
    @patch('utils.Speechify')
    def test_speechify_tts_different_formats(self, mock_speechify):
        """Test Speechify TTS with different audio formats."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode()
        mock_client.tts.audio.speech.return_value = mock_response
        mock_speechify.return_value = mock_client
        
        # Test different formats
        formats = ["mp3", "wav", "ogg", "aac"]
        for fmt in formats:
            result = text_to_audio_speechify(
                text=self.test_text,
                audio_format=fmt
            )
            assert result.endswith(f".{fmt}")
    
    @patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"})
    @patch('utils.Speechify')
    def test_speechify_tts_different_languages(self, mock_speechify):
        """Test Speechify TTS with different languages."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode()
        mock_client.tts.audio.speech.return_value = mock_response
        mock_speechify.return_value = mock_client
        
        # Test different languages
        languages = ["en-US", "fr-FR", "de-DE", "es-ES"]
        for lang in languages:
            text_to_audio_speechify(
                text=self.test_text,
                language=lang
            )
            call_args = mock_client.tts.audio.speech.call_args
            assert call_args[1]["language"] == lang


class TestSpeechifyVoices:
    """Test cases for Speechify voice management."""
    
    @patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"})
    @patch('utils.Speechify')
    def test_get_speechify_voices(self, mock_speechify):
        """Test getting available Speechify voices."""
        mock_client = Mock()
        mock_voices = [Mock(), Mock()]
        mock_client.tts.voices.list.return_value = mock_voices
        mock_speechify.return_value = mock_client
        
        voices = get_speechify_voices()
        assert voices == mock_voices
        mock_client.tts.voices.list.assert_called_once()
    
    def test_filter_voice_models(self):
        """Test filtering voice models by various criteria."""
        # Create mock voice objects
        mock_voice1 = Mock()
        mock_voice1.gender = "male"
        mock_voice1.tags = ["timbre:deep", "accent:american"]
        mock_voice1.models = [Mock()]
        mock_voice1.models[0].languages = [Mock()]
        mock_voice1.models[0].languages[0].locale = "en-US"
        mock_voice1.models[0].name = "voice1"
        
        mock_voice2 = Mock()
        mock_voice2.gender = "female"
        mock_voice2.tags = ["timbre:bright"]
        mock_voice2.models = [Mock()]
        mock_voice2.models[0].languages = [Mock()]
        mock_voice2.models[0].languages[0].locale = "fr-FR"
        mock_voice2.models[0].name = "voice2"
        
        voices = [mock_voice1, mock_voice2]
        
        # Test filtering by gender
        male_voices = filter_voice_models(voices, gender="male")
        assert len(male_voices) == 1
        assert male_voices[0] == "voice1"
        
        # Test filtering by locale
        en_voices = filter_voice_models(voices, locale="en-US")
        assert len(en_voices) == 1
        assert en_voices[0] == "voice1"
        
        # Test filtering by tags
        deep_voices = filter_voice_models(voices, tags=["timbre:deep"])
        assert len(deep_voices) == 1
        assert deep_voices[0] == "voice1"
        
        # Test filtering by multiple criteria
        filtered = filter_voice_models(voices, gender="male", locale="en-US")
        assert len(filtered) == 1
        assert filtered[0] == "voice1"


class TestBackwardCompatibility:
    """Test cases to ensure backward compatibility with existing TTS functions."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_text = "Testing backward compatibility"
        self.audio_dir = Path("audio")
        self.audio_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Clean up test files."""
        for file in self.audio_dir.glob("test_*.mp3"):
            file.unlink()
    
    @patch.dict(os.environ, {"ELEVEN_API_KEY": "test_key"})
    @patch('utils.ElevenLabs')
    def test_elevenlabs_fallback(self, mock_elevenlabs):
        """Test that ElevenLabs still works as fallback."""
        mock_client = Mock()
        mock_stream = [b"fake_audio_chunk"]
        mock_client.text_to_speech.convert.return_value = mock_stream
        mock_elevenlabs.return_value = mock_client
        
        result = text_to_audio_elevenlabs_sdk(
            text=self.test_text,
            voice_id="test_voice",
            model_id="test_model",
            output_format="mp3_44100_128"
        )
        
        assert result is not None
        assert Path(result).exists()
    
    @patch('utils.gTTS')
    def test_gtts_fallback(self, mock_gtts):
        """Test that gTTS still works as fallback."""
        mock_tts = Mock()
        mock_gtts.return_value = mock_tts
        
        result = tts_to_audio(self.test_text, language="en")
        
        assert result is not None
        mock_tts.save.assert_called_once()


class TestIntegration:
    """Integration tests for the complete TTS workflow."""
    
    @patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"})
    @patch('utils.Speechify')
    def test_speechify_integration(self, mock_speechify):
        """Test complete Speechify integration workflow."""
        # Mock the Speechify client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode()
        mock_client.tts.audio.speech.return_value = mock_response
        mock_speechify.return_value = mock_client
        
        # Test the complete workflow
        result = text_to_audio_speechify(
            text="This is a test of the Speechify integration",
            voice_id="scott",
            model="simba-english",
            audio_format="mp3",
            language="en-US",
            loudness_normalization=True,
            text_normalization=True
        )
        
        # Verify the result
        assert result is not None
        assert Path(result).exists()
        
        # Verify the audio file has content
        with open(result, "rb") as f:
            content = f.read()
            assert len(content) > 0
    
    def test_api_key_environment_variable(self):
        """Test that the API key is properly read from environment variables."""
        # Test without API key
        with pytest.raises(ValueError, match="Speechify API key is required"):
            text_to_audio_speechify("test")
        
        # Test with API key in environment
        with patch.dict(os.environ, {"SPEECHIFY_API_KEY": "test_key"}):
            with patch('utils.Speechify') as mock_speechify:
                mock_client = Mock()
                mock_response = Mock()
                mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode()
                mock_client.tts.audio.speech.return_value = mock_response
                mock_speechify.return_value = mock_client
                
                result = text_to_audio_speechify("test")
                assert result is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 