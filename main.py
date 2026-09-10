from flask import Flask, render_template

from flask import request, jsonify

import requests

from app.external_service import call_external_post_api_call, get_suno_proxy

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        template_name_or_list="index.html",
    )


@app.get("/api/suno/proxy")
def get_proxy():

    target_url = request.args.get("url")

    if not target_url:
        return {"error": "Missing url"}, 400

    result = get_suno_proxy(
        song_url=target_url,
    )
    return result


@app.post("/api/RanaUniverse/rights")
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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9999,
        debug=True,
    )
