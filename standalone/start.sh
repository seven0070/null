#!/bin/sh
# Null Universe — one command. No Minecraft, no installs, no accounts.
# Python 3 only (standard library). Then open http://localhost:8765
cd "$(dirname "$0")"
exec python3 server.py
