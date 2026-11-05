# Evening social media run for ChatSKU and Virtina. Started daily at 6:30 PM by Windows Task Scheduler
# (task name: ContentIntelSocialEvening). Needs: computer on and signed in, Chrome open and signed in to
# LinkedIn and Instagram with the Claude in Chrome extension. Logs go to logs\evening-social-YYYY-MM-DD.log.
# Use -Test to check Chrome access only (posts nothing).
param([switch]$Test)

$root = 'C:\content-intel'
Set-Location $root
New-Item -ItemType Directory -Force -Path "$root\logs" | Out-Null
$log = "$root\logs\evening-social-$(Get-Date -Format 'yyyy-MM-dd')$(if ($Test) {'-test'}).log"

if ($Test) {
  $prompt = 'TEST ONLY. Do not post anything. Call tabs_context_mcp with createIfEmpty true, report whether the Chrome tools work, close any tab you created, and stop.'
} else {
  $prompt = @'
Evening social media run (scheduled by the user: "schedule social media every evening at 6.30 pm so I dont have to tell you"). The user has authorized this run to post to LinkedIn and Instagram without asking. Follow CLAUDE.md, .claude/commands/social.md, clients/{client}/style/social.md and the memory notes (feedback_post_only_the_channel_asked, feedback_social_caption_must_add_new_value, feedback_images_show_the_pain_split_panel, feedback_social_creative_variety, feedback_linkedin_composer_accident_and_clear_copy). Do this in order and stop at the first step that yields a post for each brand: (1) For virtina and chatsku run python social/social_pipeline.py --client <c> sweep --dry-run; post any pack whose blog is live and not yet posted (LinkedIn page and Instagram of the right brand; ChatSKU Instagram may not be signed in, then skip it and say so; never type passwords). (2) If nothing is waiting for a brand, look at today's date in the content map Google Doc (https://docs.google.com/document/d/1Uf1A4CDMU2xC_WLjJ3gqGYHX4RvroTqU5Dmd5ysom8c/mobilebasic, Part 4 social posts day by day) and post today's item for that brand if one exists. (3) If still nothing, make ONE trend-based post for the brand that posted least recently: check Google Trends for the brand's themes, write the brand's own post from facts on its own site or briefing (never invent numbers, never name competitors in captions, never copy competitor content), make the images per the memory notes, and post it. Always: open a NEW Chrome tab for each job and close it afterwards, never touch the user's other tabs, never complete CAPTCHAs, record the post URLs in the pack state so nothing posts twice, post at most one post per brand per run, and finish with a short report of what was posted and where, or why nothing was posted.
'@
}

"=== $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') start (Test=$Test) ===" | Out-File -FilePath $log -Append -Encoding utf8
& 'C:\Users\ASUS\.local\bin\claude.exe' -p $prompt --allowedTools 'Bash,Read,Write,Edit,Glob,Grep,Agent,Skill,WebFetch,WebSearch,mcp__claude-in-chrome' --max-turns 200 2>&1 | Out-File -FilePath $log -Append -Encoding utf8
"=== $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') end ===" | Out-File -FilePath $log -Append -Encoding utf8
