# Example adopter overlay

Copy this folder to `adopters/<your-org>/`, then:

```bash
ackit init . --answers adopters/<your-org>/answers.yaml
cp adopters/<your-org>/rules/*.md context/rules/       # then add id, status and generated frontmatter, or write them with `ackit new rule`
cp -r adopters/<your-org>/roles/* context/roles/
ackit validate context
```

Nothing here is required; every file is an overlay on the generic kit.
