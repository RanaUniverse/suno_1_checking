"""
main.py

This will my running point of my app
"""

from flask_di import DIFlask


from app.shared.extensions import login_manager, csrf
from app.features.identity.presentation.routes import auth_bp
from app.features.general.routes import general_bp


def create_app() -> DIFlask:
    app = DIFlask(
        import_name=__name__,
    )

    login_manager.init_app(  # type: ignore
        app=app,
    )

    csrf.init_app(  # type: ignore
        app=app,
    )

    from app.config import settings

    app.secret_key = settings.app.secret_key.get_secret_value()
    app.register_blueprint(
        blueprint=auth_bp,
    )
    app.register_blueprint(
        blueprint=general_bp,
    )
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=9999,
        debug=True,
    )
