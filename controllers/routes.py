# """
# Controller: Routes and Request Handling
# Handles all HTTP routes and user interactions
# """
#
# from flask import Blueprint, render_template, request, current_app, send_from_directory, url_for
# from werkzeug.utils import secure_filename
# import os
# import uuid
# from services.extractor import extract_text_from_file, clean_text
# from services.language_detector import detect_language, preprocess_text
# from services.tts_service import TTSService
#
# bp = Blueprint('routes', __name__)
#
# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.png', '.jpg', '.jpeg', '.txt', '.bmp', '.tiff'}
#
#
# def allowed_file(filename):
#     """Check if file extension is allowed"""
#     if '.' not in filename:
#         return False
#     ext = '.' + filename.rsplit('.', 1)[1].lower()
#     return ext in ALLOWED_EXTENSIONS
#
#
# @bp.route('/')
# def index():
#     """Render homepage (Module 1)"""
#     return render_template('index.html')
#
#
# @bp.route('/process', methods=['POST'])
# def process():
#     """
#     Main processing route (Modules 1-5)
#     Handles: File Upload → Text Extraction → Language Detection → TTS → Playback
#     """
#     try:
#         # ===== MODULE 1: Input & File Handling =====
#         text_input = request.form.get('text_input', '').strip()
#         language = request.form.get('language', 'auto')  # 'en', 'ur', or 'auto'
#         tts_engine = request.form.get('tts_engine', 'pyttsx3')  # 'pyttsx3' or 'gtts'
#         uploaded_file = request.files.get('file')
#
#         extracted_text = ''
#
#         # Process uploaded file if present
#         if uploaded_file and uploaded_file.filename:
#             filename = secure_filename(uploaded_file.filename)
#
#             if not allowed_file(filename):
#                 return render_template('index.html',
#                                        error="Invalid file type. Allowed: PDF, DOCX, TXT, Images"), 400
#
#             # Save file temporarily with unique name
#             temp_filename = f"{uuid.uuid4().hex}_{filename}"
#             temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
#             uploaded_file.save(temp_path)
#
#             # ===== MODULE 2: Text Extraction & Cleaning =====
#             try:
#                 extracted_text = extract_text_from_file(temp_path)
#             except Exception as e:
#                 return render_template('index.html',
#                                        error=f"Text extraction failed: {str(e)}"), 500
#             finally:
#                 # Clean up temporary file
#                 try:
#                     os.remove(temp_path)
#                 except:
#                     pass
#
#         # Combine text input and extracted text
#         if text_input:
#             if extracted_text:
#                 final_text = text_input + '\n\n' + extracted_text
#             else:
#                 final_text = text_input
#         else:
#             final_text = extracted_text
#
#         if not final_text.strip():
#             return render_template('index.html',
#                                    error="No text provided. Please enter text or upload a file."), 400
#
#         # Clean the text (Module 2)
#         cleaned_text = clean_text(final_text)
#
#         # ===== MODULE 3: Language Detection & Preprocessing =====
#         if language == 'auto':
#             detected_lang = detect_language(cleaned_text)
#             language = detected_lang if detected_lang else 'en'
#
#         # Preprocess text for TTS
#         preprocessed_text = preprocess_text(cleaned_text, language)
#
#         # Limit text length for demo (first 1000 characters)
#         # Remove this limit in production or implement chunking
#         if len(preprocessed_text) > 1000:
#             preprocessed_text = preprocessed_text[:1000] + "..."
#             display_text = cleaned_text[:1000] + "..."
#         else:
#             display_text = cleaned_text
#
#         # ===== MODULE 4: Speech Generation (TTS Engine) =====
#         tts_service = TTSService(output_folder=current_app.config['OUTPUT_FOLDER'])
#
#         # Generate unique filename
#         if tts_engine == 'gtts':
#             output_filename = f"{uuid.uuid4().hex}.mp3"
#         else:
#             output_filename = f"{uuid.uuid4().hex}.wav"
#
#         output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename)
#
#         try:
#             if tts_engine == 'gtts':
#                 # Online TTS (gTTS)
#                 tts_service.save_with_gtts(preprocessed_text, output_path, lang=language)
#             else:
#                 # Offline TTS (pyttsx3)
#                 tts_service.save_with_pyttsx3(preprocessed_text, output_path, lang=language)
#         except Exception as e:
#             return render_template('index.html',
#                                    error=f"TTS generation failed: {str(e)}"), 500
#
#         # ===== MODULE 5: Playback (Return audio to frontend) =====
#         audio_url = url_for('routes.serve_audio', filename=output_filename)
#
#         return render_template('index.html',
#                                audio_url=audio_url,
#                                text=display_text,
#                                language=language,
#                                tts_engine=tts_engine,
#                                success=True)
#
#     except Exception as e:
#         return render_template('index.html',
#                                error=f"An error occurred: {str(e)}"), 500
#
#
# @bp.route('/outputs/<filename>')
# def serve_audio(filename):
#     """
#     Serve generated audio files (Module 5: Playback)
#     """
#     try:
#         return send_from_directory(current_app.config['OUTPUT_FOLDER'],
#                                    filename,
#                                    as_attachment=False)
#     except FileNotFoundError:
#         return "Audio file not found", 404
#
#
# @bp.route('/cleanup', methods=['POST'])
# def cleanup():
#     """Optional: Clean up old audio files"""
#     try:
#         output_folder = current_app.config['OUTPUT_FOLDER']
#         for filename in os.listdir(output_folder):
#             file_path = os.path.join(output_folder, filename)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#         return {"success": True, "message": "Cleanup completed"}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500




