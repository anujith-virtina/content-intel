---
description: Run the full content pipeline (research → analyze → create → publish) for a topic
argument-hint: [client-slug] [topic or URL]
---

Run the full content intelligence pipeline for client **$1** on topic: **$2**

Steps:

1. Verify the client folder exists at `clients/$1/`. If not, list available clients and stop.
2. Confirm the topic with one short sentence. Ask the user only what you can't infer from the client's style files (usually format and target length). Max 2 questions.
3. Delegate to `researcher` with client=$1 and topic=$2.
4. Show the user the research summary inline. Wait for "go" or edits.
5. Delegate to `analyzer` with the research file.
6. Show the user the brief inline. Wait for "go" or edits.
7. Delegate to `creator` with the approved brief.
8. Show the draft (or its path) and the headline options. Wait for "go" or edits.
9. Ask which channels to publish to: file only, file + CMS, file + social, or all.
10. Delegate to `publisher` with the chosen channels.
11. Confirm what shipped and where.

Pause between every stage. Do not skip checkpoints.
