"""
Runner: loads .env then imports and runs build_pdf_catalog_post.main()
"""
import os, subprocess, sys

# Load .env
env_path = r"C:\content-intel\.env"
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

# Verify creds loaded
assert os.environ.get("CHATSKU_WP_USERNAME"), "CHATSKU_WP_USERNAME missing"
assert os.environ.get("CHATSKU_WP_APP_PASSWORD"), "CHATSKU_WP_APP_PASSWORD missing"
print(f"Credentials loaded: CHATSKU_WP_USERNAME={os.environ['CHATSKU_WP_USERNAME']}")
print(f"PEXELS_API_KEY present: {'YES' if os.environ.get('PEXELS_API_KEY') else 'NO -- will use Openverse'}")

# Run the build script in the same process (env vars already set)
sys.path.insert(0, r"C:\content-intel\clients\chatsku\output\research")

# Execute via runpy to avoid module name clash
import runpy
runpy.run_path(
    r"C:\content-intel\clients\chatsku\output\research\build_pdf_catalog_post.py",
    run_name="__main__"
)
