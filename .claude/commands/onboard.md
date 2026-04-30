---
description: Onboard a new client by copying the example template and filling in style files
argument-hint: [client-slug]
---

Onboard a new client with slug **$1**.

Steps:

1. Validate the slug: lowercase, kebab-case, no spaces. If invalid, suggest a fix and stop.
2. Check that `clients/$1/` does not already exist. If it does, stop and tell the user.
3. Run: `cp -r clients/_example-client clients/$1`
4. Walk the user through filling in the four style files, one at a time, in this order:
   - `clients/$1/style/voice.md` — ask: tone, formality, banned words, sentence/paragraph rules, AI tells to avoid
   - `clients/$1/style/audience.md` — ask: who they read this for, expertise level, what they already know
   - `clients/$1/style/brand.md` — ask: positioning, products, things never to say, competitors not to cite
   - `clients/$1/style/cms.md` — ask: publishing target (WordPress/Ghost/Webflow/none), social channels, frontmatter requirements
   - `clients/$1/style/examples.md` — ask: 2-3 links or excerpts of past content that worked
5. Save each file as the user answers. Show them the saved version before moving on.
6. End with: "Client $1 onboarded. Run `/content $1 [topic]` to start."

Keep the conversation short. One question per file. If the user gives partial answers, save what they gave and note what's missing in a `TODO` block at the bottom of each file.
