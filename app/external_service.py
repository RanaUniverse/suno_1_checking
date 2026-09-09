"""
src/suno_1_checking/app/__init__.py

Here i will try to call the external service from my server
"""

import requests


from app.config import RIGHTS_URL, BASE_URL


def call_external_post_api_call(
    content_id: str,
    content_type: str = "clip",
    url: str = RIGHTS_URL,
) -> str:

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": BASE_URL,
        "Referer": BASE_URL,
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
    }

    data = {
        "content_params": {
            "content_id": content_id,
            "content_type": content_type,
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        raise


if __name__ == "__main__":

    # This below is a song of external songs of suno
    id_ = "b8d72ee1-0afa-4504-aa46-ec07a3bb61b0"
    call_external_post_api_call(
        content_id=id_,
    )
