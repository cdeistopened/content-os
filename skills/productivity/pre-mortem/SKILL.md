---
name: pre-mortem
description: Run a pre-mortem analysis on any project by imagining failure and working backward. Brings in domain-specific expert personas to surface uncomfortable truths before they become real problems.
---

# Pre-Mortem Analysis Skill

"It's [future date]. The project has failed. What went wrong?"

Based on Gary Klein's prospective hindsight method, which increases risk identification accuracy by 30% compared to standard critiquing.

## When to Use

- Before launching a major project or initiative
- When committing significant time/money to a goal
- When you feel overconfident about a plan
- At project kickoffs to surface concerns
- Quarterly reviews to reassess trajectory

## The Core Method

### Step 1: Set the Scene

State the project and the failure scenario vividly:

> "It's [date 6-12 months out]. The [project name] has failed to achieve [specific goal]. We're looking back to understand what went wrong."

Be specific about what failure looks like. Not "it didn't work" but "we have 12K subscribers instead of 100K" or "we shipped 2 months late and lost the client."

### Step 2: Assemble the Expert Panel

Based on project type, select 4-6 expert personas. Each brings a different failure lens.

**Default panels by project type:**

| Project Type | Expert Panel |
|--------------|--------------|
| **YouTube/Content** | Algorithm Expert, Content Strategist, Creator Coach, Audience Researcher, Growth Hacker |
| **Product Launch** | VC/Investor, Product Manager, Customer Success, Go-to-Market Strategist, UX Researcher |
| **Content Business** | Platform Risk Analyst, Community Builder, Newsletter Operator, Monetization Expert, Content Ops |
| **Creative Project** | Producer, Client Advocate, Shipping Coach, Art Director, Scope Manager |
| **Software/Tech** | Technical Architect, QA Lead, DevOps, Security Analyst, User Advocate |

**Universal personas (add to any panel):**
- The Skeptical Customer ("Why wouldn't I just use X?")
- The Accountant ("Show me the math")
- The Pessimist ("What's the worst realistic outcome?")
- The Competitor ("How would I attack this?")

### Step 3: Run Each Expert's Analysis

For each expert persona, identify:

1. **Top 3-5 failure modes** - What specifically went wrong from their perspective?
2. **Early warning signs** - What signals would have predicted this failure?
3. **Prevention requirements** - What must be true to avoid this failure?

**Key rule:** During brainstorming, no solutions allowed - only failure modes. Solutions come after all risks are surfaced.

### Step 4: Identify Systemic Patterns

Look across all expert analyses for:
- **Repeated themes** - What failure modes appear in multiple perspectives?
- **Hidden assumptions** - What are we taking for granted?
- **Resource gaps** - Where do ambitions exceed allocated resources?
- **Single points of failure** - What one thing going wrong kills the project?

### Step 5: Prioritize and Plan

For each failure mode, score:
- **Likelihood** (1-5): How probable is this?
- **Severity** (1-5): How bad if it happens?
- **Detection** (1-5): How easily can we spot it early?

**Risk Score** = Likelihood × Severity

Focus mitigation efforts on highest-scoring risks with low detection scores.

### Step 6: Define Checkpoints

Set specific dates to reassess:
- What metrics at Month 3 would trigger strategy revision?
- What early warning signs are we actively monitoring?
- When is the "pivot or persist" decision point?

---

## Expert Persona Details

### YouTube/Content Experts

**Algorithm Expert**
Analyzes: Watch time, CTR, session duration, browse vs. search traffic, recommendation patterns

Key questions:
- Where do viewers drop off?
- What's our browse traffic percentage?
- Is our niche large enough for algorithmic reach?
- Are we optimizing for discoverability or vanity?

**Content Strategist**
Analyzes: Content pillars, audience-content fit, transformation narrative, format consistency

Key questions:
- Can you explain the channel's value in one sentence?
- What's the signature format?
- Are we teaching or transforming?
- Who is this actually for?

**Creator Coach**
Analyzes: Sustainability, systems, emotional resilience, execution consistency

Key questions:
- Can this be maintained for 2 years with no viral hits?
- What's the backup plan when life gets busy?
- How do we handle underperformance emotionally?
- Is perfectionism killing volume?

**Audience Researcher**
Analyzes: Demographics, psychographics, platform fit, competitive landscape

Key questions:
- Does this audience actually exist at scale?
- Is YouTube where they learn?
- What do they watch already?
- Have we validated demand before building?

**Growth Hacker**
Analyzes: Distribution, collaboration, cross-platform amplification, owned audience

Key questions:
- What happens after we hit publish?
- How many distribution channels per video?
- What's the collaboration strategy?
- Do we have any owned audience?

### Product Launch Experts

**VC/Investor**
Analyzes: Market size, team, traction, defensibility, unit economics

Key questions:
- What's the TAM? SAM? SOM?
- Why this team?
- What's the unfair advantage?
- When do unit economics work?

**Product Manager**
Analyzes: Feature prioritization, user stories, MVP definition, feedback loops

Key questions:
- What's the one feature that matters?
- What's explicitly out of scope?
- How fast is our learning loop?
- Have we shipped anything users can react to?

**Customer Success**
Analyzes: Onboarding friction, churn predictors, support burden, satisfaction

