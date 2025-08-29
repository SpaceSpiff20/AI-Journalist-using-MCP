# Speechify TTS Migration Guide

This document outlines the migration from ElevenLabs to Speechify TTS API in the AI Journalist project.

## Overview

The migration adds Speechify as the primary TTS provider while maintaining backward compatibility with ElevenLabs as a fallback option.

## Changes Made

### 1. New Dependencies

Added to `requirements.txt`:
```
speechify-api==0.1.0
```

### 2. New Functions in `utils.py`

#### `text_to_audio_speechify()`
Primary TTS function using Speechify API.

**Parameters:**
- `text` (str): Text to convert to speech
- `voice_id` (str): Speechify voice ID (default: "scott")
- `model` (str): TTS model ("simba-english" or "simba-multilingual")
- `audio_format` (str): Audio format ("aac", "mp3", "ogg", "wav")
- `language` (str): Language code (e.g., "en-US", "fr-FR")
- `output_dir` (str): Directory to save audio files
- `api_key` (str): Speechify API key (uses env var if not provided)
- `loudness_normalization` (bool): Enable loudness normalization
- `text_normalization` (bool): Enable text normalization

**Returns:**
- `str`: Path to the saved audio file

#### `get_speechify_voices()`
Get available Speechify voices.

**Returns:**
- `list`: List of available voice objects

#### `filter_voice_models()`
Filter voices by gender, locale, and/or tags.

**Parameters:**
- `voices` (list): List of GetVoice objects
- `gender` (str, optional): e.g. 'male', 'female'
- `locale` (str, optional): e.g. 'en-US'
- `tags` (list, optional): list of tags, e.g. ['timbre:deep']

**Returns:**
- `list[str]`: IDs of matching voice models

### 3. Backend Updates

The `backend.py` file now:
- Tries Speechify first
- Falls back to ElevenLabs if Speechify fails
- Maintains the same API interface

### 4. Environment Variables

**Required:**
- `SPEECHIFY_API_KEY`: Your Speechify API key

**Optional (for fallback):**
- `ELEVEN_API_KEY`: ElevenLabs API key for fallback

## Installation

1. Install the new dependency:
```bash
pip install speechify-api
```

2. Or update all dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Speechify API key:
```bash
export SPEECHIFY_API_KEY="your_api_key_here"
```

## Usage Examples

### Basic TTS Generation
```python
from utils import text_to_audio_speechify

# Generate audio with default settings
audio_path = text_to_audio_speechify("Hello, world!")
print(f"Audio saved to: {audio_path}")
```

### Advanced TTS Generation
```python
from utils import text_to_audio_speechify

# Generate audio with custom settings
audio_path = text_to_audio_speechify(
    text="This is a test of the Speechify integration",
    voice_id="scott",
    model="simba-english",
    audio_format="mp3",
    language="en-US",
    loudness_normalization=True,
    text_normalization=True
)
```

### Voice Management
```python
from utils import get_speechify_voices, filter_voice_models

# Get all available voices
voices = get_speechify_voices()

# Filter voices by criteria
male_voices = filter_voice_models(voices, gender="male")
en_voices = filter_voice_models(voices, locale="en-US")
deep_voices = filter_voice_models(voices, tags=["timbre:deep"])
```

## Supported Languages

### Fully Supported:
- English (en-US)
- French (fr-FR)
- German (de-DE)
- Spanish (es-ES)
- Portuguese Brazil (pt-BR)
- Portuguese Portugal (pt-PT)

### Beta Languages:
- Arabic (ar-AE)
- Danish (da-DK)
- Dutch (nl-NL)
- Estonian (et-EE)
- Finnish (fi-FI)
- Greek (el-GR)
- Hebrew (he-IL)
- Hindi (hi-IN)
- Italian (it-IT)
- Japanese (ja-JP)
- Norwegian (nb-NO)
- Polish (pl-PL)
- Russian (ru-RU)
- Swedish (sv-SE)
- Turkish (tr-TR)
- Ukrainian (uk-UA)
- Vietnamese (vi-VN)

## Audio Formats

Supported formats:
- `aac`
- `mp3`
- `ogg`
- `wav`

## Models

Available models:
- `simba-english`: English-optimized model
- `simba-multilingual`: Multilingual model

## Backward Compatibility

The migration maintains full backward compatibility:

1. **Existing functions remain unchanged:**
   - `text_to_audio_elevenlabs_sdk()`
   - `tts_to_audio()`

2. **Fallback mechanism:**
   - If Speechify fails, the system automatically falls back to ElevenLabs
   - If both fail, gTTS is available as a final fallback

3. **API interface unchanged:**
   - The `/generate-news-audio` endpoint works exactly as before
   - No changes required in the frontend

## Testing

### Run Unit Tests
```bash
pytest test_speechify_migration.py -v
```

### Run Real API Tests
```bash
# Set your API key first
export SPEECHIFY_API_KEY="your_api_key_here"

# Run real API tests
pytest test_speechify_real_api.py -v
```

### Test Backward Compatibility
```bash
# Test that existing functions still work
pytest test_speechify_migration.py::TestBackwardCompatibility -v
```

## Error Handling

The migration includes robust error handling:

1. **Missing API Key:** Clear error message with instructions
2. **API Errors:** Graceful fallback to ElevenLabs
3. **Invalid Parameters:** Descriptive error messages
4. **Network Issues:** Automatic retry and fallback

## Performance Considerations

1. **Audio Quality:** Speechify provides high-quality audio output
2. **Speed:** Speechify is optimized for fast generation
3. **Cost:** Speechify offers competitive pricing
4. **Reliability:** Built-in fallback ensures service availability

## Troubleshooting

### Common Issues

1. **"Speechify API key is required"**
   - Set the `SPEECHIFY_API_KEY` environment variable
   - Or pass the API key directly to the function

2. **"Invalid voice_id"**
   - Use `get_speechify_voices()` to see available voices
   - Use "scott" as the default voice ID

3. **"Invalid model"**
   - Use only "simba-english" or "simba-multilingual"

4. **"Invalid audio_format"**
   - Use only "aac", "mp3", "ogg", or "wav"

### Getting Help

1. Check the Speechify documentation: https://console.sws.speechify.com/docs
2. Run the test suite to verify your setup
3. Check the logs for detailed error messages

## Migration Checklist

- [ ] Install `speechify-api` dependency
- [ ] Set `SPEECHIFY_API_KEY` environment variable
- [ ] Test basic TTS functionality
- [ ] Test fallback to ElevenLabs
- [ ] Run the test suite
- [ ] Verify audio quality meets requirements
- [ ] Update documentation if needed

## API Key Setup

1. Sign up at https://console.sws.speechify.com/signup
2. Get your API key from the console
3. Set the environment variable:
   ```bash
   export SPEECHIFY_API_KEY="your_api_key_here"
   ```
4. Test with a simple TTS call

## Future Enhancements

Potential improvements for future versions:
1. Voice cloning capabilities
2. Real-time streaming
3. Advanced audio processing options
4. Batch processing for multiple texts
5. Custom voice training 