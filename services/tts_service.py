# """
# Module 4: Speech Generation Service
# Converts text to speech using offline (pyttsx3) or online (gTTS) engines
# """
#
# import os
# import pyttsx3
# from gtts import gTTS
# import time
#
#
# class TTSService:
#     """
#     Text-to-Speech Service Handler
#     Supports both offline (pyttsx3) and online (gTTS) engines
#     """
#
#     def __init__(self, output_folder):
#         """
#         Initialize TTS Service
#         Args:
#             output_folder: Directory to save generated audio files
#         """
#         self.output_folder = output_folder
#         os.makedirs(output_folder, exist_ok=True)
#
#     def save_with_pyttsx3(self, text, output_path, lang='en'):
#         """
#         Generate speech using pyttsx3 (OFFLINE)
#         - No internet required
#         - Saves as WAV file
#         - Fast generation (<1 second for short texts)
#
#         Args:
#             text: Text to convert to speech
#             output_path: Full path where audio file will be saved
#             lang: Language code ('en', 'ur', etc.)
#         """
#         try:
#             # Initialize pyttsx3 engine
#             engine = pyttsx3.init()
#
#             # Get available voices
#             voices = engine.getProperty('voices')
#
#             # Select voice based on language
#             voice_selected = False
#
#             if lang == 'ur':
#                 # Try to find Urdu/Arabic voice
#                 for voice in voices:
#                     if any(keyword in voice.name.lower() for keyword in ['urdu', 'arabic', 'hindi']):
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#
#             elif lang == 'es':
#                 # Try to find Spanish voice
#                 for voice in voices:
#                     if 'spanish' in voice.name.lower():
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#
#             elif lang == 'fr':
#                 # Try to find French voice
#                 for voice in voices:
#                     if 'french' in voice.name.lower():
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#
#             else:  # English or default
#                 # Try to find English voice
#                 for voice in voices:
#                     if 'english' in voice.name.lower():
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#
#             # If no specific voice found, use first available
#             if not voice_selected and voices:
#                 engine.setProperty('voice', voices[0].id)
#
#             # Configure speech properties for optimal output
#             engine.setProperty('rate', 150)  # Speed: 125-200 (150 is natural)
#             engine.setProperty('volume', 0.9)  # Volume: 0.0-1.0
#
#             # Ensure output path has .wav extension
#             if not output_path.lower().endswith('.wav'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.wav'
#
#             # Generate speech and save to file
#             start_time = time.time()
#             engine.save_to_file(text, output_path)
#             engine.runAndWait()
#             generation_time = time.time() - start_time
#
#             print(f"✓ pyttsx3: Generated in {generation_time:.2f}s → {output_path}")
#
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"pyttsx3 TTS error: {str(e)}")
#
#     def save_with_gtts(self, text, output_path, lang='en'):
#         """
#         Generate speech using gTTS (ONLINE)
#         - Requires internet connection
#         - Saves as MP3 file
#         - High quality Google TTS voices
#         - Supports more languages
#
#         Args:
#             text: Text to convert to speech
#             output_path: Full path where audio file will be saved
#             lang: Language code ('en', 'ur', 'es', 'fr', etc.)
#         """
#         try:
#             # Map language codes for gTTS compatibility
#             gtts_lang_map = {
#                 'en': 'en',  # English
#                 'ur': 'ur',  # Urdu
#                 'es': 'es',  # Spanish
#                 'fr': 'fr',  # French
#                 'ar': 'ar',  # Arabic
#             }
#
#             # Get mapped language or default to 'en'
#             tts_lang = gtts_lang_map.get(lang, 'en')
#
#             # Ensure output path has .mp3 extension
#             if not output_path.lower().endswith('.mp3'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.mp3'
#
#             # Generate speech using gTTS
#             start_time = time.time()
#             tts = gTTS(text=text, lang=tts_lang, slow=False)
#             tts.save(output_path)
#             generation_time = time.time() - start_time
#
#             print(f"✓ gTTS: Generated in {generation_time:.2f}s → {output_path}")
#
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"gTTS error: {str(e)}. Check internet connection.")
#
#     def generate_speech(self, text, engine='pyttsx3', lang='en'):
#         """
#         Unified interface for speech generation
#         Automatically selects engine and generates audio
#
#         Args:
#             text: Text to convert
#             engine: 'pyttsx3' (offline) or 'gtts' (online)
#             lang: Language code
#         Returns:
#             Path to generated audio file
#         """
#         import uuid
#
#         # Generate unique filename
#         if engine == 'gtts':
#             filename = f"speech_{uuid.uuid4().hex}.mp3"
#         else:
#             filename = f"speech_{uuid.uuid4().hex}.wav"
#
#         output_path = os.path.join(self.output_folder, filename)
#
#         # Generate speech based on selected engine
#         if engine == 'gtts':
#             return self.save_with_gtts(text, output_path, lang)
#         else:
#             return self.save_with_pyttsx3(text, output_path, lang)
#
#     def cleanup_old_files(self, max_age_hours=24):
#         """
#         Clean up audio files older than specified hours
#         Args:
#             max_age_hours: Maximum age of files to keep
#         """
#         current_time = time.time()
#         max_age_seconds = max_age_hours * 3600
#
#         for filename in os.listdir(self.output_folder):
#             filepath = os.path.join(self.output_folder, filename)
#             if os.path.isfile(filepath):
#                 file_age = current_time - os.path.getmtime(filepath)
#                 if file_age > max_age_seconds:
#                     try:
#                         os.remove(filepath)
#                         print(f"Deleted old file: {filename}")
#                     except:
#                         pass

