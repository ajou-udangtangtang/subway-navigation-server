"""API 호출 로깅 — 정확도 분석/디버깅용.

`logs/api.jsonl` 에 한 줄 한 호출씩 JSONL 로 기록. /apidocs 등은 제외.
파일은 10MB × 5개 rotation.
"""
import json
import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, g, request

_SKIP_PREFIXES = ("/apidocs", "/flasgger", "/apispec", "/static")


def init_access_log(app: Flask) -> None:
    logs_dir = Path(app.config.get("DATA_DIR", ".")).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    logfile = logs_dir / "api.jsonl"

    logger = logging.getLogger("subway.access")
    if not logger.handlers:
        handler = RotatingFileHandler(
            logfile, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    @app.before_request
    def _start_timer():
        g._t0 = time.perf_counter()

    @app.after_request
    def _record(response):
        path = request.path
        if any(path.startswith(p) for p in _SKIP_PREFIXES):
            return response

        elapsed_ms = round((time.perf_counter() - getattr(g, "_t0", time.perf_counter())) * 1000, 1)

        try:
            req_body = json.loads(request.get_data(as_text=True)) if request.data else None
        except Exception:
            req_body = "<not-json>"

        try:
            res_body = response.get_json(silent=True)
        except Exception:
            res_body = None

        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "method": request.method,
            "path": path,
            "status": response.status_code,
            "elapsed_ms": elapsed_ms,
            "req": req_body,
            "res": res_body,
            "remote": request.headers.get("X-Forwarded-For", request.remote_addr),
            "ua": request.headers.get("User-Agent", "")[:80],
        }
        logger.info(json.dumps(record, ensure_ascii=False))
        return response

