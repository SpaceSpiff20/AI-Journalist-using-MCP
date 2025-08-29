"""
Real API tests for Speechify TTS migration.
These tests require a real SPEECHIFY_API_KEY environment variable.
"""

import os
import base64
import pytest
from pathlib import Path

# Import the functions to test
from utils import (
    text_to_audio_speechify,
    get_speechify_voices,
    filter_voice_models
)


class TestSpeechifyRealAPI:
    """Real API tests for Speechify TTS functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_text = "Testing Speechify migration with real API"
        self.audio_dir = Path("audio")
        self.audio_dir.mkdir(exist_ok=True)
        
        # Check if API key is available
        self.api_key = os.getenv("SPEECHIFY_API_KEY")
        if not self.api_key:
            pytest.skip("SPEECHIFY_API_KEY environment variable not set")
    
    def teardown_method(self):
        """Clean up test files."""
        # Clean up any test audio files
        for file in self.audio_dir.glob("speechify_tts_*.mp3"):
            try:
                file.unlink()
            except FileNotFoundError:
                pass
    
    def test_speechify_tts_real_api(self):
        """Test Speechify TTS with real API key."""
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
        
        # Verify the audio file has content
        with open(result, "rb") as f:
            content = f.read()
            assert len(content) > 1000  # sanity check audio was generated
    
    def test_speechify_tts_multilingual_model(self):
        """Test Speechify TTS with multilingual model."""
        result = text_to_audio_speechify(
            text=self.test_text,
            voice_id="scott",
            model="simba-multilingual",
            audio_format="mp3",
            language="en-US"
        )
        
        assert result is not None
        assert Path(result).exists()
    
    def test_speechify_tts_different_formats(self):
        """Test Speechify TTS with different audio formats."""
        formats = ["mp3", "wav"]
        
        for fmt in formats:
            result = text_to_audio_speechify(
                text=self.test_text,
                audio_format=fmt
            )
            assert result is not None
            assert result.endswith(f".{fmt}")
    
    def test_speechify_tts_different_languages(self):
        """Test Speechify TTS with different languages."""
        languages = ["en-US", "fr-FR", "de-DE", "es-ES"]
        
        for lang in languages:
            result = text_to_audio_speechify(
                text=self.test_text,
                language=lang
            )
            assert result is not None
            assert Path(result).exists()
    
    def test_speechify_tts_with_options(self):
        """Test Speechify TTS with different options."""
        # Test with normalization options
        result = text_to_audio_speechify(
            text=self.test_text,
            loudness_normalization=True,
            text_normalization=True
        )
        assert result is not None
        assert Path(result).exists()
        
        # Test without normalization options
        result2 = text_to_audio_speechify(
            text=self.test_text,
            loudness_normalization=False,
            text_normalization=False
        )
        assert result2 is not None
        assert Path(result2).exists()
    
    def test_get_speechify_voices_real_api(self):
        """Test getting available Speechify voices with real API."""
        voices = get_speechify_voices()
        
        # Verify we got a list of voices
        assert isinstance(voices, list)
        assert len(voices) > 0
        
        # Verify voice objects have expected attributes
        for voice in voices[:5]:  # Check first 5 voices
            assert hasattr(voice, 'gender')
            assert hasattr(voice, 'tags')
            assert hasattr(voice, 'models')
    
    def test_filter_voice_models_real_api(self):
        """Test filtering voice models with real API data."""
        voices = get_speechify_voices()
        
        if len(voices) == 0:
            pytest.skip("No voices available from API")
        
        # Test filtering by gender
        male_voices = filter_voice_models(voices, gender="male")
        female_voices = filter_voice_models(voices, gender="female")
        
        # At least one gender should have voices
        assert len(male_voices) > 0 or len(female_voices) > 0
        
        # Test filtering by locale
        en_voices = filter_voice_models(voices, locale="en-US")
        assert isinstance(en_voices, list)
    
    def test_speechify_tts_long_text(self):
        """Test Speechify TTS with longer text."""
        long_text = """
        This is a longer test text to ensure that the Speechify API can handle 
        more substantial content. It includes multiple sentences and should 
        generate a longer audio file. The text should be processed correctly 
        and the audio should be generated without errors.
        """
        
        result = text_to_audio_speechify(
            text=long_text,
            voice_id="scott",
            model="simba-english"
        )
        
        assert result is not None
        assert Path(result).exists()
        
        # Verify the audio file has content
        with open(result, "rb") as f:
            content = f.read()
            assert len(content) > 1000


class TestSpeechifyErrorHandling:
    """Test error handling with real API."""
    
    def test_speechify_tts_invalid_voice(self):
        """Test Speechify TTS with invalid voice ID."""
        with pytest.raises(Exception):
            text_to_audio_speechify(
                text="Test text",
                voice_id="invalid_voice_id"
            )
    
    def test_speechify_tts_invalid_model(self):
        """Test Speechify TTS with invalid model."""
        with pytest.raises(Exception):
            text_to_audio_speechify(
                text="Test text",
                model="invalid_model"
            )
    
    def test_speechify_tts_invalid_format(self):
        """Test Speechify TTS with invalid audio format."""
        with pytest.raises(Exception):
            text_to_audio_speechify(
                text="Test text",
                audio_format="invalid_format"
            )


if __name__ == "__main__":
    # Check if API key is available
    if not os.getenv("SPEECHIFY_API_KEY"):
        print("Warning: SPEECHIFY_API_KEY environment variable not set.")
        print("Real API tests will be skipped.")
        print("Set the environment variable to run real API tests.")
    
    # Run tests
    pytest.main([__file__, "-v"]) 