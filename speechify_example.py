"""
Example script demonstrating Speechify TTS integration.
This script shows how to use the new Speechify TTS functionality.
"""

import os
from pathlib import Path

# Import the Speechify functions from utils
try:
    from utils import text_to_audio_speechify, get_speechify_voices, filter_voice_models
    UTILS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import from utils: {e}")
    print("This is expected if dependencies are not installed.")
    UTILS_AVAILABLE = False

def example_basic_tts():
    """Example of basic TTS generation."""
    print("🎤 Example 1: Basic TTS Generation")
    print("-" * 40)
    
    if not UTILS_AVAILABLE:
        print("❌ Utils not available - skipping example")
        return
    
    try:
        # Basic TTS with default settings
        text = "Hello, this is a test of the Speechify TTS integration!"
        audio_path = text_to_audio_speechify(text)
        
        print(f"✅ Audio generated successfully!")
        print(f"📁 File saved to: {audio_path}")
        print(f"📏 File size: {Path(audio_path).stat().st_size} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have set SPEECHIFY_API_KEY environment variable")

def example_advanced_tts():
    """Example of advanced TTS generation with custom settings."""
    print("\n🎤 Example 2: Advanced TTS Generation")
    print("-" * 40)
    
    if not UTILS_AVAILABLE:
        print("❌ Utils not available - skipping example")
        return
    
    try:
        # Advanced TTS with custom settings
        text = "This is an advanced example with custom voice settings and options."
        audio_path = text_to_audio_speechify(
            text=text,
            voice_id="scott",
            model="simba-english",
            audio_format="mp3",
            language="en-US",
            loudness_normalization=True,
            text_normalization=True
        )
        
        print(f"✅ Advanced audio generated successfully!")
        print(f"📁 File saved to: {audio_path}")
        print(f"📏 File size: {Path(audio_path).stat().st_size} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_multilingual_tts():
    """Example of multilingual TTS generation."""
    print("\n🎤 Example 3: Multilingual TTS Generation")
    print("-" * 40)
    
    if not UTILS_AVAILABLE:
        print("❌ Utils not available - skipping example")
        return
    
    # Test different languages
    languages = [
        ("en-US", "Hello, this is English text."),
        ("fr-FR", "Bonjour, ceci est du texte français."),
        ("de-DE", "Hallo, das ist deutscher Text."),
        ("es-ES", "Hola, este es texto en español.")
    ]
    
    for lang_code, text in languages:
        try:
            print(f"🌍 Testing {lang_code}: {text}")
            audio_path = text_to_audio_speechify(
                text=text,
                language=lang_code,
                model="simba-multilingual"
            )
            print(f"✅ {lang_code} audio generated: {audio_path}")
            
        except Exception as e:
            print(f"❌ {lang_code} failed: {e}")

def example_voice_management():
    """Example of voice management functionality."""
    print("\n🎤 Example 4: Voice Management")
    print("-" * 40)
    
    if not UTILS_AVAILABLE:
        print("❌ Utils not available - skipping example")
        return
    
    try:
        # Get available voices
        print("🔍 Getting available voices...")
        voices = get_speechify_voices()
        
        print(f"✅ Found {len(voices)} available voices")
        
        # Show some voice details
        for i, voice in enumerate(voices[:3]):  # Show first 3 voices
            print(f"   Voice {i+1}: {getattr(voice, 'name', 'Unknown')} ({getattr(voice, 'gender', 'Unknown')})")
        
        # Filter voices
        print("\n🔍 Filtering voices...")
        male_voices = filter_voice_models(voices, gender="male")
        female_voices = filter_voice_models(voices, gender="female")
        en_voices = filter_voice_models(voices, locale="en-US")
        
        print(f"   Male voices: {len(male_voices)}")
        print(f"   Female voices: {len(female_voices)}")
        print(f"   English voices: {len(en_voices)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_different_formats():
    """Example of generating audio in different formats."""
    print("\n🎤 Example 5: Different Audio Formats")
    print("-" * 40)
    
    if not UTILS_AVAILABLE:
        print("❌ Utils not available - skipping example")
        return
    
    text = "Testing different audio formats with Speechify."
    formats = ["mp3", "wav"]
    
    for fmt in formats:
        try:
            print(f"🔊 Testing {fmt.upper()} format...")
            audio_path = text_to_audio_speechify(
                text=text,
                audio_format=fmt
            )
            print(f"✅ {fmt.upper()} audio generated: {audio_path}")
            
        except Exception as e:
            print(f"❌ {fmt.upper()} failed: {e}")

def check_environment():
    """Check the environment setup."""
    print("🔧 Environment Check")
    print("-" * 40)
    
    # Check API key
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if api_key:
        print(f"✅ SPEECHIFY_API_KEY is set: {api_key[:10]}...")
    else:
        print("❌ SPEECHIFY_API_KEY not set")
        print("💡 Set it with: export SPEECHIFY_API_KEY='your_api_key_here'")
    
    # Check audio directory
    audio_dir = Path("audio")
    if audio_dir.exists():
        print(f"✅ Audio directory exists: {audio_dir}")
    else:
        print(f"⚠️  Audio directory will be created: {audio_dir}")
    
    # Check Speechify availability
    try:
        from speechify import Speechify
        print("✅ Speechify API is available")
    except ImportError:
        print("❌ Speechify API not installed")
        print("💡 Install with: pip install speechify-api")

def main():
    """Run all examples."""
    print("🎤 Speechify TTS Integration Examples")
    print("=" * 50)
    
    # Check environment first
    check_environment()
    
    # Run examples
    examples = [
        example_basic_tts,
        example_advanced_tts,
        example_multilingual_tts,
        example_voice_management,
        example_different_formats
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"❌ Example failed: {e}")
    
    print("\n" + "=" * 50)
    print("📝 Summary:")
    print("   - Speechify TTS integration is ready to use")
    print("   - Set SPEECHIFY_API_KEY to test with real API")
    print("   - Check SPEECHIFY_MIGRATION_GUIDE.md for detailed documentation")
    print("   - Run test_speechify_simple.py for basic testing")

if __name__ == "__main__":
    main() 