# SEO Research

Strategic keyword research and content planning. Use this skill BEFORE writing to identify opportunities, validate topics, and create a research brief.

## When to Use This Skill

Use when:
- Planning new SEO content (before writing)
- Identifying keyword opportunities for a topic
- Validating whether a topic is worth pursuing
- Creating a content calendar
- Finding content that needs refresh
- Researching what's ranking for a keyword

DO NOT use for:
- Actually writing the content (use `seo-content-writer`)
- Quick social posts or newsletters
- Content that doesn't need SEO optimization

---

## Credentials Location

Credentials are stored in `Studio/SEO Article Factory/credentials/`:
- `.env` - DataForSEO login, GA4 property ID
- `ga4-credentials.json` - Google service account

---

## The Research Process

```
SEED → EXPAND → VALIDATE → PRIORITIZE → BRIEF
```

1. **Seed** - Start with topic/keyword idea
2. **Expand** - Use 6 Circles Method to find related keywords
3. **Validate** - Run 4 tests to confirm it's worth pursuing
4. **Prioritize** - Score by business value and opportunity
5. **Brief** - Create research brief for writing

---

## Phase 1: Seed & Initial Research

### Check Existing Content First

Before anything else, see what OpenEd already has. Check the Content Map in `Studio/SEO Article Factory/Content Map.md` for planned and published articles.

### Keyword Research Tools

**DataForSEO** (credentials in `.env`):
- Use their API or dashboard for keyword ideas, search volume, difficulty
- Get SERP analysis for top competitors
- Check OpenEd's current rankings

**Free alternatives:**
- Google Search Console (if GA4 access works)
- Ubersuggest free tier
- AnswerThePublic for question keywords
- AlsoAsked.com for PAA questions
- Google autocomplete and related searches

### Check GA4 for Performance Context

