# Publishing — _example-client

This file tells the publisher agent where and how to ship content. Fill in only the channels this client uses. Delete or comment out the rest.

## Channels enabled

- [ ] file (always on)
- [ ] cms
- [ ] linkedin
- [ ] x
- [ ] threads
- [ ] bluesky

## Confirmation policy

```yaml
require_confirmation: true   # publisher must show payload and wait for "ship it" before pushing live
```

Set to `false` only for low-stakes channels where mistakes are cheap to fix.

---

## Frontmatter schema for published files

The publisher writes this at the top of every file in `output/published/`:

```yaml
---
title: ...
client: _example-client
date: YYYY-MM-DD
slug: ...
stage: published
canonical_url: ...
channels: [file, cms, linkedin]
tags: [...]
---
```

Add custom fields the client's CMS requires (e.g., `category`, `featured_image`, `seo_title`, `seo_description`).

---

## CMS: WordPress

```yaml
platform: wordpress
endpoint: https://example.com/wp-json/wp/v2/posts
auth_method: application_password
auth_env_var: WP_APP_PASSWORD       # never hardcode; reference env var
username_env_var: WP_USERNAME
default_status: draft                # publisher creates drafts, human hits publish
default_category_id: 1
format: html                         # convert Markdown → HTML before push
```

## CMS: Ghost

```yaml
platform: ghost
endpoint: https://example.com/ghost/api/admin/posts/
auth_method: jwt_from_admin_key
auth_env_var: GHOST_ADMIN_API_KEY
default_status: draft
format: lexical                      # or html
```

## CMS: Webflow

```yaml
platform: webflow
api_version: v2
site_id_env_var: WEBFLOW_SITE_ID
collection_id_env_var: WEBFLOW_COLLECTION_ID
auth_env_var: WEBFLOW_API_TOKEN
default_status: draft
```

(Keep only the platform you actually use.)

---

## Social: LinkedIn

```yaml
char_limit: 3000
preferred_length: 1200-1800
hook_chars: 200                      # what shows above "see more"
hashtags: 3-5
hashtag_style: lowercase
links_in_post: false                 # link goes in first comment
cta_style: question                  # question / soft / direct
```

Default hashtag set:

- #...
- #...

## Social: X / Twitter

```yaml
char_limit: 280
single_post_target: 240-275
thread_length: 4-7
thread_format: numbered              # "1/n" at end of each post
hashtags: 0-2
links_in_post: true
```

## Social: Threads / Bluesky / Mastodon

```yaml
threads:
  char_limit: 500
bluesky:
  char_limit: 300
mastodon:
  char_limit: 500
  instance: https://...
```

---

## Tags / categories

Default tags applied to every published piece:

- ...
- ...

## SEO defaults

- Meta description length: 150-160 chars
- SEO title format: `{Title} | {Client name}`

---

## TODO when onboarding

- [ ] Pick the CMS platform and delete unused blocks
- [ ] Set environment variables for all credentials in the shell or `.env` (never commit them)
- [ ] Confirm which social channels are active
- [ ] Get the client to confirm `require_confirmation` policy