Key questions:
- What makes customers quit in 30 days?
- Where does onboarding break?
- What support tickets will overwhelm us?
- How do we know if customers are successful?

**Go-to-Market Strategist**
Analyzes: Positioning, distribution, pricing, competitive response

Key questions:
- How do customers hear about us?
- What's the acquisition cost?
- How will competitors respond?
- Is the pricing validated?

---

## Output Formats

### Quick Format (5 min review)

```
PROJECT: [Name]
GOAL: [Specific target]
FAILURE SCENARIO: [What failure looks like]

TOP 5 RISKS:
1. [Risk] - Score: X/25 - Owner: [Name]
2. [Risk] - Score: X/25 - Owner: [Name]
3. [Risk] - Score: X/25 - Owner: [Name]
4. [Risk] - Score: X/25 - Owner: [Name]
5. [Risk] - Score: X/25 - Owner: [Name]

SINGLE MOST LIKELY FAILURE:
[One paragraph]

IMMEDIATE ACTIONS:
- [ ] Action - Owner - Due
- [ ] Action - Owner - Due
- [ ] Action - Owner - Due
```

### Standard Format (Full Analysis)

```
# Pre-Mortem: [Project Name]

## The Failure Scenario
[Date]. [Vivid description of what failure looks like]

## Expert Panel Analysis

### [Expert 1 Name]
**Failure Modes:**
1. [Failure mode with explanation]
2. [Failure mode with explanation]
3. [Failure mode with explanation]

**Early Warning Signs:**
- [Signal to watch]
- [Signal to watch]

**Prevention Requirements:**
- [What must be true]

[Repeat for each expert]

## Systemic Patterns
- [Pattern across experts]
- [Pattern across experts]

## Risk Register

| Risk | Likelihood | Severity | Score | Owner | Mitigation |
|------|------------|----------|-------|-------|------------|
| [Risk 1] | 4 | 5 | 20 | [Name] | [Plan] |

## The Uncomfortable Truth
[Single most likely failure mode, stated bluntly]

## Checkpoints
- Month [X]: [What metrics trigger revision?]
- [Warning sign]: [Response if detected]

## Pre-Commitments Required
- [ ] [What must be secured before starting]
```

---

## Question Bank by Category

### Resource Questions
- What if the budget gets cut 50%?
- What if the timeline shrinks by 25%?
- What if our key person is unavailable for a month?
- What are we assuming we'll have that we don't have yet?

### Execution Questions
- What's the single point of failure?
- Where will communication break down?
- Which handoffs are likely to drop things?
- What will we underestimate?

### Market Questions
- What competitor move would hurt us most?
- What market change could make this irrelevant?
- What assumption about demand might be wrong?
- Who else is building this right now?

### Team Questions
- Who might leave mid-project?
- What skills are we missing?
- Where is expertise concentrated in one person?
- What happens if morale drops?

### External Questions
- What regulatory/platform change could impact us?
- What dependency could change their terms?
- What economic shift would matter?
- What seasonal factor are we ignoring?

---

## Usage Examples

### Example 1: YouTube Channel Launch

```
/pre-mortem

Project: Skill Stack YouTube Channel
Goal: 100,000 subscribers by December 2026
Timeline: 12 months

Context:
- Creator: Charlie Deist (part-time, has day job)
- Niche: AI skills, context engineering
- Starting point: Near zero subscribers
- Resources: Solo creator, no team yet
```

### Example 2: Product Launch

```
/pre-mortem

Project: Writer's IDE Launch
Goal: 500 paying customers in first 90 days
Timeline: 3 months

Context:
- Product: Lightweight content engine wrapping Claude Code
- Price: $90 lifetime + $500-2000 setup
- Target: People who would otherwise hire ghostwriters
- Team: 1 developer, 1 marketer
```

### Example 3: Creative Project

```
/pre-mortem

Project: Commissioned video series for client
Goal: 10 videos delivered, client satisfied, paid in full
Timeline: 6 weeks

Context:
- Client: [Company]
- Budget: $15,000
- Deliverables: 10 x 60-second social videos
- Team: Director, editor, animator
```

---

## Tips for Effective Pre-Mortems

1. **Be specific about failure** - "It didn't work" isn't useful. "We had 12K subscribers and burned out at month 8" is useful.

2. **Don't defend the plan** - The point is to find holes, not prove the plan is good.

3. **Welcome uncomfortable truths** - If nothing feels uncomfortable, you're not being honest.

4. **Distinguish likely from catastrophic** - A meteor strike is catastrophic but not likely. Focus on likely failures.

5. **Assign owners immediately** - A risk without an owner is a risk ignored.

6. **Set a review date** - Pre-mortems aren't one-time events. Revisit quarterly.

7. **Use it to scope down** - Often the best outcome is realizing the goal needs adjustment.

---

## Sources

- Gary Klein - "Performing a Project Premortem" (HBR, 2007)
- Dragonfly Thinking - Pre-Mortem Analysis Framework
- FMEA (Failure Mode and Effects Analysis) - ASQ
- Tim Ferriss - Fear-Setting Exercise
- Red Team thinking (McChrystal Group)

---

*The goal of a pre-mortem isn't to predict the future. It's to expand your imagination about what could go wrong so you're not blindsided when it does.*
