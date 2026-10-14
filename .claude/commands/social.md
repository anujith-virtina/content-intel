---
description: Turn a blog post into a LinkedIn + Instagram post (poster or carousel) and publish it once the article is live
argument-hint: [client-slug] [wp-post-id]
---

Build and post the social pack for client **$1**, WordPress post **$2**. Rules: `clients/$1/style/social.md`.
Works for any client that has `clients/$1/social.json` (currently `virtina`, `chatsku`).

Standing instruction: published blogs are posted automatically. Do not ask the user to approve.
You (the orchestrator) run every command yourself. Sub-agents have no Bash.

1. `python social/social_pipeline.py --client $1 fetch $2` and note the slug, status and URL it prints.
2. Delegate the copy to `creator`. Pass: the client, the source file
   `clients/$1/output/social/_source/$2.json`, the rules file `clients/$1/style/social.md`, and the output
   path `clients/$1/output/social/{slug}-{YYYY-MM-DD}.json` (today's date; append `-v2` if it exists).
   Tell it this is a social pack, not a blog draft, and to write only that one file. Say whether you want
   a single poster or a carousel.
3. `python social/social_pipeline.py render <pack>` then `python social/social_pipeline.py qa <pack>`.
   - "text does not fit": send the named text back to `creator` to shorten. Never shrink the font.
   - A QA failure is a copy failure: send the listed lines back to `creator`. A Python traceback is a
     tool bug: fix the script, do not rewrite the copy.
4. Open every rendered slide image and look at it. Check for clipped or crowded text.
5. `python social/social_pipeline.py publish <pack> --dry-run`.
   - "article is still draft": stop here. The pack is held; tell the user it will post when the article
     goes live. This is the normal end state for a fresh draft.
   - Only "missing ... in .env" blockers: post through the browser (step 6).
   - Clean: run `publish <pack>` and report both post URLs.
6. Browser route (no API tokens). Use Claude in Chrome on the profile named "Personal Chrome"
   (`switch_browser` if another profile is selected). Check the right account is active before posting:
   the client's LinkedIn company page admin view, and the client's Instagram handle (switch accounts on
   Instagram if another is active). If the account is not signed in, stop and ask the user to sign in.
   - Suppress the native file picker before clicking any upload button: patch
     `HTMLInputElement.prototype.click` to capture file inputs, then use `file_upload` on that input.
   - LinkedIn: type the caption first, remove the auto link-preview card, then add the image(s).
   - Instagram: upload all slides in order, keep the 1:1 crop, type the caption, Share.
   - Use the text of `linkedin_text` / `instagram_text` exactly (the `.md` preview next to the pack).
7. After a browser post, write `state.linkedin.url` and `state.instagram.url` into the pack so `sweep`
   never posts it again. Tell the user where each post went.

`python social/social_pipeline.py --client $1 sweep --dry-run` lists every pack that is ready or held.
