Set-Location "C:\content-intel"
python "C:\content-intel\clients\chatsku\output\research\run_publish.py" 2>&1 | Tee-Object -FilePath "C:\content-intel\clients\chatsku\output\research\run_publish_log.txt"
