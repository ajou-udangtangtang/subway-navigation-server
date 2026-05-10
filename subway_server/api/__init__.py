from flask import Blueprint, Flask, jsonify

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def health():
    """Health check
    ---
    tags:
      - meta
    responses:
      200:
        description: Server is up
        content:
          application/json:
            schema:
              type: object
              properties:
                status: { type: string, example: "ok" }
    """
    return jsonify(status="ok")


def register_blueprints(app: Flask) -> None:
    # Import endpoint modules so their @bp.route decorators run.
    from . import direction, locate, route  # noqa: F401

    app.register_blueprint(bp)
