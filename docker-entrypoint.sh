#!/bin/bash

function run_gunicorn {
    echo "[*] Starting server"
    gunicorn \
        --log-level error \
        -w 1 \
        -b "${TT_API_LISTEN_ADDR}:${TT_API_LISTEN_PORT}" \
        -t 300 \
        wsgi:application
}

function migrate {
    echo "[*] Running migrations..."
    python manage.py migrate --noinput
    return $?
    echo "[*] Done."
}

echo "[*] Executing $1"

case "$1" in
    server)
        migrate && \
        run_gunicorn
        ;;
    *)
        exec "$@"
        ;;
esac
