# """
# Text-to-Speech Voice Agent - Main Application
# Flask-based TTS system with offline/online support
# """
#
# from flask import Flask
# import os
#
#
# def create_app():
#     """Application factory pattern"""
#     app = Flask(__name__,
#                 static_folder='static',
#                 template_folder='templates')
#
#     # Configuration
#     app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
#     app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
#
#     # Setup folders
#     app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
#     app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'outputs')
#
#     # Create directories if they don't exist
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#     os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
#     os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)
#
#     # Register blueprints
#     from controllers.routes import bp as routes_bp
#     app.register_blueprint(routes_bp)
#
#     # Error handlers
#     @app.errorhandler(413)
#     def too_large(e):
#         return "File is too large (max 16MB)", 413
#
#     @app.errorhandler(500)
#     def internal_error(e):
#         return f"Internal server error: {str(e)}", 500
#
#     return app
#
#
# if __name__ == '__main__':
#     app = create_app()
#     print("=" * 50)
#     print("🎙️  TTS Voice Agent Starting...")
#     print("=" * 50)
#     print("📍 Access at: http://localhost:5000")
#     print("=" * 50)
#     app.run(debug=True, host='0.0.0.0', port=5000)


# ........................ Version 5 ......................

"""
AI Voice Agent with RAG - Main Application
Flask-based TTS system with working Coqui XTTS-v2 integration
"""

from flask import Flask
import os
import sys


def create_app():
    """Application factory pattern with enhanced configuration"""
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    # ===== CONFIGURATION =====
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-in-production-' + os.urandom(24).hex())
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

    # Folder setup
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'outputs')

    # Create all required directories
    for folder in [
        app.config['UPLOAD_FOLDER'],
        app.config['OUTPUT_FOLDER'],
        os.path.join(app.root_path, 'static'),
        os.path.join(app.root_path, 'templates')
    ]:
        os.makedirs(folder, exist_ok=True)

    # ===== REGISTER BLUEPRINTS =====
    from controllers.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # ===== ERROR HANDLERS =====
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {
            'success': False,
            'error': 'File is too large. Maximum size is 16MB.'
        }, 413

    @app.errorhandler(500)
    def internal_server_error(error):
        return {
            'success': False,
            'error': f'Internal server error: {str(error)}'
        }, 500

    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'error': 'Resource not found'
        }, 404

    # ===== STARTUP CHECKS (Run immediately) =====
    print("\n" + "=" * 60)
    print("🔍 Running system checks...")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 8):
        print("⚠ WARNING: Python 3.8+ recommended")
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check required libraries
    required_libs = {
        'flask': 'Flask',
        'torch': 'PyTorch',
        'TTS': 'Coqui TTS',
        'gtts': 'Google TTS',
        'pyttsx3': 'pyttsx3',
        'pdfplumber': 'pdfplumber',
        'pytesseract': 'pytesseract',
        'langdetect': 'langdetect'
    }

    for module, name in required_libs.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"⚠ {name} not installed")

    print("=" * 60)
    print("✓ System checks complete")
    print("=" * 60 + "\n")

    return app


def print_startup_banner():
    """Print application startup information"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║          🎙️  AI VOICE AGENT WITH RAG  🎙️            ║
    ║                                                       ║
    ║     Text-to-Speech System with Multiple Engines      ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)
    print("\n📋 SUPPORTED FEATURES:")
    print("   • Coqui XTTS-v2 (90-95% humanoid quality)")
    print("   • Google Text-to-Speech (fast & reliable)")
    print("   • pyttsx3 (offline support)")
    print("\n📄 SUPPORTED FILE TYPES:")
    print("   • PDF, DOCX, TXT")
    print("   • Images (PNG, JPG, JPEG, BMP, TIFF)")
    print("\n🌐 SUPPORTED LANGUAGES:")
    print("   • English, Urdu, Arabic, Spanish, French, Hindi")
    print("   • Auto-detection available")
    print("\n" + "=" * 60)
    print("🚀 SERVER STARTING...")
    print("=" * 60)
    print("📍 Local:    http://localhost:5000")
    print("📍 Network:  http://0.0.0.0:5000")
    print("=" * 60)
    print("\n💡 TIPS:")
    print("   • First request may take time (model loading)")
    print("   • Use Ctrl+C to stop the server")
    print("   • Check /health endpoint for status")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    # Print startup information
    print_startup_banner()

    # Create and run application
    app = create_app()

    # Development server settings
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True  # Enable threading for better performance
    )