# """
# Controller: Routes and Request Handling
# Handles all HTTP routes and user interactions
# """
#
# from flask import Blueprint, render_template, request, current_app, send_from_directory, url_for
# from werkzeug.utils import secure_filename
# import os
# import uuid
# from services.extractor import extract_text_from_file, clean_text
# from services.language_detector import detect_language, preprocess_text, split_text_into_chunks
# from services.tts_service import TTSService
#
# bp = Blueprint('routes', __name__)
#
# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.png', '.jpg', '.jpeg', '.txt', '.bmp', '.tiff'}
#
#
# def allowed_file(filename):
#     """Check if file extension is allowed"""
#     if '.' not in filename:
#         return False
#     ext = '.' + filename.rsplit('.', 1)[1].lower()
#     return ext in ALLOWED_EXTENSIONS
#
#
# @bp.route('/')
# def index():
#     """Render homepage (Module 1)"""
#     return render_template('index.html')
#
#
# @bp.route('/process', methods=['POST'])
# def process():
#     """
#     Main processing route (Modules 1-5)
#     Handles: File Upload → Text Extraction → Language Detection → TTS → Playback
#     NOW SUPPORTS UNLIMITED TEXT LENGTH!
#     """
#     try:
#         # ===== MODULE 1: Input & File Handling =====
#         text_input = request.form.get('text_input', '').strip()
#         language = request.form.get('language', 'auto')
#         tts_engine = request.form.get('tts_engine', 'pyttsx3')
#         voice_quality = request.form.get('voice_quality', 'standard')  # NEW: Voice quality
#         uploaded_file = request.files.get('file')
#
#         extracted_text = ''
#
#         # Process uploaded file if present
#         if uploaded_file and uploaded_file.filename:
#             filename = secure_filename(uploaded_file.filename)
#
#             if not allowed_file(filename):
#                 return render_template('index.html',
#                                        error="Invalid file type. Allowed: PDF, DOCX, TXT, Images"), 400
#
#             # Save file temporarily with unique name
#             temp_filename = f"{uuid.uuid4().hex}_{filename}"
#             temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
#             uploaded_file.save(temp_path)
#
#             # ===== MODULE 2: Text Extraction & Cleaning =====
#             # IMPROVED: Extract ALL text without limits
#             try:
#                 extracted_text = extract_text_from_file(temp_path)
#                 print(f"✓ Extracted {len(extracted_text)} characters from file")
#             except Exception as e:
#                 return render_template('index.html',
#                                        error=f"Text extraction failed: {str(e)}"), 500
#             finally:
#                 # Clean up temporary file
#                 try:
#                     os.remove(temp_path)
#                 except:
#                     pass
#
#         # Combine text input and extracted text
#         if text_input:
#             if extracted_text:
#                 final_text = text_input + '\n\n' + extracted_text
#             else:
#                 final_text = text_input
#         else:
#             final_text = extracted_text
#
#         if not final_text.strip():
#             return render_template('index.html',
#                                    error="No text provided. Please enter text or upload a file."), 400
#
#         # Clean the text (Module 2)
#         cleaned_text = clean_text(final_text)
#
#         # ===== MODULE 3: Language Detection & Preprocessing =====
#         if language == 'auto':
#             detected_lang = detect_language(cleaned_text)
#             language = detected_lang if detected_lang else 'en'
#
#         # Preprocess text for TTS
#         preprocessed_text = preprocess_text(cleaned_text, language)
#
#         # REMOVED: Text length limit - process ALL text now!
#         # Split into chunks for better processing if needed
#         text_chunks = split_text_into_chunks(preprocessed_text, max_chunk_size=5000)
#
#         print(f"✓ Processing {len(text_chunks)} chunks of text")
#         print(f"✓ Total text length: {len(preprocessed_text)} characters")
#
#         # ===== MODULE 4: Speech Generation (TTS Engine) =====
#         tts_service = TTSService(output_folder=current_app.config['OUTPUT_FOLDER'])
#
#         # Generate unique filename
#         output_filename = f"{uuid.uuid4().hex}.mp3"
#         output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename)
#
#         try:
#             # IMPROVED: Generate speech for ALL text (unlimited)
#             if tts_engine == 'gtts':
#                 # Online TTS (gTTS) - handles long text automatically
#                 tts_service.save_with_gtts(preprocessed_text, output_path, lang=language)
#             elif tts_engine == 'elevenlabs':
#                 # ElevenLabs (High quality, neural)
#                 tts_service.save_with_elevenlabs(preprocessed_text, output_path, lang=language, quality=voice_quality)
#             else:
#                 # Offline TTS (pyttsx3) - process in chunks if needed
#                 tts_service.save_with_pyttsx3_unlimited(
#                     preprocessed_text,
#                     output_path,
#                     lang=language,
#                     quality=voice_quality
#                 )
#         except Exception as e:
#             return render_template('index.html',
#                                    error=f"TTS generation failed: {str(e)}"), 500
#
#         # ===== MODULE 5: Playback (Return audio to frontend) =====
#         audio_url = url_for('routes.serve_audio', filename=output_filename)
#
#         # Show text stats
#         word_count = len(preprocessed_text.split())
#         char_count = len(preprocessed_text)
#
#         return render_template('index.html',
#                                audio_url=audio_url,
#                                text=cleaned_text[:1000] + ("..." if len(cleaned_text) > 1000 else ""),
#                                full_text_length=char_count,
#                                word_count=word_count,
#                                language=language,
#                                tts_engine=tts_engine,
#                                voice_quality=voice_quality,
#                                success=True)
#
#     except Exception as e:
#         return render_template('index.html',
#                                error=f"An error occurred: {str(e)}"), 500
#
#
# @bp.route('/outputs/<filename>')
# def serve_audio(filename):
#     """Serve generated audio files (Module 5: Playback)"""
#     try:
#         return send_from_directory(current_app.config['OUTPUT_FOLDER'],
#                                    filename,
#                                    as_attachment=False)
#     except FileNotFoundError:
#         return "Audio file not found", 404
#
#
# @bp.route('/cleanup', methods=['POST'])
# def cleanup():
#     """Optional: Clean up old audio files"""
#     try:
#         output_folder = current_app.config['OUTPUT_FOLDER']
#         for filename in os.listdir(output_folder):
#             file_path = os.path.join(output_folder, filename)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#         return {"success": True, "message": "Cleanup completed"}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500