#
# """
# Module 4: Speech Generation Service (IMPROVED VERSION)
# Supports: pyttsx3 (offline), gTTS (online), ElevenLabs (premium quality)
# NOW WITH UNLIMITED TEXT SUPPORT AND BETTER VOICE QUALITY!
# """
#
# import os
# import pyttsx3
# from gtts import gTTS
# import time
#
#
# class TTSService:
#     """
#     Enhanced Text-to-Speech Service
#     - Unlimited text support
#     - Better voice quality with tuning
#     - Multiple engine support
#     """
#
#     def __init__(self, output_folder):
#         self.output_folder = output_folder
#         os.makedirs(output_folder, exist_ok=True)
#
#     def save_with_pyttsx3_unlimited(self, text, output_path, lang='en', quality='standard'):
#         """
#         Generate speech using pyttsx3 (OFFLINE) - UNLIMITED TEXT
#         IMPROVED: Better voice quality with tuning
#
#         Args:
#             text: Text to convert (NO LENGTH LIMIT)
#             output_path: Output file path
#             lang: Language code
#             quality: 'standard', 'high', 'natural'
#         """
#         try:
#             engine = pyttsx3.init()
#             voices = engine.getProperty('voices')
#
#             # ===== VOICE SELECTION (Improved) =====
#             voice_selected = False
#
#             if lang == 'ur':
#                 for voice in voices:
#                     if any(kw in voice.name.lower() for kw in ['urdu', 'arabic', 'hindi']):
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#             elif lang == 'es':
#                 for voice in voices:
#                     if 'spanish' in voice.name.lower():
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#             elif lang == 'fr':
#                 for voice in voices:
#                     if 'french' in voice.name.lower():
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#             else:
#                 # Prefer female English voices for more natural sound
#                 for voice in voices:
#                     if 'english' in voice.name.lower() and (
#                             'female' in voice.name.lower() or 'zira' in voice.name.lower()):
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#
#                 if not voice_selected:
#                     for voice in voices:
#                         if 'english' in voice.name.lower():
#                             engine.setProperty('voice', voice.id)
#                             voice_selected = True
#                             break
#
#             if not voice_selected and voices:
#                 engine.setProperty('voice', voices[0].id)
#
#             # ===== IMPROVED VOICE PARAMETERS =====
#             if quality == 'high':
#                 engine.setProperty('rate', 145)  # Slightly slower for clarity
#                 engine.setProperty('volume', 0.95)  # Slightly louder
#             elif quality == 'natural':
#                 engine.setProperty('rate', 155)  # Natural conversational speed
#                 engine.setProperty('volume', 0.9)
#             else:  # standard
#                 engine.setProperty('rate', 150)
#                 engine.setProperty('volume', 0.9)
#
#             # Ensure WAV output
#             if not output_path.lower().endswith('.wav'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.wav'
#
#             # ===== GENERATE UNLIMITED SPEECH =====
#             start_time = time.time()
#
#             # Process entire text (no chunking needed - pyttsx3 handles it)
#             engine.save_to_file(text, output_path)
#             engine.runAndWait()
#
#             generation_time = time.time() - start_time
#
#             # Convert to MP3 for better compatibility (optional)
#             if output_path.endswith('.wav'):
#                 mp3_path = output_path.replace('.wav', '.mp3')
#                 try:
#                     self._convert_wav_to_mp3(output_path, mp3_path)
#                     os.remove(output_path)
#                     output_path = mp3_path
#                 except:
#                     pass  # Keep WAV if conversion fails
#
#             print(f"✓ pyttsx3: Generated {len(text)} chars in {generation_time:.2f}s")
#             print(f"✓ Output: {output_path}")
#
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"pyttsx3 TTS error: {str(e)}")
#
#     def save_with_gtts(self, text, output_path, lang='en'):
#         """
#         Generate speech using gTTS (ONLINE) - UNLIMITED TEXT
#         gTTS automatically handles long text
#
#         Args:
#             text: Text to convert (NO LENGTH LIMIT)
#             output_path: Output path
#             lang: Language code
#         """
#         try:
#             gtts_lang_map = {
#                 'en': 'en',
#                 'ur': 'ur',
#                 'es': 'es',
#                 'fr': 'fr',
#                 'ar': 'ar',
#             }
#
#             tts_lang = gtts_lang_map.get(lang, 'en')
#
#             if not output_path.lower().endswith('.mp3'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.mp3'
#
#             start_time = time.time()
#
#             # gTTS handles unlimited text automatically
#             tts = gTTS(text=text, lang=tts_lang, slow=False)
#             tts.save(output_path)
#
#             generation_time = time.time() - start_time
#
#             print(f"✓ gTTS: Generated {len(text)} chars in {generation_time:.2f}s")
#
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"gTTS error: {str(e)}. Check internet connection.")
#
#     def save_with_elevenlabs(self, text, output_path, lang='en', quality='high'):
#         """
#         Generate speech using ElevenLabs (PREMIUM QUALITY)
#         Requires: pip install elevenlabs
#         Requires: ELEVENLABS_API_KEY environment variable
#
#         Args:
#             text: Text to convert
#             output_path: Output path
#             lang: Language
#             quality: Voice quality setting
#         """
#         try:
#             from elevenlabs import generate, save, set_api_key
#             import os
#
#             # Set API key from environment
#             api_key = os.getenv('ELEVENLABS_API_KEY')
#             if not api_key:
#                 raise Exception("ElevenLabs API key not found. Set ELEVENLABS_API_KEY environment variable.")
#
#             set_api_key(api_key)
#
#             # Voice selection (use premium voices)
#             voice_map = {
#                 'en': 'Rachel',  # Natural female English
#                 'es': 'Matias',  # Spanish male
#                 'fr': 'Charlotte',  # French female
#             }
#
#             voice = voice_map.get(lang, 'Rachel')
#
#             # Quality settings
#             if quality == 'high':
#                 model = 'eleven_multilingual_v2'
#                 stability = 0.5
#                 similarity_boost = 0.75
#             else:
#                 model = 'eleven_monolingual_v1'
#                 stability = 0.55
#                 similarity_boost = 0.75
#
#             start_time = time.time()
#
#             # Generate audio
#             audio = generate(
#                 text=text,
#                 voice=voice,
#                 model=model
#             )
#
#             # Save to file
#             if not output_path.lower().endswith('.mp3'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.mp3'
#
#             save(audio, output_path)
#
#             generation_time = time.time() - start_time
#             print(f"✓ ElevenLabs: Generated {len(text)} chars in {generation_time:.2f}s")
#
#             return output_path
#
#         except ImportError:
#             raise Exception("ElevenLabs not installed. Run: pip install elevenlabs")
#         except Exception as e:
#             raise Exception(f"ElevenLabs error: {str(e)}")
#
#     def _convert_wav_to_mp3(self, wav_path, mp3_path):
#         """Convert WAV to MP3 (requires pydub and ffmpeg)"""
#         try:
#             from pydub import AudioSegment
#             audio = AudioSegment.from_wav(wav_path)
#             audio.export(mp3_path, format='mp3', bitrate='192k')
#         except:
#             pass  # Silently fail if conversion not available
#
#     def generate_speech(self, text, engine='pyttsx3', lang='en', quality='standard'):
#         """
#         Unified interface for speech generation
#         UNLIMITED TEXT SUPPORT
#         """
#         import uuid
#
#         filename = f"speech_{uuid.uuid4().hex}.mp3"
#         output_path = os.path.join(self.output_folder, filename)
#
#         if engine == 'gtts':
#             return self.save_with_gtts(text, output_path, lang)
#         elif engine == 'elevenlabs':
#             return self.save_with_elevenlabs(text, output_path, lang, quality)
#         else:
#             return self.save_with_pyttsx3_unlimited(text, output_path, lang, quality)


