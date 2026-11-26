"""Flask Application Factory with REST API Blueprints and Static/Page Hosting."""
import os
from flask import Flask, jsonify, render_template, send_from_directory, session
from backend.app.config import Config
from backend.app.database.db import DatabaseConnectionError, check_db_health


def create_app(config_class=Config):
    # Determine frontend directory paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    frontend_dir = os.path.join(base_dir, "frontend")
    pages_dir = os.path.join(frontend_dir, "pages")

    app = Flask(
        __name__,
        static_folder=frontend_dir,
        static_url_path="",
        template_folder=pages_dir
    )
    app.config.from_object(config_class)

    # Register API Blueprints
    from backend.app.routes.auth_routes import auth_bp
    from backend.app.routes.profile_routes import profile_bp
    from backend.app.routes.nlp_routes import nlp_bp
    from backend.app.routes.chat_routes import chat_bp
    from backend.app.routes.matching_routes import matching_bp
    from backend.app.routes.scheme_routes import scheme_bp
    from backend.app.routes.checklist_routes import checklist_bp
    from backend.app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(nlp_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(scheme_bp)
    app.register_blueprint(checklist_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(DatabaseConnectionError)
    def handle_db_error(e):
        return jsonify({"success": False, "error": str(e), "db_status": "disconnected"}), 503

    @app.route("/api/health", methods=["GET"])
    def api_health():
        connected, msg, count = check_db_health()
        return jsonify({
            "status": "healthy" if connected else "degraded",
            "app_name": "AI Scheme Sahayak",
            "database": "MySQL 8.0",
            "mysql_connected": connected,
            "active_schemes_in_db": count,
            "message": msg
        }), (200 if connected else 503)

    # Root route serves index.html from frontend
    @app.route("/", methods=["GET"])
    def index():
        return send_from_directory(frontend_dir, "index.html")

    # Static asset alias so /static/css/... and /static/js/... map directly to frontend/
    @app.route("/static/<path:filename>")
    def custom_static(filename):
        return send_from_directory(frontend_dir, filename)

    # Service worker & manifest direct routes for PWA
    @app.route("/service-worker.js")
    def sw():
        resp = send_from_directory(frontend_dir, "service-worker.js", mimetype="application/javascript")
        resp.headers["Service-Worker-Allowed"] = "/"
        resp.headers["Cache-Control"] = "no-cache"
        return resp

    @app.route("/manifest.json")
    def manifest():
        return send_from_directory(frontend_dir, "manifest.json", mimetype="application/manifest+json")

    return app