# .....................................................................................
#
# """
# Controller: Routes - WITH COQUI XTTS-v2 SUPPORT
# """
#
# from flask import Blueprint, render_template, request, current_app, send_from_directory, url_for
# from werkzeug.utils import secure_filename
# import os
# import uuid
# from services.extractor import extract_text_from_file, clean_text
# from services.language_detector import detect_language, preprocess_text, split_text_into_chunks
# from services.tts_service import TTSService
#
# bp = Blueprint('routes', __name__)
#
# ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.png', '.jpg', '.jpeg', '.txt', '.bmp', '.tiff'}
#
#
# def allowed_file(filename):
#     if '.' not in filename:
#         return False
#     ext = '.' + filename.rsplit('.', 1)[1].lower()
#     return ext in ALLOWED_EXTENSIONS
#
#
# @bp.route('/')
# def index():
#     return render_template('index.html')
#
#
# @bp.route('/process', methods=['POST'])
# def process():
#     try:
#         text_input = request.form.get('text_input', '').strip()
#         language = request.form.get('language', 'auto')
#         tts_engine = request.form.get('tts_engine', 'coqui')  # DEFAULT: Coqui (best free)
#         voice_quality = request.form.get('voice_quality', 'high')
#         uploaded_file = request.files.get('file')
#
#         extracted_text = ''
#
#         if uploaded_file and uploaded_file.filename:
#             filename = secure_filename(uploaded_file.filename)
#
#             if not allowed_file(filename):
#                 return render_template('index.html',
#                                        error="Invalid file type"), 400
#
#             temp_filename = f"{uuid.uuid4().hex}_{filename}"
#             temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
#             uploaded_file.save(temp_path)
#
#             try:
#                 extracted_text = extract_text_from_file(temp_path)
#                 print(f"✓ Extracted {len(extracted_text)} characters")
#             except Exception as e:
#                 return render_template('index.html',
#                                        error=f"Extraction failed: {str(e)}"), 500
#             finally:
#                 try:
#                     os.remove(temp_path)
#                 except:
#                     pass
#
#         if text_input:
#             final_text = text_input + ('\n\n' + extracted_text if extracted_text else '')
#         else:
#             final_text = extracted_text
#
#         if not final_text.strip():
#             return render_template('index.html',
#                                    error="No text provided"), 400
#
#         cleaned_text = clean_text(final_text)
#
#         if language == 'auto':
#             detected_lang = detect_language(cleaned_text)
#             language = detected_lang if detected_lang else 'en'
#
#         preprocessed_text = preprocess_text(cleaned_text, language)
#
#         print(f"✓ Processing {len(preprocessed_text)} characters")
#         print(f"✓ Using engine: {tts_engine}")
#
#         tts_service = TTSService(output_folder=current_app.config['OUTPUT_FOLDER'])
#
#         output_filename = f"{uuid.uuid4().hex}.mp3"
#         output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename)
#
#         try:
#             if tts_engine == 'coqui':
#                 # Coqui XTTS-v2 (BEST FREE - 90-95% HUMANOID)
#                 tts_service.save_with_coqui_xtts(preprocessed_text, output_path, lang=language, quality=voice_quality)
#             elif tts_engine == 'gtts':
#                 tts_service.save_with_gtts(preprocessed_text, output_path, lang=language)
#             elif tts_engine == 'elevenlabs':
#                 tts_service.save_with_elevenlabs(preprocessed_text, output_path, lang=language, quality=voice_quality)
#             else:  # pyttsx3
#                 tts_service.save_with_pyttsx3_unlimited(preprocessed_text, output_path, lang=language,
#                                                         quality=voice_quality)
#         except Exception as e:
#             return render_template('index.html',
#                                    error=f"TTS failed: {str(e)}"), 500
#
#         audio_url = url_for('routes.serve_audio', filename=output_filename)
#
#         word_count = len(preprocessed_text.split())
#         char_count = len(preprocessed_text)
#
#         return render_template('index.html',
#                                audio_url=audio_url,
#                                text=cleaned_text[:1000] + ("..." if len(cleaned_text) > 1000 else ""),
#                                full_text_length=char_count,
#                                word_count=word_count,
#                                language=language,
#                                tts_engine=tts_engine,
#                                voice_quality=voice_quality,
#                                success=True)
#
#     except Exception as e:
#         return render_template('index.html',
#                                error=f"Error: {str(e)}"), 500
#
#
# @bp.route('/outputs/<filename>')
# def serve_audio(filename):
#     try:
#         return send_from_directory(current_app.config['OUTPUT_FOLDER'],
#                                    filename, as_attachment=False)
#     except FileNotFoundError:
#         return "Audio not found", 404
#
#
# @bp.route('/cleanup', methods=['POST'])
# def cleanup():
#     try:
#         output_folder = current_app.config['OUTPUT_FOLDER']
#         for filename in os.listdir(output_folder):
#             file_path = os.path.join(output_folder, filename)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#         return {"success": True}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500


