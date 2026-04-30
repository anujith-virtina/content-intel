# Content Intelligence Agent

A multi-client, multi-stage content pipeline built for Claude Code. Research → Analyze → Create → Publish, with each stage running as an isolated sub-agent.

## What this is

Four specialized sub-agents that work together:

- **researcher** — finds primary sources, scans competitors, identifies gaps
- **analyzer** — turns research into a sharp, opinionated brief
- **creator** — drafts content matching the client's voice
- **publisher** — formats, pushes to CMS, generates social variants

The orchestrator (root `CLAUDE.md`) coordinates them. You stay in the driver's seat at every checkpoint.

## Setup

1. Install Claude Code if you haven't:

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. Drop this whole folder anywhere on your machine.

3. Open a terminal in this folder and run:

   ```bash
   claude
   ```

4. Claude Code reads `CLAUDE.md` automatically and discovers the four sub-agents in `.claude/agents/`.

5. Verify with `/agents` — you should see researcher, analyzer, creator, publisher.

## Onboard your first client

```
/onboard acme-corp
```

The orchestrator walks you through filling in:

- `clients/acme-corp/style/voice.md` — tone, banned words, sentence rules
- `clients/acme-corp/style/audience.md` — who reads this
- `clients/acme-corp/style/brand.md` — positioning, off-limits topics
- `clients/acme-corp/style/cms.md` — WordPress/Ghost/Webflow + social configs
- `clients/acme-corp/style/examples.md` — past content that worked

Takes 10-15 minutes per client. Worth it — the agents read these files every run and the output quality scales with how good these are.

## Run the full pipeline

```
/content acme-corp how AI changes content marketing in 2026
```

You'll get checkpoints between every stage. Approve, edit, or redirect.

## Run a single stage

Just talk to the orchestrator:

- "Research X for acme-corp" — researcher only
- "Critique this draft for acme-corp: [paste]" — analyzer only
- "Rewrite this paragraph in acme-corp voice: [paste]" — creator only
- "Format and publish this draft for acme-corp to LinkedIn and WordPress" — publisher only

## Folder layout

```
content-intel/
├── CLAUDE.md                       # orchestrator instructions
├── README.md                       # this file
├── .claude/
│   ├── agents/
│   │   ├── researcher.md
│   │   ├── analyzer.md
│   │   ├── creator.md
│   │   └── publisher.md
│   └── commands/
│       ├── content.md              # /content slash command
│       └── onboard.md              # /onboard slash command
├── templates/
│   ├── research-notes.md
│   ├── brief.md
│   └── article.md
└── clients/
    ├── _example-client/            # template — copy this for new clients
    │   ├── style/
    │   │   ├── voice.md
    │   │   ├── audience.md
    │   │   ├── brand.md
    │   │   ├── examples.md
    │   │   └── cms.md
    │   └── output/
    │       ├── research/
    │       ├── briefs/
    │       ├── drafts/
    │       ├── published/
    │       └── social/
    └── acme-corp/                  # your real clients live alongside
        └── ...
```

## Credentials

Never put API keys, tokens, or passwords in any file in this repo.

The `cms.md` files reference environment variables by name (e.g., `WP_APP_PASSWORD`). Set them in your shell, a `.env` file (gitignored), or your secrets manager. The publisher reads them at runtime.

If you commit this to git, add `.env` and any local secrets to `.gitignore`.

## Tips

- The pipeline pauses between every stage. That's the feature, not a bug — multi-agent chains compound errors fast, and the human checkpoint is the cheapest quality gate you have.
- Style files are everything. A weak `voice.md` produces generic output no matter how good the brief is.
- The `examples.md` file matters more than you think. The creator pattern-matches cadence from real samples better than from rules.
- Onboarding a new client is just `cp -r clients/_example-client clients/{new-slug}` plus filling in the style files.
- Add per-client slash commands in `.claude/commands/` if a client has a recurring workflow (e.g., `/weekly-newsletter acme-corp`).

## Extending

- **Add a new sub-agent** — drop a new `.md` file in `.claude/agents/` with frontmatter (`name`, `description`, `tools`, `model`) and a system prompt.
- **Add MCP servers** — connect Notion, Airtable, Slack, or your CMS directly via MCP for first-class tool access instead of API calls in the publisher.
- **Add evaluation** — create an `evaluator` sub-agent that scores drafts against the brief before they reach publish.

## Troubleshooting

- Sub-agents don't show up in `/agents` → restart your Claude Code session, or run `/agents` to force a reload.
- Publisher fails on CMS push → check that the env vars in `cms.md` are actually set (`echo $WP_APP_PASSWORD`).
- Voice drift in drafts → strengthen `voice.md` with more specific banned words and add another example to `examples.md`.
