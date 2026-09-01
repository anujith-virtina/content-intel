"""Direct runner that loads .env and executes the build script."""
import os, sys

# Load .env
env_path = r"C:\content-intel\.env"
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

print(f"CHATSKU_WP_USERNAME = {os.environ.get('CHATSKU_WP_USERNAME', 'NOT SET')}")
print(f"CHATSKU_WP_APP_PASSWORD = {'SET' if os.environ.get('CHATSKU_WP_APP_PASSWORD') else 'NOT SET'}")

# Execute main script
exec(open(r"C:\content-intel\clients\chatsku\output\research\build_rfq_form_post.py").read())