If GA4 service account is working:
- Top performing content (what's working)
- Declining content (refresh candidates)
- Traffic trends by topic cluster

---

## Phase 2: Expand with 6 Circles Method

For each seed keyword, expand using 6 different lenses:

### Circle 1: What OpenEd Offers
Products, services, and solutions directly related to this topic.

**Questions to answer:**
- What OpenEd features connect to this topic?
- What curriculum/approach categories apply?
- What tools or resources do we offer?

### Circle 2: Problems This Solves
Pain points and challenges the audience faces.

**Questions to answer:**
- What frustrations bring parents to search this?
- What isn't working in their current approach?
- What are they afraid of getting wrong?

### Circle 3: Outcomes They Want
Results and transformations families are seeking.

**Questions to answer:**
- What does success look like for this topic?
- What transformation are they hoping for?
- What would make them feel confident?

### Circle 4: OpenEd's Unique Positioning
What makes OpenEd's perspective different.

**Questions to answer:**
- What do we know that competitors don't?
- What podcast guests have discussed this?
- What community insights do we have?

### Circle 5: Adjacent Topics
Related areas where the audience spends time.

**Questions to answer:**
- What else are they researching alongside this?
- What broader categories does this fit into?
- What complementary topics should we cover?

### Circle 6: Entities to Associate With
People, methods, curricula, tools to connect with.

**Questions to answer:**
- What specific curricula or methods relate?
- What thought leaders discuss this?
- What tools or platforms are relevant?

### Expansion Patterns

For each keyword, generate variations:

**Question patterns:**
- What is [keyword]?
- How to [keyword]?
- Why [keyword]?
- Best [keyword]?
- [keyword] vs [alternative]?
- [keyword] examples
- [keyword] for [age/grade]

**Modifier patterns:**
- [keyword] curriculum
- [keyword] resources
- [keyword] for beginners
- [keyword] schedule
- [keyword] 2025
- [keyword] for [learning style]

**Comparison patterns:**
- [keyword A] vs [keyword B]
- best [category]
- [method] alternatives
- [curriculum] review

---

## Phase 3: Validate with 4 Tests

Before committing to a topic, run these 4 validation tests:

### Test 1: Search Volume Test

**Question:** Does this topic have >1,000 monthly searches across its keyword cluster?

**How to check:**
- Use DataForSEO or free keyword tools
- Sum volume across related terms
- If total cluster volume <1,000, this is NOT a pillar - maybe a single article

**Pass/Fail:**
- ✅ PASS: Cluster has 1,000+ monthly searches
- ❌ FAIL: Not enough search demand

### Test 2: Market-Centric Test

**Question:** Is this something the MARKET searches for, or something WE want to talk about?

| Product-Centric (Wrong) | Market-Centric (Right) |
|-------------------------|------------------------|
| "OpenEd methodology" | "homeschool curriculum" |
| "Our approach to learning" | "how to start homeschooling" |
| "Why OpenEd is different" | "best homeschool methods" |
| Features we offer | Problems parents search |

**Pass/Fail:**
- ✅ PASS: People actually search for this
- ❌ FAIL: We're talking to ourselves

### Test 3: Competitive Reality Test

**Question:** Can OpenEd actually win here?

**How to check:**
- Search the keyword in Google
- Look at who's ranking in top 3

**Evaluation:**
- All DR 80+ sites (Forbes, HubSpot, etc.)? → Find adjacent topic
- Mix of authority and smaller sites? → Winnable with great content
- Thin content from unknown sites? → High opportunity

**Pass/Fail:**
- ✅ PASS: Realistic path to page 1
- ❌ FAIL: Dominated by unbeatable competitors

### Test 4: Proprietary Advantage Test

**Question:** Do we have unique content, data, or expertise?

| Advantage | Priority |
|-----------|----------|
| Podcast interviews on this topic | Prioritize highly |
| Community discussions/insights | Prioritize highly |
| Newsletter coverage | Prioritize |
| Same info everyone else has | Deprioritize |

**How to check:**
- Search podcast transcripts in `Content/Open Ed Podcasts/`
- Check newsletter archive
- Query NotebookLM for related content

**Pass/Fail:**
- ✅ PASS: We have proprietary insights
- ❌ FAIL: We'd just be aggregating web content

### Validation Summary

```
Topic: [Your Topic]

Test 1 (Search Volume): PASS/FAIL - [evidence]
Test 2 (Market-Centric): PASS/FAIL - [evidence]
Test 3 (Competitive):    PASS/FAIL - [evidence]
Test 4 (Proprietary):    PASS/FAIL - [what we have]

VERDICT: VALID PILLAR / DEMOTE TO ARTICLE / REMOVE
```

**If 2+ tests fail, don't pursue as a pillar.** Either demote to single article or remove entirely.

---

## Phase 4: Prioritize

### Priority Matrix

Score each validated topic:

#### Business Value (High / Medium / Low)

**High:** Direct path to OpenEd signups
- Commercial intent keywords
- Close to decision point
- Core offering topics

**Medium:** Indirect path
- Builds trust and authority
- Educational content
- Captures email subscribers

**Low:** Brand awareness only
- Top of funnel
- Tangentially related

#### Opportunity (High / Medium / Low)

**High opportunity signals:**
- No good content exists (category definition opportunity)
- Existing content is outdated (2+ years old)
- Existing content is thin/generic
- We have unique angle competitors miss
- Growing search trend

**Low opportunity signals:**
- Dominated by major sites
- Excellent content already exists
- Declining interest

#### Speed to Win (Fast / Medium / Long)

**Fast (3 months):** Low competition, we have unique data
**Medium (6 months):** Moderate competition, comprehensive content needed
**Long (9-12 months):** High competition, authority building required

### Priority Decision

| Business Value | Opportunity | Speed | Priority |
|---------------|-------------|-------|----------|
| High | High | Fast | **DO FIRST** |
| High | High | Medium | **DO SECOND** |
| High | Medium | Fast | **DO THIRD** |
| Medium | High | Fast | **QUICK WIN** |
| High | Low | Any | **LONG PLAY** |
| Low | Any | Any | **BACKLOG** |

---

## Phase 5: Gather Proprietary Sources

Before creating the brief, collect OpenEd-specific insights:

### Query NotebookLM

Use the notebooklm skill to query for content:
- "What content exists about [YOUR TOPIC]?"
- "What have podcast guests said about [TOPIC]?"
- "What insights are unique to OpenEd?"

### Search Podcast Transcripts

Look in `Content/Open Ed Podcasts/` for relevant discussions.

### Check Newsletter Archive

Query NotebookLM for OpenEd Daily coverage of the topic.

### Find Internal Link Opportunities

Check existing Hub pages and blog content in `Studio/Open Education Hub/` and `Studio/SEO Article Factory/Content Map.md`.

---

## Phase 6: Create Research Brief

### Research Brief Template

```markdown
# Research Brief: [Topic]

**Date:** [YYYY-MM-DD]
**Priority:** [DO FIRST / DO SECOND / QUICK WIN / etc.]

---

## SEO Foundation

**Primary Keyword:** [exact phrase]
**Search Volume:** [monthly]
**Keyword Difficulty:** [score]

**Secondary Keywords:**
- [keyword] - [volume]
- [keyword] - [volume]
- [keyword] - [volume]

**Search Intent:** [Informational / Commercial / Transactional]

---

## Validation Results

| Test | Result | Evidence |
|------|--------|----------|
| Search Volume | PASS/FAIL | [cluster total] |
| Market-Centric | PASS/FAIL | [evidence] |
| Competitive | PASS/FAIL | [who's ranking] |
| Proprietary | PASS/FAIL | [what we have] |

---

## Competitive Landscape

**Top 3 Ranking Articles:**
1. [Title] - [URL] - [Word count] - [What they do well]
2. [Title] - [URL] - [Word count] - [What they do well]
3. [Title] - [URL] - [Word count] - [What they do well]

**Content Gaps (What's Missing):**
- [Gap 1]
- [Gap 2]
- [Gap 3]

**Our Unique Angle:**
[What makes OpenEd's take different]

---

## Proprietary Sources

**Podcast Coverage:**
- [Guest Name]: "[Key quote or insight]"
- [Guest Name]: "[Key quote or insight]"

**Newsletter Coverage:**
- [Issue #]: [Topic covered]

**Community Insights:**
- [Insight from Slack/community]

---

## Recommended Structure

**Content Type:** [Pillar Guide / How-To / Comparison / Listicle]
**Target Word Count:** [based on competition]

**Proposed Outline:**
1. H2: [Section]
2. H2: [Section]
3. H2: [Section]
4. H2: [Section]
5. H2: FAQ

---

## Internal Linking Opportunities

**Link TO this article from:**
- [Existing article URL]
- [Existing article URL]

**Link FROM this article to:**
- [Related OpenEd content URL]
- [Related OpenEd content URL]
- [Related OpenEd content URL]

---

## Meta Elements (Draft)

**Meta Title (50-60 chars):**
[Draft title]

**Meta Description (150-160 chars):**
[Draft description]

**URL Slug:**
/blog/[slug]

---

## Next Steps

1. [ ] Gather full quotes from podcast transcripts
2. [ ] Write article using `seo-content-writer` skill
3. [ ] Review and publish
4. [ ] Update Content Map with status
```

---

## 90-Day Content Calendar Template

For planning multiple pieces:

```markdown
# 90-Day SEO Content Calendar

## Month 1: Foundation

**Week 1-2:** [Flagship Pillar]
- Keyword: [primary]
- Priority: DO FIRST
- Word count: [target]

**Week 3:** [Supporting Article]
- Keyword: [primary]
- Links to: [pillar]

**Week 4:** [Supporting Article]
- Keyword: [primary]
- Links to: [pillar]

## Month 2: Expansion

**Week 5-6:** [Second Pillar]
...

## Month 3: Depth

**Week 9-10:** [Third Pillar or Major Refresh]
...

## Quick Wins (Anytime)

- [Low-competition keyword] - [why quick]
- [Low-competition keyword] - [why quick]

## Backlog (Future)

- [Topic] - [reason to defer]
- [Topic] - [reason to defer]
```

---

## Output

This skill produces:
1. **Validation summary** - Pass/fail on 4 tests
2. **Research brief** - Complete brief for writing phase
3. **Content calendar** - If planning multiple pieces

The research brief then feeds into the `seo-content-writer` skill for actual content creation.
