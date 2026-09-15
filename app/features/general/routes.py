"""
app/features/general/routes.py

Normal related main parts of my logics will be here
"""

from flask import Blueprint, render_template, request, jsonify


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
