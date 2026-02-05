---
name: wiki-ontology-design
version: 1.0.0
description: "When the user wants to design a wiki structure by building and refining a layered ontology from a fuzzy topic cloud to a sharp map. Also use when planning information architecture for a new corpus. For multi-source research into wiki pages, see multi-source-research."
---

# Wiki Ontology Design

Use this skill to design the wiki structure for a new corpus.

## Workflow
1. **Fuzzy scan**: extract top terms and co-occurrences.
2. **Broad domains**: 3-7 buckets that define the worldview.
3. **Subtopics**: 6-15 per domain, remove overlaps.
4. **Canonical map**: classify into frameworks, cases, people, episodes.
5. **Approve**: write `approved.json` and generate scaffolds.

## Script
```bash
python3 scripts/ontology_refiner.py --input phase1_domains.json --output approved.json
```

## References
- `references/blur-to-focus.md`
- `references/ontology-schema.json`

## Related Skills

- **Upstream**: **multi-source-research**
- **Enhanced by**: **semantic-chunking-rules**
- **Feeds into**: **podcast-wiki-pipeline**
