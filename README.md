# AI Workflow Vault

Private integrated vault for reusable AI production workflows.

Current purpose:

- Save proven workflows as reusable playbooks.
- Give each workflow a dedicated landing page.
- Publish one integrated GitHub Pages site for navigation and review.
- Keep implementation templates, prompts, QA checklists, and examples together.

## Workflows

| Workflow | Purpose | Status |
|---|---|---|
| YouTube Shorts AI Learning Video | Turn an AI concept into a researched, narrated, premium 9:16 educational Short | v1 saved |
| Design Workflow Studio | Placeholder for the separate UI/UX design workflow; can be imported next | planned |

## Structure

```text
workflows/
  youtube-shorts-ai-learning/
    README.md
    workflow.md
    prompts/
    templates/
    scripts/
    examples/
site/
  index.html
  workflows/youtube-shorts-ai-learning.html
.github/workflows/pages.yml
```

## GitHub Pages

This repo is private. Pages deployment uses GitHub Actions and publishes the static files from `site/`.

If Pages is enabled for the private repo, the site will be available at the repository Pages URL.

## Safety

- Do not commit API keys, OAuth tokens, raw credentials, or local `.env` files.
- Large generated videos/audio should usually stay in Drive or artifact storage; commit scripts, prompts, metadata, and QA notes instead.
- Public YouTube upload remains a separate approval step.
