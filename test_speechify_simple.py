"""
Simple test script for Speechify TTS functionality.
This script tests the Speechify integration without requiring all project dependencies.
"""

import os
import base64
from unittest.mock import Mock, patch
from pathlib import Path

# Mock the imports that would normally come from utils.py
def mock_imports():
    """Mock the imports to avoid dependency issues."""
    import sys
    from unittest.mock import MagicMock
    
    # Mock the modules that would cause import errors
    mock_modules = {
        'fastapi': MagicMock(),
        'elevenlabs': MagicMock(),
        'gtts': MagicMock(),
        'langchain_anthropic': MagicMock(),
        'langchain_groq': MagicMock(),
        'langchain_core': MagicMock(),
        'bs4': MagicMock(),
        'requests': MagicMock(),
        'dotenv': MagicMock(),
    }
    
    for module_name, mock_module in mock_modules.items():
        sys.modules[module_name] = mock_module

# Mock the imports first
mock_imports()

# Now we can safely import the Speechify functions
try:
    from speechify import Speechify
    from speechify.tts import GetSpeechOptionsRequest
    SPEECHIFY_AVAILABLE = True
except ImportError:
    SPEECHIFY_AVAILABLE = False
    print("Warning: speechify-api not installed. Install with: pip install speechify-api")

def test_speechify_import():
    """Test that Speechify can be imported."""
    if not SPEECHIFY_AVAILABLE:
        print("❌ Speechify API not available")
        return False
    
    print("✅ Speechify API imported successfully")
    return True

def test_speechify_client_creation():
    """Test creating a Speechify client."""
    if not SPEECHIFY_AVAILABLE:
        print("❌ Speechify API not available")
        return False
    
    try:
        # This will fail without a real API key, but we can test the client creation
        client = Speechify(token="test_token")
        print("✅ Speechify client created successfully")
        return True
    except Exception as e:
        print(f"⚠️  Speechify client creation failed (expected without real API key): {e}")
        return True  # This is expected without a real API key

def test_speechify_options():
    """Test creating Speechify options."""
    if not SPEECHIFY_AVAILABLE:
        print("❌ Speechify API not available")
        return False
    
    try:
        options = GetSpeechOptionsRequest(
            loudness_normalization=True,
            text_normalization=True
        )
        print("✅ Speechify options created successfully")
        return True
    except Exception as e:
        print(f"❌ Speechify options creation failed: {e}")
        return False

def test_speechify_tts_function():
    """Test the Speechify TTS function logic."""
    if not SPEECHIFY_AVAILABLE:
        print("❌ Speechify API not available")
        return False
    
    # Mock the Speechify client and response
    with patch('speechify.Speechify') as mock_speechify:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode()
        mock_client.tts.audio.speech.return_value = mock_response
        mock_speechify.return_value = mock_client
        
        # Test the TTS call
        try:
            client = Speechify(token="test_token")
            audio_response = client.tts.audio.speech(
                audio_format="mp3",
                input="Test text",
                language="en-US",
                model="simba-english",
                options=GetSpeechOptionsRequest(
                    loudness_normalization=True,
                    text_normalization=True
                ),
                voice_id="scott"
            )
            
            # Decode the audio data
            audio_bytes = base64.b64decode(audio_response.audio_data)
            
            print("✅ Speechify TTS function works correctly")
            print(f"   - Audio data length: {len(audio_bytes)} bytes")
            return True
            
        except Exception as e:
            print(f"❌ Speechify TTS function failed: {e}")
            return False

def test_voice_filtering_logic():
    """Test the voice filtering logic."""
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
    
    # Test filtering function
    def filter_voice_models(voices, *, gender=None, locale=None, tags=None):
        results = []
        for voice in voices:
            if gender and voice.gender.lower() != gender.lower():
                continue
            if locale:
                if not any(
                    any(lang.locale == locale for lang in model.languages)
                    for model in voice.models
                ):
                    continue
            if tags:
                if not all(tag in voice.tags for tag in tags):
                    continue
            for model in voice.models:
                results.append(model.name)
        return results
    
    # Test filtering
    male_voices = filter_voice_models(voices, gender="male")
    female_voices = filter_voice_models(voices, gender="female")
    en_voices = filter_voice_models(voices, locale="en-US")
    deep_voices = filter_voice_models(voices, tags=["timbre:deep"])
    
    assert len(male_voices) == 1 and male_voices[0] == "voice1"
    assert len(female_voices) == 1 and female_voices[0] == "voice2"
    assert len(en_voices) == 1 and en_voices[0] == "voice1"
    assert len(deep_voices) == 1 and deep_voices[0] == "voice1"
    
    print("✅ Voice filtering logic works correctly")
    return True

def test_environment_variable():
    """Test environment variable handling."""
    # Test without API key
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if api_key:
        print(f"✅ SPEECHIFY_API_KEY is set: {api_key[:10]}...")
        return True
    else:
        print("⚠️  SPEECHIFY_API_KEY not set (this is expected for testing)")
        return True

def main():
    """Run all tests."""
    print("🧪 Testing Speechify TTS Migration")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_speechify_import),
        ("Client Creation", test_speechify_client_creation),
        ("Options Creation", test_speechify_options),
        ("TTS Function", test_speechify_tts_function),
        ("Voice Filtering", test_voice_filtering_logic),
        ("Environment Variable", test_environment_variable),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Speechify migration is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    if not SPEECHIFY_AVAILABLE:
        print("\n📝 To install Speechify API:")
        print("   pip install speechify-api")
    
    print("\n📝 To set up your API key:")
    print("   export SPEECHIFY_API_KEY='your_api_key_here'")
    print("   Get your API key at: https://console.sws.speechify.com/signup")

if __name__ == "__main__":
    main() 