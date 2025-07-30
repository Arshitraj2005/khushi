#!/bin/bash

# Start Flask app for UptimeRobot ping support
python3 main.py &

# Then start the stream script in parallel
python3 stream.py
