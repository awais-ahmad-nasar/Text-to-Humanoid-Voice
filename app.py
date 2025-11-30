"""
Text-to-Speech Voice Agent - Main Application
Flask-based TTS system with offline/online support
"""

from flask import Flask
import os


def create_app():
    """Application factory pattern"""
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

    # Setup folders
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'outputs')

    # Create directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)

    # Register blueprints
    from controllers.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Error handlers
    @app.errorhandler(413)
    def too_large(e):
        return "File is too large (max 16MB)", 413

    @app.errorhandler(500)
    def internal_error(e):
        return f"Internal server error: {str(e)}", 500

    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("🎙️  TTS Voice Agent Starting...")
    print("=" * 50)
    print("📍 Access at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)