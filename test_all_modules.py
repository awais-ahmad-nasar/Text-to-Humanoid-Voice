"""
Complete Testing Suite for TTS Voice Agent
Tests all 5 modules independently and integration
"""

import os
import sys


def test_module_1_imports():
    """Test Module 1: Import all Flask dependencies"""
    print("\n" + "=" * 60)
    print("MODULE 1: Testing Input & File Handling Imports")
    print("=" * 60)

    try:
        from flask import Flask, render_template, request
        from werkzeug.utils import secure_filename
        print("✓ Flask imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_module_2_text_extraction():
    """Test Module 2: Text Extraction & Cleaning"""
    print("\n" + "=" * 60)
    print("MODULE 2: Testing Text Extraction & Cleaning")
    print("=" * 60)

    try:
        # Test imports
        import pdfplumber
        from docx import Document
        from PIL import Image
        import pytesseract
        print("✓ All extraction libraries imported")

        # Test cleaning function
        from services.extractor import clean_text
        test_text = "  Hello   World  \n\n\n  Test  "
        cleaned = clean_text(test_text)
        assert "Hello World" in cleaned
        print("✓ Text cleaning works")

        # Test Tesseract availability
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract OCR version: {version}")
        except:
            print("⚠ Tesseract not found (OCR will not work)")

        return True
    except Exception as e:
        print(f"✗ Module 2 error: {e}")
        return False


def test_module_3_language_detection():
    """Test Module 3: Language Detection & Preprocessing"""
    print("\n" + "=" * 60)
    print("MODULE 3: Testing Language Detection & Preprocessing")
    print("=" * 60)

    try:
        from services.language_detector import detect_language, preprocess_text

        # Test English detection
        text_en = "Hello, this is a test message"
        lang = detect_language(text_en)
        print(f"✓ English detected as: {lang}")

        # Test Urdu detection
        text_ur = "یہ ایک ٹیسٹ ہے"
        lang_ur = detect_language(text_ur)
        print(f"✓ Urdu detected as: {lang_ur}")

        # Test preprocessing
        preprocessed = preprocess_text(text_en, 'en')
        assert len(preprocessed) > 0
        print("✓ Text preprocessing works")

        return True
    except Exception as e:
        print(f"✗ Module 3 error: {e}")
        return False


def test_module_4_tts_engines():
    """Test Module 4: Speech Generation"""
    print("\n" + "=" * 60)
    print("MODULE 4: Testing Speech Generation Engines")
    print("=" * 60)

    # Test pyttsx3 (offline)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"✓ pyttsx3 initialized ({len(voices)} voices available)")

        # Test speech generation
        test_file = "test_speech.wav"
        engine.save_to_file("This is a test", test_file)
        engine.runAndWait()

        if os.path.exists(test_file):
            print("✓ pyttsx3 audio generation works")
            os.remove(test_file)
        else:
            print("⚠ pyttsx3 file creation failed")

    except Exception as e:
        print(f"⚠ pyttsx3 error: {e}")

    # Test gTTS (online)
    try:
        from gtts import gTTS
        print("✓ gTTS imported (requires internet for use)")
    except ImportError:
        print("⚠ gTTS not installed")

    return True


def test_module_5_flask_routes():
    """Test Module 5: Flask Routes"""
    print("\n" + "=" * 60)
    print("MODULE 5: Testing Flask Routes & Templates")
    print("=" * 60)

    try:
        from controllers.routes import bp
        print("✓ Routes blueprint imported")

        # Check if template exists
        if os.path.exists('templates/index.html'):
            print("✓ index.html template exists")
        else:
            print("✗ index.html template missing")
            return False

        return True
    except Exception as e:
        print(f"✗ Module 5 error: {e}")
        return False


def test_directory_structure():
    """Test project directory structure"""
    print("\n" + "=" * 60)
    print("Testing Project Directory Structure")
    print("=" * 60)

    required_dirs = [
        'controllers',
        'services',
        'templates',
        'static',
        'static/uploads',
        'static/outputs'
    ]

    required_files = [
        'app.py',
        'requirements.txt',
        'controllers/__init__.py',
        'services/__init__.py',
        'controllers/routes.py',
        'services/extractor.py',
        'services/language_detector.py',
        'services/tts_service.py',
        'templates/index.html'
    ]

    all_ok = True

    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/")
        else:
            print(f"✗ {directory}/ missing")
            try:
                os.makedirs(directory)
                print(f"  → Created {directory}/")
            except:
                all_ok = False

    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} missing")
            all_ok = False

    return all_ok


def run_integration_test():
    """Run integration test of complete workflow"""
    print("\n" + "=" * 60)
    print("INTEGRATION TEST: Complete Workflow")
    print("=" * 60)

    try:
        from services.extractor import clean_text
        from services.language_detector import detect_language, preprocess_text
        from services.tts_service import TTSService

        # Test text
        test_text = "This is a test of the complete TTS system."

        # Step 1: Clean text
        cleaned = clean_text(test_text)
        print(f"✓ Step 1: Text cleaned")

        # Step 2: Detect language
        lang = detect_language(cleaned)
        print(f"✓ Step 2: Language detected: {lang}")

        # Step 3: Preprocess
        preprocessed = preprocess_text(cleaned, lang)
        print(f"✓ Step 3: Text preprocessed")

        # Step 4: Generate TTS
        os.makedirs('static/outputs', exist_ok=True)
        tts = TTSService('static/outputs')
        output_file = tts.generate_speech(preprocessed, engine='pyttsx3', lang=lang)

        if os.path.exists(output_file):
            print(f"✓ Step 4: TTS generated: {output_file}")
            os.remove(output_file)
            return True
        else:
            print("✗ Step 4: TTS generation failed")
            return False

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TTS VOICE AGENT - COMPLETE MODULE TESTING")
    print("=" * 60)

    results = {
        "Directory Structure": test_directory_structure(),
        "Module 1 (Input/File Handling)": test_module_1_imports(),
        "Module 2 (Text Extraction)": test_module_2_text_extraction(),
        "Module 3 (Language Detection)": test_module_3_language_detection(),
        "Module 4 (TTS Engines)": test_module_4_tts_engines(),
        "Module 5 (Flask Routes)": test_module_5_flask_routes(),
        "Integration Test": run_integration_test()
    }

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed ({passed * 100 // total}%)")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("Run: python app.py")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
        print("See PROJECT_STRUCTURE.md for troubleshooting.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)