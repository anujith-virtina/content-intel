#!/usr/bin/env python3
"""
Inline runner: loads .env, then runs the publish pipeline.
"""
import os
import sys
import subprocess

# Load .env
env_path = r"C:\content-intel\.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()
    print("Loaded .env")
else:
    print(f"ERROR: .env not found at {env_path}")
    sys.exit(1)

# Now import and run the pipeline
sys.path.insert(0, r"C:\content-intel\clients\virtina\output\research")
import publish_b2b_portal
publish_b2b_portal.main()
