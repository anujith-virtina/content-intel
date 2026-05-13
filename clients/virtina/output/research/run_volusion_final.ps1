# ============================================================
# Publish Volusion to WooCommerce migration post
# Run this from PowerShell (admin not required):
#   cd C:\content-intel
#   python clients\virtina\output\research\publish_volusion_final.py 2>&1 | Tee-Object -FilePath clients\virtina\output\research\volusion_final_log.txt
# Or just:
#   .\clients\virtina\output\research\run_volusion_final.ps1
# ============================================================

Set-Location C:\content-intel
python clients\virtina\output\research\publish_volusion_final.py 2>&1 | Tee-Object -FilePath clients\virtina\output\research\volusion_final_log.txt
Write-Host "`nLog saved to: C:\content-intel\clients\virtina\output\research\volusion_final_log.txt"