# ......................... Version 5 .......................


"""
Controller: Routes - WITH IMPROVED TTS SUPPORT
Uses working TTS models from your humanoid voice project
"""

from flask import Blueprint, render_template, request, current_app, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
import uuid
from services.extractor import extract_text_from_file, clean_text
from services.language_detector import detect_language, preprocess_text
from services.tts_service import TTSService

bp = Blueprint('routes', __name__)

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.png', '.jpg', '.jpeg', '.txt', '.bmp', '.tiff'}


def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = '.' + filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/process', methods=['POST'])
def process():
    try:
        text_input = request.form.get('text_input', '').strip()
        language = request.form.get('language', 'auto')
        tts_engine = request.form.get('tts_engine', 'gtts')  # Changed default to gtts (most reliable)
        voice_quality = request.form.get('voice_quality', 'high')
        uploaded_file = request.files.get('file')

        extracted_text = ''

        # Handle file upload
        if uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)

            if not allowed_file(filename):
                return render_template('index.html',
                                       error="Invalid file type. Supported: PDF, DOCX, TXT, PNG, JPG"), 400

            temp_filename = f"{uuid.uuid4().hex}_{filename}"
            temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
            uploaded_file.save(temp_path)

            try:
                extracted_text = extract_text_from_file(temp_path)
                print(f"✓ Extracted {len(extracted_text)} characters from {filename}")
            except Exception as e:
                return render_template('index.html',
                                       error=f"Failed to extract text: {str(e)}"), 500
            finally:
                try:
                    os.remove(temp_path)
                except:
                    pass

        # Combine text input and extracted text
        if text_input:
            final_text = text_input + ('\n\n' + extracted_text if extracted_text else '')
        else:
            final_text = extracted_text

        if not final_text.strip():
            return render_template('index.html',
                                   error="No text provided. Please enter text or upload a document."), 400

        # Clean and preprocess
        cleaned_text = clean_text(final_text)

        # Auto-detect language if needed
        if language == 'auto':
            detected_lang = detect_language(cleaned_text)
            language = detected_lang if detected_lang else 'en'
            print(f"✓ Auto-detected language: {language}")

        preprocessed_text = preprocess_text(cleaned_text, language)

        print(f"✓ Processing {len(preprocessed_text)} characters")
        print(f"✓ Using TTS engine: {tts_engine}")
        print(f"✓ Target language: {language}")

        # Initialize TTS service
        tts_service = TTSService(output_folder=current_app.config['OUTPUT_FOLDER'])

        output_filename = f"speech_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename)

        # Generate speech based on selected engine
        try:
            if tts_engine == 'coqui':
                # Coqui XTTS-v2 with speaker reference
                tts_service.save_with_coqui_xtts(preprocessed_text, output_path, lang=language, quality=voice_quality)
            elif tts_engine == 'gtts':
                # Google TTS (most reliable)
                tts_service.save_with_gtts(preprocessed_text, output_path, lang=language)
            elif tts_engine == 'elevenlabs':
                # ElevenLabs (premium)
                tts_service.save_with_elevenlabs(preprocessed_text, output_path, lang=language, quality=voice_quality)
            elif tts_engine == 'pyttsx3':
                # pyttsx3 (offline)
                tts_service.save_with_pyttsx3_unlimited(preprocessed_text, output_path, lang=language,
                                                        quality=voice_quality)
            else:
                # Fallback to gTTS
                tts_service.save_with_gtts(preprocessed_text, output_path, lang=language)

            print(f"✓ Audio generated successfully: {output_filename}")

        except Exception as e:
            error_msg = str(e)
            print(f"✗ TTS generation failed: {error_msg}")

            # Provide helpful error messages and fallback suggestions
            if tts_engine == 'coqui':
                return render_template('index.html',
                                       error=f"Coqui XTTS-v2 failed: {error_msg}. Try using gTTS or pyttsx3 instead."), 500
            elif tts_engine == 'elevenlabs':
                return render_template('index.html',
                                       error=f"ElevenLabs failed: {error_msg}. Check your API key or try another engine."), 500
            else:
                return render_template('index.html',
                                       error=f"TTS generation failed: {error_msg}"), 500

        # Generate URL for the audio file
        audio_url = url_for('routes.serve_audio', filename=output_filename)

        # Calculate statistics
        word_count = len(preprocessed_text.split())
        char_count = len(preprocessed_text)

        # Return success page with audio
        return render_template('index.html',
                               audio_url=audio_url,
                               text=cleaned_text[:1000] + ("..." if len(cleaned_text) > 1000 else ""),
                               full_text_length=char_count,
                               word_count=word_count,
                               language=language,
                               tts_engine=tts_engine,
                               voice_quality=voice_quality,
                               success=True)

    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('index.html',
                               error=f"Unexpected error: {str(e)}"), 500


@bp.route('/outputs/<filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        return send_from_directory(current_app.config['OUTPUT_FOLDER'],
                                   filename, as_attachment=False)
    except FileNotFoundError:
        return "Audio file not found", 404


@bp.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up old audio files"""
    try:
        output_folder = current_app.config['OUTPUT_FOLDER']
        deleted_count = 0

        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path) and filename != 'speaker_reference.wav':
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except:
                    pass

        return {"success": True, "deleted": deleted_count}, 200
    except Exception as e:
        return {"error": str(e)}, 500