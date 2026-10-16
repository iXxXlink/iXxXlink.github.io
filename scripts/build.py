#!/usr/bin/env python3
"""Build the static homepage and matching GitHub Profile README from profile.json."""
import html
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / 'profile.json').read_text())
esc = lambda s: html.escape(str(s), quote=True)
project, contribution = p['projects'][0], p['contributions'][0]
values = {
    'NAME': p['name'], 'HANDLE': p['handle'], 'ROLE': p['role'], 'COMPANY': p['company'],
    'HOMEPAGE': p['homepage'], 'GITHUB': p['github'], 'BIO': p['bio'], 'MISSION': p['mission'],
    'DESCRIPTION': f"{p['name']}, {p['role']} at {p['company']}. Sichuan University graduate, focused on agent applications and agent infrastructure.",
    'PROJECT_TYPE': project['type'], 'PROJECT_NAME': project['name'], 'PROJECT_DESCRIPTION': project['description'], 'PROJECT_URL': project['url'],
    'CONTRIBUTION_NAME': contribution['name'], 'CONTRIBUTION_DESCRIPTION': contribution['description'], 'CONTRIBUTION_LABEL': contribution['label'], 'CONTRIBUTION_URL': contribution['url'],
}
values = {k: esc(v) for k, v in values.items()}
values['FOCUS_CARDS'] = ''.join(f'<article class="focus-card"><div class="focus-top"><span>{esc(f["tag"])}</span><span aria-hidden="true">0{i+1}</span></div><h3>{esc(f["name"])}</h3><p>{esc(f["description"])}</p></article>' for i, f in enumerate(p['focus']))
values['PROJECT_TAGS'] = ''.join(f'<span>{esc(t)}</span>' for t in project['tags'])
template = (ROOT / 'site.template.html').read_text()
page = re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: values[m[1]], template)
(ROOT / 'index.html').write_text(page)
readme = f'''# Hi, I’m {p['name']}

**{p['role']} at {p['company']} · Sichuan University graduate**

{p['bio']}

{p['mission']}

[Personal website]({p['homepage']}) · [Agent Observatory]({project['url']})

## Focus

'''
readme += ''.join(f"- **{f['name']}** — {f['description']}\n" for f in p['focus'])
readme += f'''
## Public work

- **[{project['name']}]({project['url']})** — {project['description']}
- **[{contribution['name']}]({contribution['url']})** — {contribution['description']} Submitted pull request; the linked PR shows its current status.

## Let’s collaborate

I’m interested in agent applications, execution harnesses, and reproducible evaluation. I welcome conversations around practical tools, useful experiments, and focused open-source improvements.

Explore my repositories and contributions here on GitHub, or visit my [personal website]({p['homepage']}).

---

Personal work and views. This profile is maintained alongside my [website source](https://github.com/{p['handle']}/{p['handle']}.github.io).
'''
(ROOT / 'PROFILE_README.md').write_text(readme)
print('Built index.html and PROFILE_README.md from profile.json.')
