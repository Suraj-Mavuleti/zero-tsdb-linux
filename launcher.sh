#!/bin/bash
# AUTO-UPDATER
cd /home/suraj/.gemini/antigravity/scratch/heavy_suite/zero-tsdb-linux
git pull origin main --quiet
python3 zero_tsdb_gui.py
