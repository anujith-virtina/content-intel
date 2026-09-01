# CMS — eldercarematters

## Target

WordPress at https://eldercarematters.com/

Verified against the live REST API on 2026-09-01.

| Property | Value |
|---|---|
| Site name | Elder Care Directory - ElderCareMatters.com |
| REST root | `https://eldercarematters.com/wp-json/` |
| Posts endpoint | `/wp-json/wp/v2/posts` |
| Public read access | Yes, no auth needed for GET |
| Namespaces present | `wp/v2`, `yoast/v1`, `wc/v3`, `wordfence/v1`, `wordfence-login-security/v1`, `saswp-output`, `inavii/v1`, `inavii/v2` |

## Page builder: none

This is the important difference from the other clients in this repo.

Posts are plain semantic HTML in `post_content`. Verified on post 283258: zero Elementor markup, zero Gutenberg `wp-block` classes, no Divi `et_pb`, no Thrive `tve`.

**So:**
- No `_elementor_data` payload (unlike chatsku and impelhub)
- No `_tve_updated_post` problem (unlike virtina)
- Just write clean `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>`, `<table>` and push it

This makes ECM the simplest client to publish to. Do not import build scripts from the other clients.

## Plugins that matter

- **Yoast SEO** (`yoast/v1` namespace present). **Yoast fields are NOT exposed in the REST `meta` object on this install.** Verified 2026-09-01: a `context=edit` read of post 283258 returns only `_acf_changed` and `footnotes` in `meta`. Neither `_yoast_wpseo_title` nor `_yoast_wpseo_metadesc` is registered. Expect to set Yoast title and description **manually in the WP dashboard**, the same situation as Virtina post 42441. Still attempt the REST write on the first push and re-read with `context=edit`, because the ChatSKU install behaved this way until it did not. Do not claim they persisted without verifying.
- **ACF** (Advanced Custom Fields) is active (`_acf_changed` present in post meta). Check whether any ACF field drives layout before assuming `post_content` is the whole post.
- **Wordfence** with login security. Expect rate limiting and possible blocking on repeated failed auth. Do not hammer the API.
- **WooCommerce** (`wc/v3`). The directory listings are sold through it. Do not touch WooCommerce endpoints.
- **SASWP** (Schema and Structured Data for WP) is generating schema already. Check what it outputs before adding hand-written JSON-LD, or you will produce duplicate schema.

## Credentials

**Configured and verified 2026-09-01.**

```
ECM_WP_USERNAME=<in .env, line 7>
ECM_WP_APP_PASSWORD=<in .env, line 8>
```

Values live only in `.env`, which is gitignored. **This repository is public**, so never write a username or password into a tracked file.

Verified with an authenticated `GET /wp-json/wp/v2/users/me?context=edit`:

| Property | Value |
|---|---|
| User ID | 6135 |
| Name | (see `.env`) |
| Role | administrator |
| edit_posts / publish_posts | true / true |
| upload_files | true |
| edit_others_posts / edit_published_posts | true / true |
| manage_categories | true |

Never reuse another client's credentials. These are four separate WordPress installations.

## Publishing rules

- Status always `draft`. Never auto-publish.
- `featured_media` must be a real media ID, never 0. Post 283258 uses 283598.
- Existing drafts on the site: 1 as of 2026-09-01. Do not touch drafts you did not create.
- Default author on recent posts is user 6068, not our user 6135. Confirm which author new posts should carry.
- Categories: pull the real ID from `/wp-json/wp/v2/categories`. The taxonomy is enormous and granular (thousands of terms, e.g. 12639 "Adult Day Care Services for Seniors", 174 "Assisted Living", 5583 "Aging in Place"). Never guess an ID.
- Yoast title: 60 characters max
- Yoast description: 150 to 160 characters

## Post format standard

Match post 283258 (`/assisted-living-vs-home-care/`, published 2026-08-13), which is the current best example on the site:

- 1,500 to 1,800 words
- H2 sections in Title Case, H3 subsections
- One comparison table when weighing two options
- Numbered question lists the reader can act on
- A decision checklist before the closing section
- A final section that answers the title question directly
- 2 body images
- About 6 internal links, 2 or fewer external links to authoritative sources

### Images, verified from post 283258

| | |
|---|---|
| Featured image | 1024 x 536, **WebP** (media 283598) |
| Body images | 2, both WebP, no explicit width/height attributes in the markup |
| Body image alt text | present, 70 and 63 characters |
| Featured image alt text | **empty** |

The featured image carrying no alt text is an accessibility and SEO gap on the site's own best post. Set alt text on every image we upload, featured included, 80 to 150 characters.

WebP is the site's working format. Upload WebP rather than JPEG to match, and confirm the media endpoint accepts it before a real push.

### Links, verified from post 283258

Internal links point at directory category pages, not other blog posts: `/assisted-living/`, `/memory-care/`, `/home-care-providers/`. That is the house pattern, and it matches the business model. Send readers into the directory.

The 2 external links both go to CareScout and Genworth for cost-of-care data. That confirms the site is willing to cite a commercial source for cost figures, but it dates them. Prefer government sources where one exists.

Older posts (280614, 280620) run 436 to 542 words with no images and no tables. Do not use them as a model.

## Frontmatter for local files

```yaml
---
title: ...
client: eldercarematters
date: YYYY-MM-DD
topic: ...
audience: ...
stage: research | brief | draft | published
slug: ...
---
```

## Social

Unknown. No channels confirmed.

## TODO when onboarding

- [x] Add `ECM_WP_USERNAME` and `ECM_WP_APP_PASSWORD` to `.env` and verify with an authenticated GET (done 2026-09-01, administrator, user 6135)
- [x] Test whether Yoast fields are REST-writable (they are **not exposed** in `meta`; expect manual dashboard entry)
- [x] Confirm image dimensions used by the theme (featured 1024x536 WebP; body images WebP, no fixed attributes)
- [ ] Check what schema SASWP already emits, to avoid duplicating it
- [ ] Confirm the default category and author for new posts (recent posts use author 6068, we authenticate as 6135)
- [ ] Confirm whether ACF fields affect post layout
- [ ] Test a WebP media upload before the first real push
- [ ] Confirm social channels, if any
