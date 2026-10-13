---
description: Turn a Virtina blog post into a LinkedIn + Instagram pack (copy + carousel), then post it once the article is live
argument-hint: [wp-post-id]
---

Build the social pack for Virtina WordPress post **$1**. Rules: `clients/virtina/style/social.md`.

You (the orchestrator) run every command yourself. Sub-agents have no Bash.

1. `python social/social_pipeline.py fetch $1` and note the slug, status and URL it prints.
2. Delegate the copy to `creator`. Pass: client `virtina`, the source file
   `clients/virtina/output/social/_source/$1.json`, the rules file `clients/virtina/style/social.md`, and
   the output path `clients/virtina/output/social/{slug}-{YYYY-MM-DD}.json` (today's date; append `-v2`
   if it exists). Tell it this is a social pack, not a blog draft, and to write only that one file.
3. `python social/social_pipeline.py render <pack>` then `python social/social_pipeline.py qa <pack>`.
   - "text does not fit": send the named text back to `creator` to shorten. Never shrink the font.
   - A QA failure is a copy failure: send the listed lines back to `creator`. A Python traceback is a
     tool bug: fix the script, do not rewrite the copy.
4. Open `slides/<pack name>/contact-sheet.png` and look at it. Check for clipped or crowded text.
5. Show the user the LinkedIn post, the Instagram caption and the contact sheet path inline.
6. `python social/social_pipeline.py publish <pack> --dry-run` and report what it says.
   - "article is still draft": expected for a fresh post. The pack waits. `sweep` posts it later.
   - "not approved": run `approve <pack>` only after the user has okayed the copy in this session.
7. Only when the dry run is clean and the user has approved: `publish <pack>`. Report both post URLs.

`python social/social_pipeline.py sweep` posts every approved pack whose article has gone live.