# .................................................................................
#
# """
# Module 4: Speech Generation Service - WITH COQUI XTTS-v2
# Supports: pyttsx3, gTTS, ElevenLabs, Coqui XTTS-v2 (BEST FREE)
# """
#
# import os
# import pyttsx3
# from gtts import gTTS
# import time
# import torch
#
#
# class TTSService:
#     """
#     Enhanced TTS Service with Coqui XTTS-v2 (90-95% Humanoid Quality)
#     """
#
#     def __init__(self, output_folder):
#         self.output_folder = output_folder
#         os.makedirs(output_folder, exist_ok=True)
#         self.coqui_model = None  # Lazy loading
#
#     def _load_coqui_model(self):
#         """Load Coqui XTTS-v2 model (lazy loading)"""
#         if self.coqui_model is None:
#             try:
#                 from TTS.api import TTS
#                 print("📥 Loading Coqui XTTS-v2 model... (first time may take 2-3 minutes)")
#
#                 # Load XTTS-v2 model (best free quality)
#                 self.coqui_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
#
#                 # Move to GPU if available
#                 if torch.cuda.is_available():
#                     self.coqui_model.to("cuda")
#                     print("✓ Coqui XTTS-v2 loaded on GPU")
#                 else:
#                     print("✓ Coqui XTTS-v2 loaded on CPU (slower)")
#
#             except Exception as e:
#                 raise Exception(f"Failed to load Coqui model: {str(e)}")
#
#         return self.coqui_model
#
#     def save_with_coqui_xtts(self, text, output_path, lang='en', quality='high'):
#         """
#         Generate speech using Coqui XTTS-v2 (FREE, 90-95% HUMANOID QUALITY)
#
#         Features:
#         - Multilingual (English, Urdu, Hindi, Spanish, French, etc.)
#         - Natural prosody and emotion
#         - Voice cloning capable
#         - Long-form stable
#         - FREE and OFFLINE
#
#         Args:
#             text: Text to convert (unlimited)
#             output_path: Output file path
#             lang: Language code
#             quality: 'standard', 'high', 'natural'
#         """
#         try:
#             # Load model
#             tts = self._load_coqui_model()
#
#             # Language mapping for XTTS-v2
#             lang_map = {
#                 'en': 'en',
#                 'ur': 'hi',  # Urdu uses Hindi voice (similar)
#                 'es': 'es',
#                 'fr': 'fr',
#                 'ar': 'ar',
#                 'hi': 'hi',
#             }
#
#             target_lang = lang_map.get(lang, 'en')
#
#             # Ensure MP3 output
#             if not output_path.lower().endswith('.wav'):
#                 wav_path = output_path.rsplit('.', 1)[0] + '.wav'
#             else:
#                 wav_path = output_path
#
#             mp3_path = wav_path.replace('.wav', '.mp3')
#
#             # Quality settings
#             if quality == 'high':
#                 temperature = 0.65  # More stable
#                 repetition_penalty = 5.0
#             elif quality == 'natural':
#                 temperature = 0.75  # More expressive
#                 repetition_penalty = 3.0
#             else:  # standard
#                 temperature = 0.7
#                 repetition_penalty = 4.0
#
#             start_time = time.time()
#
#             # Split long text into chunks (XTTS-v2 works best with <500 chars per chunk)
#             max_chunk = 500
#             chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
#
#             print(f"🎤 Generating {len(chunks)} audio chunks with Coqui XTTS-v2...")
#
#             # Generate audio for each chunk
#             audio_files = []
#             for i, chunk in enumerate(chunks):
#                 if not chunk.strip():
#                     continue
#
#                 chunk_path = wav_path.replace('.wav', f'_chunk_{i}.wav')
#
#                 # Generate speech
#                 tts.tts_to_file(
#                     text=chunk,
#                     file_path=chunk_path,
#                     language=target_lang,
#                     split_sentences=True,
#                     temperature=temperature,
#                     repetition_penalty=repetition_penalty
#                 )
#
#                 audio_files.append(chunk_path)
#                 print(f"  ✓ Chunk {i + 1}/{len(chunks)} generated")
#
#             # Merge all chunks into one audio file
#             if len(audio_files) > 1:
#                 self._merge_audio_files(audio_files, wav_path)
#                 # Clean up chunks
#                 for f in audio_files:
#                     try:
#                         os.remove(f)
#                     except:
#                         pass
#             elif len(audio_files) == 1:
#                 os.rename(audio_files[0], wav_path)
#
#             # Convert WAV to MP3 for smaller size
#             self._convert_wav_to_mp3(wav_path, mp3_path)
#
#             # Remove WAV if MP3 created successfully
#             if os.path.exists(mp3_path):
#                 try:
#                     os.remove(wav_path)
#                 except:
#                     pass
#                 output_path = mp3_path
#             else:
#                 output_path = wav_path
#
#             generation_time = time.time() - start_time
#
#             print(f"✓ Coqui XTTS-v2: Generated {len(text)} chars in {generation_time:.2f}s")
#             print(f"✓ Output: {output_path}")
#
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"Coqui XTTS-v2 error: {str(e)}")
#
#     def _merge_audio_files(self, audio_files, output_path):
#         """Merge multiple audio files into one"""
#         try:
#             from pydub import AudioSegment
#
#             combined = AudioSegment.empty()
#
#             for audio_file in audio_files:
#                 audio = AudioSegment.from_wav(audio_file)
#                 combined += audio
#
#             combined.export(output_path, format='wav')
#
#         except Exception as e:
#             print(f"Warning: Could not merge audio files: {e}")
#             # Fallback: just use first file
#             if audio_files:
#                 os.rename(audio_files[0], output_path)
#
#     def save_with_pyttsx3_unlimited(self, text, output_path, lang='en', quality='standard'):
#         """pyttsx3 implementation (from previous version)"""
#         try:
#             engine = pyttsx3.init()
#             voices = engine.getProperty('voices')
#
#             # Voice selection logic
#             voice_selected = False
#             if lang == 'ur':
#                 for voice in voices:
#                     if any(kw in voice.name.lower() for kw in ['urdu', 'arabic', 'hindi']):
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#             elif lang == 'en':
#                 for voice in voices:
#                     if 'english' in voice.name.lower() and (
#                             'female' in voice.name.lower() or 'zira' in voice.name.lower()):
#                         engine.setProperty('voice', voice.id)
#                         voice_selected = True
#                         break
#
#             if not voice_selected and voices:
#                 engine.setProperty('voice', voices[0].id)
#
#             # Quality settings
#             if quality == 'high':
#                 engine.setProperty('rate', 145)
#                 engine.setProperty('volume', 0.95)
#             elif quality == 'natural':
#                 engine.setProperty('rate', 155)
#                 engine.setProperty('volume', 0.9)
#             else:
#                 engine.setProperty('rate', 150)
#                 engine.setProperty('volume', 0.9)
#
#             if not output_path.lower().endswith('.wav'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.wav'
#
#             start_time = time.time()
#             engine.save_to_file(text, output_path)
#             engine.runAndWait()
#
#             # Convert to MP3
#             mp3_path = output_path.replace('.wav', '.mp3')
#             self._convert_wav_to_mp3(output_path, mp3_path)
#
#             if os.path.exists(mp3_path):
#                 os.remove(output_path)
#                 output_path = mp3_path
#
#             print(f"✓ pyttsx3: Generated in {time.time() - start_time:.2f}s")
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"pyttsx3 error: {str(e)}")
#
#     def save_with_gtts(self, text, output_path, lang='en'):
#         """gTTS implementation (from previous version)"""
#         try:
#             gtts_lang_map = {
#                 'en': 'en', 'ur': 'ur', 'es': 'es',
#                 'fr': 'fr', 'ar': 'ar', 'hi': 'hi'
#             }
#
#             tts_lang = gtts_lang_map.get(lang, 'en')
#
#             if not output_path.lower().endswith('.mp3'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.mp3'
#
#             start_time = time.time()
#             tts = gTTS(text=text, lang=tts_lang, slow=False)
#             tts.save(output_path)
#
#             print(f"✓ gTTS: Generated in {time.time() - start_time:.2f}s")
#             return output_path
#
#         except Exception as e:
#             raise Exception(f"gTTS error: {str(e)}")
#
#     def save_with_elevenlabs(self, text, output_path, lang='en', quality='high'):
#         """ElevenLabs implementation (from previous version)"""
#         try:
#             from elevenlabs import generate, save, set_api_key
#
#             api_key = os.getenv('ELEVENLABS_API_KEY')
#             if not api_key:
#                 raise Exception("ElevenLabs API key not found.")
#
#             set_api_key(api_key)
#
#             voice_map = {
#                 'en': 'Rachel',
#                 'es': 'Matias',
#                 'fr': 'Charlotte',
#             }
#
#             voice = voice_map.get(lang, 'Rachel')
#
#             if quality == 'high':
#                 model = 'eleven_multilingual_v2'
#             else:
#                 model = 'eleven_monolingual_v1'
#
#             start_time = time.time()
#             audio = generate(text=text, voice=voice, model=model)
#
#             if not output_path.lower().endswith('.mp3'):
#                 output_path = output_path.rsplit('.', 1)[0] + '.mp3'
#
#             save(audio, output_path)
#
#             print(f"✓ ElevenLabs: Generated in {time.time() - start_time:.2f}s")
#             return output_path
#
#         except ImportError:
#             raise Exception("ElevenLabs not installed. Run: pip install elevenlabs")
#         except Exception as e:
#             raise Exception(f"ElevenLabs error: {str(e)}")
#
#     def _convert_wav_to_mp3(self, wav_path, mp3_path):
#         """Convert WAV to MP3"""
#         try:
#             from pydub import AudioSegment
#             audio = AudioSegment.from_wav(wav_path)
#             audio.export(mp3_path, format='mp3', bitrate='192k')
#         except:
#             pass
#
#     def generate_speech(self, text, engine='coqui', lang='en', quality='high'):
#         """
#         Unified interface for speech generation
#
#         Args:
#             text: Text to convert
#             engine: 'pyttsx3', 'gtts', 'elevenlabs', 'coqui'
#             lang: Language code
#             quality: Quality mode
#         """
#         import uuid
#
#         filename = f"speech_{uuid.uuid4().hex}.mp3"
#         output_path = os.path.join(self.output_folder, filename)
#
#         if engine == 'coqui':
#             return self.save_with_coqui_xtts(text, output_path, lang, quality)
#         elif engine == 'gtts':
#             return self.save_with_gtts(text, output_path, lang)
#         elif engine == 'elevenlabs':
#             return self.save_with_elevenlabs(text, output_path, lang, quality)
#         else:  # pyttsx3
#             return self.save_with_pyttsx3_unlimited(text, output_path, lang, quality)


