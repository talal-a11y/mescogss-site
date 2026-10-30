# mescogss-site

Two static deployments of the MESCO GSS website, built by Bidaya.

- `old/` — the original WordPress/Elementor site exported to static HTML, exactly as it was live (reference only; forms are inert).
- `new/` — the redesign. Same wording, palette, fonts, logo and images; new layouts and transitions. Built from `build.py` + `content.py` (run `python3 build.py` to regenerate `new/`).

Each folder is its own Vercel project (Root Directory = `old` or `new`, framework = Other, no build step).
