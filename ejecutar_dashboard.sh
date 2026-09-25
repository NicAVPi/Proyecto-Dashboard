#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python validar_datos.py
python app.py
