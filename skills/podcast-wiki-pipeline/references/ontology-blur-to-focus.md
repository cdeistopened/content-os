# Ontology: Blur to Focus

Goal: move from a fuzzy topic cloud to a sharp, orthogonal map.

## Step 1: Fuzzy scan
- Run entity/keyword frequency across chunks.
- Pull top 30-60 terms and co-occurrence pairs.
- Output: a rough cloud (no structure yet).

## Step 2: Broad domains (3-7)
- Cluster terms into 3-7 broad buckets.
- Approve or rename buckets.
- Output: `phase1_domains.json`.

## Step 3: Subtopics per domain
- For each domain, list 6-15 subtopics.
- Remove duplicates and vague overlaps.
- Output: `phase2_subtopics.json`.

## Step 4: Canonical map
- Convert subtopics into frameworks/cases/people buckets.
- Keep cases as one-off stories, not concepts.
- Output: `approved.json`.

## Approval gates
- User approval required after Step 2 and Step 4.
