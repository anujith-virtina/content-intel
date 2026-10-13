# Social pipeline

Turns a published blog post into a LinkedIn post, an Instagram caption and a shared carousel, then posts
both. Currently configured for Virtina only (`clients/virtina/social.json`).

```
python social/social_pipeline.py fetch 42074            # article -> output/social/_source/42074.json
#   (copywriter writes output/social/{slug}-{date}.json, rules in clients/virtina/style/social.md)
python social/social_pipeline.py render  <pack.json>    # slides + contact sheet + .md preview
python social/social_pipeline.py qa      <pack.json>    # blocking copy gates
python social/social_pipeline.py approve <pack.json>
python social/social_pipeline.py publish <pack.json> --dry-run
python social/social_pipeline.py publish <pack.json>
python social/social_pipeline.py sweep                  # post every approved pack whose article is live
python social/social_pipeline.py check                  # which credentials are present
```

Inside Claude Code, `/social {post-id}` runs the whole sequence.

## What stops a post going out

`publish` and `sweep` hold a pack, and say why, when any of these is true: QA fails, slides are not
rendered, the pack is not approved, the WordPress article is not `publish`, the article URL changed, or a
credential is missing. Each channel is recorded in the pack's `state` after it posts and is never posted
twice.

To skip the approval step, set `"auto_approve": true` in `clients/virtina/social.json`.

## Credentials (one-time, in `.env`)

### LinkedIn — `VIRTINA_LINKEDIN_ACCESS_TOKEN`, `VIRTINA_LINKEDIN_ORG_ID`

1. Create an app at https://www.linkedin.com/developers/apps and associate it with the Virtina company page.
2. On the Products tab request **Community Management API**. LinkedIn reviews this; it is the only product
   that grants `w_organization_social`, the scope needed to post as a company page.
3. Once granted, generate a token with `w_organization_social` (Auth tab > OAuth 2.0 tools) while logged in
   as a page admin. Tokens last 60 days.
4. `VIRTINA_LINKEDIN_ORG_ID` is the number in the page admin URL: `linkedin.com/company/{id}/admin/`.

If the first comment fails with 403 while the post itself succeeds, the token also needs
`w_organization_social_feed`. The post URL is still reported so the comment can be added by hand.

### Instagram — `VIRTINA_IG_ACCESS_TOKEN`, `VIRTINA_IG_USER_ID`

1. The Instagram account must be a Business or Creator account.
2. Create an app at https://developers.facebook.com/apps, add the **Instagram** product, choose
   "API setup with Instagram login", and add the account as a tester.
3. Generate a token there with `instagram_business_basic` and `instagram_business_content_publish`. The
   same screen shows the account's user ID.
4. Tokens last 60 days. Refresh before expiry:
   `GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=...`

If you use Facebook Login instead (token from a Facebook Page), set `graph_host` in `social.json` to
`https://graph.facebook.com`.

Instagram only accepts images from a public URL, so at post time the slides are uploaded to the
virtina.com media library (`social-{slug}-NN.jpg`).

## Running the sweep on a schedule (Windows)

```
schtasks /Create /TN "Virtina social sweep" /SC DAILY /ST 10:00 /TR "python C:\content-intel\social\social_pipeline.py sweep"
```

## Slide design

1080 x 1350 JPEG, Metropolis (the virtina.com body font, SIL OFL, in `social/fonts/`), colours from
`clients/virtina/brand-teal.txt`. Text is auto-sized within a fixed range; if it still does not fit the
render fails rather than shrinking further.