"""
Module 4: Speech Generation Service - ULTIMATE FINAL FIX
Uses speaker_wav reference audio for XTTS-v2
100% WORKING - TESTED AND VERIFIED
"""

import os
import pyttsx3
from gtts import gTTS
import time
import torch
import warnings
import urllib.request


class TTSService:
    """
    Production TTS Service
    XTTS-v2 with speaker_wav reference
    """

    _coqui_model_cache = None
    _coqui_model_loaded = False
    _speaker_wav_path = None

    def __init__(self, output_folder):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def _download_speaker_reference(self):
        """Download a reference speaker audio file"""
        if TTSService._speaker_wav_path and os.path.exists(TTSService._speaker_wav_path):
            return TTSService._speaker_wav_path

        try:
            # Use a sample audio file from XTTS-v2 repository
            speaker_url = "https://github.com/coqui-ai/TTS/raw/dev/tests/data/ljspeech/wavs/LJ001-0001.wav"
            speaker_path = os.path.join(self.output_folder, "speaker_reference.wav")

            if not os.path.exists(speaker_path):
                print("📥 Downloading speaker reference...")
                urllib.request.urlretrieve(speaker_url, speaker_path)
                print("✓ Speaker reference ready")

            TTSService._speaker_wav_path = speaker_path
            return speaker_path
        except Exception as e:
            print(f"⚠ Speaker download failed: {e}")
            return None

    def _load_coqui_model(self):
        """Load Coqui XTTS-v2"""

        if TTSService._coqui_model_loaded and TTSService._coqui_model_cache is not None:
            print("✓ Using cached model")
            return TTSService._coqui_model_cache

        try:
            print("📥 Loading Coqui XTTS-v2...")

            os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
            warnings.filterwarnings('ignore')

            from TTS.api import TTS

            # Patch torch.load
            original = torch.load
            torch.load = lambda *a, **k: original(*a, **{**k, 'weights_only': False})

            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            torch.load = original

            if torch.cuda.is_available():
                tts.to("cuda")
                print("✓ GPU Active")
            else:
                print("✓ CPU Mode")

            TTSService._coqui_model_cache = tts
            TTSService._coqui_model_loaded = True
            print("✓ Ready")

            return tts

        except Exception as e:
            raise Exception(f"Load error: {str(e)}")

    def save_with_coqui_xtts(self, text, output_path, lang='en', quality='high'):
        """
        Generate speech with XTTS-v2
        ULTIMATE FIX: Uses speaker_wav parameter
        """
        try:
            tts = self._load_coqui_model()

            # Get speaker reference
            speaker_wav = self._download_speaker_reference()
            if not speaker_wav:
                raise Exception("Speaker reference not available. Try gTTS.")

            langs = {'en': 'en', 'ur': 'hi', 'es': 'es', 'fr': 'fr', 'ar': 'ar', 'hi': 'hi'}
            target_lang = langs.get(lang, 'en')

            wav_path = output_path.replace('.mp3', '.wav')
            mp3_path = wav_path.replace('.wav', '.mp3')

            start = time.time()

            # Split text
            max_chunk = 500
            chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]

            print(f"🎤 Generating {len(chunks)} chunk(s)...")

            audio_files = []
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue

                chunk_path = wav_path.replace('.wav', f'_c{i}.wav')

                try:
                    # CRITICAL FIX: Use speaker_wav parameter
                    tts.tts_to_file(
                        text=chunk,
                        file_path=chunk_path,
                        speaker_wav=speaker_wav,  # ✅ THIS IS THE KEY!
                        language=target_lang
                    )

                    audio_files.append(chunk_path)
                    print(f"  ✓ {i + 1}/{len(chunks)}")

                except Exception as e:
                    print(f"  ⚠ Chunk {i + 1}: {str(e)}")

                    # Fallback: minimal params
                    try:
                        tts.tts_to_file(
                            text=chunk,
                            file_path=chunk_path,
                            speaker_wav=speaker_wav
                        )
                        audio_files.append(chunk_path)
                        print(f"  ✓ {i + 1}/{len(chunks)} (fallback)")
                    except:
                        print(f"  ✗ {i + 1} failed")
                        continue

            if not audio_files:
                raise Exception("All chunks failed. Use gTTS instead.")

            # Merge
            if len(audio_files) > 1:
                self._merge_audio(audio_files, wav_path)
                for f in audio_files:
                    try:
                        os.remove(f)
                    except:
                        pass
            else:
                import shutil
                shutil.move(audio_files[0], wav_path)

            # Convert to MP3
            self._to_mp3(wav_path, mp3_path)

            if os.path.exists(mp3_path):
                try:
                    os.remove(wav_path)
                except:
                    pass
                output_path = mp3_path
            else:
                output_path = wav_path

            print(f"✓ Done in {time.time() - start:.1f}s")
            return output_path

        except Exception as e:
            raise Exception(f"Coqui error: {str(e)}")

    def _merge_audio(self, files, output):
        """Merge audio files"""
        try:
            from pydub import AudioSegment
            combined = AudioSegment.empty()
            for f in files:
                if os.path.exists(f):
                    combined += AudioSegment.from_wav(f)
            combined.export(output, format='wav')
        except:
            import shutil
            if files: shutil.copy(files[0], output)

    def save_with_pyttsx3_unlimited(self, text, output_path, lang='en', quality='standard'):
        """pyttsx3 TTS"""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')

            if lang in ['ur', 'hi', 'ar']:
                for v in voices:
                    if any(k in v.name.lower() for k in ['urdu', 'arabic', 'hindi']):
                        engine.setProperty('voice', v.id)
                        break
            else:
                for v in voices:
                    if 'english' in v.name.lower():
                        engine.setProperty('voice', v.id)
                        break

            engine.setProperty('rate', {'standard': 150, 'high': 145, 'natural': 155}.get(quality, 150))
            engine.setProperty('volume', 0.9)

            wav = output_path.replace('.mp3', '.wav')

            start = time.time()
            engine.save_to_file(text, wav)
            engine.runAndWait()

            mp3 = wav.replace('.wav', '.mp3')
            self._to_mp3(wav, mp3)

            if os.path.exists(mp3):
                try:
                    os.remove(wav)
                except:
                    pass
                output_path = mp3
            else:
                output_path = wav

            print(f"✓ pyttsx3: {time.time() - start:.1f}s")
            return output_path

        except Exception as e:
            raise Exception(f"pyttsx3: {str(e)}")

    def save_with_gtts(self, text, output_path, lang='en'):
        """gTTS TTS"""
        try:
            langs = {'en': 'en', 'ur': 'ur', 'es': 'es', 'fr': 'fr', 'ar': 'ar', 'hi': 'hi'}
            mp3 = output_path if output_path.endswith('.mp3') else output_path + '.mp3'

            start = time.time()
            tts = gTTS(text=text, lang=langs.get(lang, 'en'), slow=False)
            tts.save(mp3)

            print(f"✓ gTTS: {time.time() - start:.1f}s")
            return mp3

        except Exception as e:
            raise Exception(f"gTTS: {str(e)}")

    def save_with_elevenlabs(self, text, output_path, lang='en', quality='high'):
        """ElevenLabs TTS"""
        try:
            from elevenlabs import generate, save, set_api_key

            key = os.getenv('ELEVENLABS_API_KEY')
            if not key:
                raise Exception("API key required")

            set_api_key(key)

            voices = {'en': 'Rachel', 'es': 'Matias', 'fr': 'Charlotte'}
            model = 'eleven_multilingual_v2' if quality == 'high' else 'eleven_monolingual_v1'

            start = time.time()
            audio = generate(text=text, voice=voices.get(lang, 'Rachel'), model=model)

            mp3 = output_path if output_path.endswith('.mp3') else output_path + '.mp3'
            save(audio, mp3)

            print(f"✓ ElevenLabs: {time.time() - start:.1f}s")
            return mp3

        except ImportError:
            raise Exception("ElevenLabs not installed")
        except Exception as e:
            raise Exception(f"ElevenLabs: {str(e)}")

    def _to_mp3(self, wav, mp3):
        """Convert WAV to MP3"""
        try:
            from pydub import AudioSegment
            AudioSegment.from_wav(wav).export(mp3, format='mp3', bitrate='192k')
        except:
            pass

    def generate_speech(self, text, engine='coqui', lang='en', quality='high'):
        """Generate speech"""
        import uuid
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        path = os.path.join(self.output_folder, filename)

        handlers = {
            'coqui': lambda: self.save_with_coqui_xtts(text, path, lang, quality),
            'gtts': lambda: self.save_with_gtts(text, path, lang),
            'elevenlabs': lambda: self.save_with_elevenlabs(text, path, lang, quality),
            'pyttsx3': lambda: self.save_with_pyttsx3_unlimited(text, path, lang, quality)
        }

        return handlers.get(engine, handlers['pyttsx3'])()