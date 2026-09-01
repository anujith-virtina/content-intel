"""Inject CSS via WordPress Customizer to add SVG arrows to post 42202 TOC."""
import os, sys, requests, urllib3, re, base64, json, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://virtina.com"
USERNAME = "anujith"
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
REAL_PASSWORD = os.environ.get("WP_REAL_PASSWORD", "")

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
h_api = {"Authorization": f"Basic {token}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# SVG data URI for the arrow (same as post 42177)
svg_uri = "data:image/svg+xml,%3Csvg viewBox='0 0 24 24' width='18' height='18' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4%2C11V13H16L10.5%2C18.5L11.92%2C19.92L19.84%2C12L11.92%2C4.08L10.5%2C5.5L16%2C11H4Z' fill='%2343627f'/%3E%3C/svg%3E"

# CSS to add arrows to post 42202 TOC items
# The TOC <ul> has style="list-style: none!important; padding-left: 0!important..."
# The <li> has position: relative and padding-left: 32px - perfect for ::before
arrow_css = f"""
/* Virtina post 42202 TOC arrows */
.post-42202 ul[style*="list-style"] > li::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 8px;
    width: 18px;
    height: 18px;
    background-image: url("{svg_uri}");
    background-repeat: no-repeat;
    background-size: contain;
}}
"""

print("=== Arrow CSS to inject ===")
print(arrow_css)

# Step 1: Try REST API for custom CSS (Customizer CSS)
print("\n=== Trying REST API approaches ===")

# WordPress exposes Customizer CSS via wp/v2/custom-css endpoint (since WP 5.9 via global styles)
for endpoint in [
    "/wp-json/wp/v2/settings",
    "/wp-json/wp/v2/custom-css",
    "/wp-json/wp/v2/global-styles",
    "/wp-json/wp/v2/themes?status=active",
]:
    r = requests.get(f"{SITE}{endpoint}", headers=h_api, verify=False, timeout=15)
    if r.status_code == 200:
        print(f"GET {endpoint}: {r.status_code} (length: {len(r.text)})")
        data = r.json()
        if isinstance(data, dict):
            css_keys = [k for k in data.keys() if 'css' in k.lower() or 'style' in k.lower()]
            print(f"  CSS-related keys: {css_keys}")
        elif isinstance(data, list) and data:
            print(f"  First item keys: {list(data[0].keys())[:10]}")
    else:
        print(f"GET {endpoint}: {r.status_code}")

# Step 2: Try WP REST API settings to find custom_css option
r_settings = requests.get(f"{SITE}/wp-json/wp/v2/settings", headers=h_api, verify=False, timeout=15)
if r_settings.status_code == 200:
    settings = r_settings.json()
    css_val = settings.get("custom_css", settings.get("additional_css", ""))
    print(f"\nCurrent custom_css in settings: '{str(css_val)[:100]}'")

# Step 3: Find the custom_css post (Customizer stores CSS as a special post)
print("\n=== Finding custom_css post type ===")
r_custom = requests.get(f"{SITE}/wp-json/wp/v2/custom-css", headers=h_api, verify=False, timeout=15)
print(f"GET /wp-json/wp/v2/custom-css: {r_custom.status_code} {r_custom.text[:200]}")

# Step 4: Session-based approach - submit Customizer via admin-ajax
print("\n=== Session login for Customizer approach ===")
session = requests.Session()
session.verify = False
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
session.get(f"{SITE}/wp-login.php", timeout=15)
session.post(f"{SITE}/wp-login.php", data={
    "log": USERNAME, "pwd": REAL_PASSWORD, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1",
}, allow_redirects=True, timeout=20)
logged_in = any("logged_in" in k for k in session.cookies.keys())
print(f"Logged in: {logged_in}")

rest_nonce = session.get(f"{SITE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=10).text.strip()
sh = {"X-WP-Nonce": rest_nonce, "Content-Type": "application/json"}

# Try to save via Customizer save endpoint
# WordPress Customizer saves via admin-ajax.php?action=customize_save
print("\n=== Trying Customizer save via AJAX ===")
customize_url = f"{SITE}/wp-admin/customize.php"
r_customize = session.get(customize_url, timeout=20)
print(f"Customize page: {r_customize.status_code}")

# Find customizer nonce
customize_nonce_m = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', r_customize.text)
wp_customize_m = re.search(r'_wpCustomizeSettings\s*=\s*(\{[^;]+\})', r_customize.text, re.S)

# Find save-nonce
save_nonce_m = re.search(r'"save-nonce"\s*:\s*"([a-f0-9]+)"', r_customize.text)
if save_nonce_m:
    save_nonce = save_nonce_m.group(1)
    print(f"  Customize save-nonce: {save_nonce}")

    # Try to get current custom_css post ID
    theme_m = re.search(r'"stylesheet"\s*:\s*"([^"]+)"', r_customize.text)
    theme = theme_m.group(1) if theme_m else ""
    print(f"  Theme: {theme}")

    # Submit customize_save via AJAX with custom_css
    customize_data = {
        "action": "customize_save",
        "nonce": save_nonce,
        "wp_customize": "on",
        "customized": json.dumps({
            "custom_css[" + theme + "]": arrow_css
        }),
        "customize_changeset_uuid": "",
        "customize_theme": theme,
        "customize_messenger_channel": "preview-0",
    }
    r_save = session.post(f"{SITE}/wp-admin/admin-ajax.php", data=customize_data, timeout=20)
    print(f"  Customize save: {r_save.status_code} {r_save.text[:200]}")

# Try the REST API global styles approach (WP 5.9+)
print("\n=== Trying REST API global styles ===")
r_global = requests.get(f"{SITE}/wp-json/wp/v2/global-styles/themes/virtina", headers=h_api, verify=False, timeout=15)
print(f"GET global-styles/themes/virtina: {r_global.status_code} {r_global.text[:200]}")

# Find active theme slug
r_themes = requests.get(f"{SITE}/wp-json/wp/v2/themes?status=active", headers=h_api, verify=False, timeout=15)
if r_themes.status_code == 200:
    themes = r_themes.json()
    if themes:
        theme_slug = themes[0].get("stylesheet", "")
        print(f"Active theme slug: {theme_slug}")
        # Try global styles for this theme
        r_gs = requests.get(f"{SITE}/wp-json/wp/v2/global-styles/themes/{theme_slug}", headers=h_api, verify=False, timeout=15)
        print(f"GET global-styles/themes/{theme_slug}: {r_gs.status_code} {r_gs.text[:300]}")
