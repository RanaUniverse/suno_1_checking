"""
app/features/general/routes.py

Normal related main parts of my logics will be here
"""

from flask import Blueprint, render_template, request, jsonify

from flask_login import (  # type: ignore
    login_required,  # type: ignore
    current_user,
)

import requests


from app.external_service import call_external_post_api_call, get_suno_proxy

general_bp = Blueprint(
    name="general_bp",
    import_name=__name__,
    # template_folder="templates",
)


@general_bp.route("/")
def home():
    return render_template(
        template_name_or_list="index.html",
    )


@general_bp.get("/api/suno/proxy")
def get_proxy():

    target_url = request.args.get("url")

    if not target_url:
        return {"error": "Missing url"}, 400

    result = get_suno_proxy(
        song_url=target_url,
    )
    return result


@general_bp.post("/api/RanaUniverse/rights")
def get_rights():
    try:
        data = request.get_json()

        content_id = data["content_params"]["content_id"]
        content_type = data["content_params"]["content_type"]

    except (TypeError, KeyError):
        return jsonify({"error": "Invalid request body"}), 400

    try:
        result = call_external_post_api_call(
            content_id=content_id,
            content_type=content_type,
        )
        return jsonify(result), 200

    except requests.RequestException as e:
        print(f"External API error: {e}")

        return jsonify({"error": "External service unavailable"}), 502


@general_bp.get("/playlist/")
def playlist():
    return render_template("rana_playlist.html")


@general_bp.route("/dashboard")
@login_required
def dashboard():
    # Mapping real data from your usermodel columns + demo stats for stars/songs
    user_data = {
        "first_name": getattr(current_user, "first_name", "Rana"),
        "last_name": getattr(current_user, "last_name", "Universe"),
        "email": getattr(current_user, "email", "rana@example.com"),
        "last_login_time": getattr(current_user, "last_login_time", "Today, 4:15 PM"),
        "is_verified": getattr(current_user, "is_verified", True),
        "profile_pic": "https://avatars.githubusercontent.com/u/142967497?v=4",
        "total_stars": 150,
        "songs_downloaded": [
            {
                "title": "Cyberpunk Sunset vibe",
                "url": "https://suno.com/s/sample-track-1",
                "date": "2026-06-12",
            },
            {
                "title": "Lo-Fi Linux Coding",
                "url": "https://suno.com/s/sample-track-2",
                "date": "2026-06-10",
            },
            {
                "title": "Python Developer Anthem",
                "url": "https://suno.com/s/sample-track-3",
                "date": "2026-06-08",
            },
            {
                "title": "Bootstrap 5 Fast Beats",
                "url": "https://suno.com/s/sample-track-4",
                "date": "2026-06-05",
            },
            {
                "title": "Midnight Debugging",
                "url": "https://suno.com/s/sample-track-5",
                "date": "2026-06-01",
            },
        ],
    }
    return render_template("dashboard.html", user=user_data)
