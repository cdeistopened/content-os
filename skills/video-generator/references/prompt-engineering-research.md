---
title: "Video Prompt Engineering Research"
date: 2026-02-03
status: raw
sources:
  - https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide
  - https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
  - https://deepmind.google/models/veo/prompt-guide/
  - https://github.com/snubroot/Veo-3-Prompting-Guide
  - https://fal.ai/learn/devs/veo3-prompt-guide-master-google-video-generation
  - https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide
  - https://cookbook.openai.com/examples/sora/sora2_prompting_guide
  - https://venice.ai/blog/the-complete-guide-to-ai-video-prompt-engineering
  - https://skywork.ai/blog/how-to-audio-aware-prompting-veo-3-1-guide/
  - https://skywork.ai/blog/multi-prompt-multi-shot-consistency-veo-3-1-best-practices/
  - https://www.dreamhost.com/blog/veo-3-1-prompt-guide/
  - https://www.lovart.ai/blog/ai-video-prompts
---

# Video Prompt Engineering Reference

Comprehensive research on prompt engineering for AI video generation, with primary focus on Google Veo 3.1. Principles drawn from Veo, Runway Gen-4, Sora 2, and general AI video generation best practices.

---

## 1. Fundamental Principles

### Think Like a Cinematographer, Not a Chatbot
AI video models are trained on professional film and video data. They understand cinematography terminology far better than casual descriptions. "A woman walking in a garden" produces generic output. "Medium tracking shot of a woman in a linen dress walking through a sunlit herb garden, shallow depth of field, golden hour backlighting" produces cinema.

### Start Simple, Then Layer
Every major model vendor (Google, Runway, OpenAI) recommends the same workflow: begin with a simple prompt, evaluate the output, then add one variable at a time. Trying to build the perfect prompt on the first attempt almost always fails.

### One Shot = One Scene = One Action
Each generation is 4-8 seconds. Treat every generation as a single shot on a storyboard. Do not try to pack multiple scene changes, subject actions, or style shifts into one prompt. One clear camera move and one clear subject action per shot.

### Describe What You Want, Not What You Don't Want
Negative phrasing ("no blurry footage," "don't show text") often produces unpredictable or opposite results. Use dedicated negative prompt fields where available. When writing negative prompts, describe the unwanted element as a noun/adjective (e.g., "walls, frames, blur") rather than instructive language ("no walls," "don't blur").

### Optimal Prompt Length
Veo sweet spot: 150-300 characters. Below 100 yields generic results. Above 400 causes unpredictable prioritization where the model drops elements. Sora and Runway have similar thresholds -- concise beats verbose every time.

---

## 2. Prompt Architecture

### The Five-Element Framework (Veo-Optimized)

Structure prompts in this hierarchy. You do not need all five for every prompt, but this is the order of priority:

1. **Shot Specification** -- camera work, framing, movement
2. **Setting & Atmosphere** -- location, time, weather, lighting
3. **Subject Specification** -- who/what, with enough visual detail for consistency
4. **Action Sequence** -- what happens, described in beats
5. **Audio/Dialogue** (optional) -- spoken lines, sound effects, ambient sound

### The Six-Layer Framework (Cross-Platform)

A more granular version that works across all models:

1. **Subject & Action** -- who/what + what they're doing + emotional state
2. **Shot Type & Framing** -- wide, medium, close-up, angle
3. **Camera Movement** -- tracking, pan, dolly, static, handheld
4. **Lighting & Atmosphere** -- light source, quality, mood, color temperature
5. **Technical Specs** -- lens choice, depth of field, film stock/grade
6. **Duration & Pacing** -- slow motion, time-lapse, beat timing

### Prompt Order (Runway-Specific)
Runway Gen-4 responds best when you lead with subject movement, follow with camera motion, then add visual context/style last.

### Structured Fields Template (Advanced)

For complex scenes, use a structured fields approach:

```
Scene: [location, time, atmosphere]
Visual Action: [what happens, in beats]
Camera: [shot type, movement, lens]
Lighting: [key source, quality, color temperature]
Dialogue: [Character says: "line"]
SFX: [timed sound effects]
Ambience: [background soundscape, 2-3 specific cues]
Music: [mood/role, not rhythmic unless needed]
Style: [artistic treatment, color grade, film reference]
```

---

## 3. Camera & Cinematography Language

These terms are directly interpreted by all major video models. Using them produces dramatically better results than casual descriptions.

### Shot Types
| Term | Effect |
|------|--------|
| Extreme close-up (ECU) | Fills frame with small detail (eyes, hands, texture) |
| Close-up (CU) | Face or single object, intimate |
| Medium close-up (MCU) | Head and shoulders |
| Medium shot (MS) | Waist up, conversational |
| Medium wide / cowboy shot | Knees up |
| Full shot | Entire body in frame |
| Wide / establishing shot | Full environment, context |
| Extreme wide shot | Vast landscape, subject small |

### Camera Angles
| Term | Effect |
|------|--------|
| Eye-level | Natural, neutral |
| Low-angle | Power, dominance, heroic |
| High-angle | Vulnerability, overview |
| Bird's-eye view | Directly above, map-like |
| Worm's-eye view | Extreme low, looking up |
| Dutch / canted angle | Unease, disorientation |
| Over-the-shoulder (OTS) | Conversation, connection |
| POV shot | First-person perspective |

### Camera Movements
| Term | Description | Mood |
|------|-------------|------|
| Static / fixed | No movement | Stability, observation |
| Pan (left/right) | Horizontal rotation on axis | Reveal, survey |
| Tilt (up/down) | Vertical rotation on axis | Scale, reveal |
| Dolly (in/out) | Camera moves toward/away from subject | Intimacy / retreat |
| Truck (left/right) | Camera moves laterally | Parallel motion |
| Pedestal (up/down) | Camera moves vertically | Elevation change |
| Crane shot | Sweeping vertical + horizontal | Epic, establishing |
| Tracking shot | Camera follows subject | Connection, journey |
| Orbit / arc shot | Camera circles subject | Dramatic reveal |
| Handheld / shaky cam | Unstable, naturalistic | Documentary, urgency |
| Whip pan | Very fast horizontal pan | Transition, energy |
| Zoom (in/out) | Lens focal length change | Emphasis, surprise |
| Aerial / drone | Overhead, sweeping | Scale, geography |
| Rack focus | Shift focus between planes | Redirect attention |
| Dolly zoom / vertigo | Dolly + opposing zoom | Disorientation, dread |

**Speed note**: Slow, deliberate camera movements produce the most cinematic results. Very fast moves (rapid pans, spins) tend to break output across all models.

**Pro tip (Runway)**: If you need "fast" energy, shrink the focal distance in your prompt ("tight medium shot") so the motion feels bigger without actually moving faster.

### Lens Language
| Term | Effect |
|------|--------|
| Wide-angle / 24mm | Broader field of view, exaggerated perspective |
| 35mm | Natural wide, documentary feel |
| 50mm | Standard human perspective |
| 85mm | Portrait compression, shallow DOF |
| Telephoto / 135mm+ | Compressed perspective, subject isolation |
| Macro | Extreme detail, tiny subjects |
| Fisheye | Ultra-wide with barrel distortion |
| Anamorphic | Widescreen with characteristic oval bokeh and flares |

### Optical Effects
- **Shallow depth of field**: focused subject, blurred background (bokeh)
- **Deep depth of field**: sharp foreground-to-background
- **Lens flare**: bright light streaks and starbursts
- **Film grain**: textured, analog feel
- **Bokeh**: out-of-focus light circles

---

## 4. Motion Description

### Subject Motion
Use simple, direct verbs: "runs," "turns," "lifts," "pauses." Avoid complex descriptive phrases. Runway specifically recommends referring to characters with general terms ("the subject," "she," "he") to keep the model focused on smooth motion rather than reinterpreting subject details.

### Describe Actions in Beats
Vague: "Actor walks across the room."
Precise: "Actor takes four steps to the window, pauses, and pulls the curtain in the final second."

Beats give the model timing anchors. Use temporal markers: "first," "then," "finally," "in the last moment."

### Sequence Prompting ("This Then That")
For Veo, structure emotional/action progressions:
- Confusion leads to confidence leads to accomplishment
- Hesitation leads to breath leads to resolve
- Wide shot narrows to medium shot then lands on close-up

### Transformation & Temporal Effects
- Slow-motion: "slow motion capture of..."
- Time-lapse: "time-lapse of flower blooming over hours"
- Evolution: "candle burning down," "dawn breaking across the valley"
- Rhythmic: "pulsating light," "rhythmic ocean waves"

### Subtle Motion (Often Overlooked)
- Breeze effects on hair/fabric
- Rustling leaves
- Gentle nods or micro-expressions
- Steam rising
- Flickering candlelight
- Dew drops forming

---

## 5. Lighting & Atmosphere

### Natural Light
| Term | Quality |
|------|---------|
| Golden hour | Warm, romantic, long shadows |
| Blue hour | Cool, mysterious twilight |
| Overcast | Soft, diffused, even |
| Harsh midday sun | High contrast, sharp shadows |
| Dappled forest light | Filtered through canopy |
| Moonlight | Cool, low-key, silvery |
| Pre-dawn | Soft, gradual, anticipatory |

### Artificial / Cinematic Light
| Term | Quality |
|------|---------|
| Rembrandt lighting | Classic portrait, triangle under eye |
| Film noir | High contrast, dramatic shadows |
| High-key lighting | Bright, even, minimal shadows |
| Low-key lighting | Dark, moody, dramatic |
| Rim lighting / backlighting | Silhouette edges, separation from background |
| Side lighting | Dramatic texture and depth |
| Volumetric lighting | Visible light rays through atmosphere |
| Neon lighting | Colorful, urban, cyberpunk |
| Candlelight / fireplace glow | Warm, intimate, flickering |
| Fluorescent | Flat, institutional |

### Atmosphere & Color
**Color palettes** (name 3-5 core colors as "palette anchors" for consistency):
- Monochromatic
- Warm autumnal (amber, rust, gold)
- Cool futuristic (steel blue, silver, white)
- Muted earth tones
- Vibrant tropical
- Desaturated / bleached

**Atmospheric effects**: fog, mist, haze, falling snow, rain, dust particles, heat haze, glowing particles, smoke

**Textural qualities**: rough stone, polished chrome, soft velvet, weathered wood, dewdrops on glass

---

## 6. Style & Artistic Treatment

### Photorealistic
- "Ultra-realistic rendering," "8K camera aesthetic"
- "Shot on Arri Alexa" or "shot on 35mm film"
- "Documentary style," "cinema verite"

### Cinematic References (Style Stacking)
Combine 2-3 film references for precise aesthetic control:
- "Blade Runner 2049 color grading with Seven atmosphere"
- "Wes Anderson symmetrical composition with warm pastel palette"
- "Emmanuel Lubezki natural lighting style"

### Animation Styles
- Japanese anime
- Pixar 3D rendering
- Disney hand-drawn
- Claymation / stop-motion
- Cel-shaded
- Watercolor animation
- Charcoal sketch style

### Art Movement References
- Impressionist (Monet, Renoir)
- Surrealist (Dali)
- Art Deco
- Bauhaus
- Post-impressionist (Van Gogh)
- Graphic novel / comic book

### Mood/Tone Keywords
| Mood | Keywords |
|------|----------|
| Happy / joyful | Bright, vibrant, cheerful, uplifting |
| Melancholy | Somber, muted, slow-paced, poignant |
| Suspenseful | Dark, shadowy, uneasy, thrilling |
| Peaceful | Calm, tranquil, gentle, meditative |
| Epic | Sweeping, majestic, awe-inspiring, grandiose |
| Futuristic | Sleek, metallic, neon, technological |
| Vintage | Sepia tone, grainy film, era-specific |
| Romantic | Soft focus, warm colors, intimate |
| Horror | Dark, unsettling, eerie, oppressive |

### Editing / Transition Terms (Advanced)
Match cut, jump cut, establishing shot sequence, montage, split diopter effect, cross-dissolve, hard cut, fade to black.

---

## 7. Audio Cues (Veo 3 / 3.1 Native Audio)

Veo 3+ generates native synchronized audio. This is a differentiating capability. Audio is controlled entirely through prompt text.

### Core Principle
Use separate sentences to describe audio. Do not mix audio description into visual description sentences. Treat audio as its own layer.

### Dialogue Prompting

**Format**: Use colon syntax before quoted dialogue -- this is critical for preventing unwanted subtitle generation.

```
A woman says: "We have to leave now."
```

NOT:
```
A woman says "We have to leave now."
```

**Character voice control**: Specify age range, emotional state, personality, and professional tone. The model does not have voice presets, but character description shapes the voice.

**Formula**: Character + Emotion + Tone + Context

```
A tired detective in his fifties says: "I've seen this before." His voice is gravelly and resigned.
```

**Length rule**: Keep dialogue to under ~7 words per line for clean lip-sync. The 8-second clip duration means about one natural sentence. Shorter lines fix lip-sync drift. Longer lines cause rushed speech or gibberish.

**Multi-character dialogue**: Use visual descriptors (clothing, position) to distinguish speakers.

```
The woman in the red jacket says: "Are you sure?" The tall man in the gray coat replies: "Absolutely."
```

### Sound Effects (SFX)

Describe sounds explicitly with short, descriptive cues anchored to visual action:

```
SFX: Thunder cracks in the distance as rain begins to fall.
SFX: A glass shatters on the tile floor.
SFX: Footsteps echo down the empty corridor.
```

**Placement rule**: SFX phrases should sit immediately next to the described visual action in the prompt. This temporal anchoring improves sync.

### Ambient Sound

Define the background soundscape with 2-3 specific environmental cues:

```
Ambient: The quiet hum of fluorescent lights and distant keyboard typing.
Ambient: Rain hiss on windows, transformer buzz, occasional car passing.
Ambient: Cafe HVAC hum, dishes clinking, muffled conversation.
```

**Reusable ambience blocks** -- maintain a small library:
- Office: "fluorescent hum, keyboard typing, distant phone ringing"
- Urban street: "traffic noise, distant sirens, pedestrian chatter"
- Forest: "birdsong, wind through leaves, creek babbling"
- Kitchen: "sizzling pan, exhaust fan, utensils clinking"
- Beach: "crashing waves, seagulls, wind"

### Music

Keep music as mood/texture, not rhythmic:
```
Music: A soft, melancholy piano melody plays in the background.
Music: Low, tension-building strings underscore the scene.
```

Music should be supportive, not dominant. Plan complex music/beats for post-production.

### Audio Quality Keywords
- "Crystal clear dialogue" -- for speech clarity
- "Professional audio mixing" -- for complex multi-element scenes
- "Balanced audio levels" -- when dialogue + SFX + ambience coexist
- "Studio-quality sound" -- general quality boost

### Audio Pitfalls
- If unwanted captions appear: add "no subtitles, no on-screen text" (reinforce if needed: "No subtitles. No subtitles! No on-screen text whatsoever")
- Reduce ambient complexity if dialogue or SFX gets masked
- After two iterations, audit: can you clearly hear each intended audio element without masking? If not, reduce concurrent elements
- Phantom sounds (audience laughter, random music): explicitly specify the environmental soundscape to prevent hallucinated audio additions

---

## 8. Style Consistency Across Multiple Clips

### The Core Problem
Each AI generation is independent -- no memory mechanism. Character identity, lighting, and style can drift between clips. Consistency requires deliberate strategy.

### Technique 1: Reference Image Anchoring
Upload 1-3 reference images per generation. The image acts as a visual anchor; the prompt guides action and camera. For Veo 3.1, use up to three reference images (character, object, or scene).

Build a multi-angle reference pack: front, 3/4 profile, and profile views of the same character under various lighting.

### Technique 2: Frame-to-Frame Chaining
Generate shot N to a clean last frame. Use that last frame as the reference image for shot N+1. This preserves motion vectors, subject orientation, and lighting continuity across cuts.

### Technique 3: Character Bible in Every Prompt
Repeat the exact same identity description across all prompts. Use identical phrases:
- Same wardrobe description word-for-word ("charcoal peacoat, silver-rimmed glasses")
- Same hair description ("auburn hair pulled back in a loose bun")
- Same distinguishing features ("scar above left eyebrow")

Never paraphrase between shots. "Brown trench coat" in one prompt and "coat" in the next causes drift.

### Technique 4: Lock Your Technical Parameters
Across all clips in a project, maintain:
- Same aspect ratio (16:9 or 9:16)
- Same resolution (720p for drafts, 1080p for final)
- Same camera language conventions
- Same color palette anchors (name 3-5 specific colors)
- Same lighting direction ("soft key from camera right")
- Same time-of-day language

### Technique 5: Palette Anchors
Name your palette explicitly and repeat across prompts:
```
Palette: amber, cream, walnut brown, deep olive
```

Changing palette mid-sequence is one of the most common sources of perceived discontinuity.

### Technique 6: Wardrobe & Props as Anchors
Simple silhouettes, solid colors, and notable but minimal anchors (red jacket, silver pendant, specific hat) are more consistent than busy patterns or reflective textures, which mutate frame to frame.

### Technique 7: Lighting Consistency
Maintain a single dominant light direction per scene. If the key light flips sides mid-sequence, identities wobble. Color temperature notes (warm tungsten vs. cool neon) shift skin tone and hair cues.

### Technique 8: Test Before Committing
For each shot type (close-up, medium, wide), test a 1-2 second snippet to confirm identity holds at that angle. If features drift, swap in the most similar reference angle and retest.

---

## 9. Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Vague prompts produce generic output | Use specific cinematography terms, not casual descriptions |
| Packing multiple actions into one shot | One camera move + one subject action per generation |
| Contradictory elements ("bright moonlit noon") | Review for internal logic before generating |
| Re-describing the input image (Runway) | Focus prompt on motion/action, not what's already visible |
| Abstract concepts ("show loneliness") | Translate to physical actions ("figure sits alone on bench, shoulders slumped") |
| Too-long prompts | Stay in the 150-300 character sweet spot |
| Negative phrasing in main prompt | Use dedicated negative prompt field; describe unwanted elements as nouns |
| Changing wardrobe/palette descriptions between shots | Use exact same phrases across all prompts in a project |
| Multiple concurrent audio elements masking each other | Reduce to 2-3 audio layers max per generation |
| Lip-sync drift on long dialogue | Shorten to under 7 words per spoken line |
| Fast camera movements breaking output | Slow down movements; use tight framing for perceived speed |
| Subtitle/text artifacts appearing | Add "no subtitles, no on-screen text" with reinforcement |
| Color/style inconsistency across clips | Lock palette anchors, lighting direction, and color temperature |
| Attempting timestamp-based staging | Not a guaranteed feature; use beat descriptions instead |

---

## 10. Prompt Templates

### Template A: Simple Shot (Veo / Any Model)

```
[Shot type + camera movement] of [subject with specific visual details] [doing action] in [setting with atmosphere]. [Lighting description]. [Style/lens/grade].
```

**Example**:
```
Slow tracking medium shot of a bearded fisherman in a yellow raincoat hauling nets on a misty dock at dawn. Soft diffused overcast light with cool blue tones. Shot on 35mm film, shallow depth of field.
```

### Template B: Full Scene with Audio (Veo 3.1)

```
Scene: [Location, time of day, weather/atmosphere]
Camera: [Shot type, movement, lens]
Lighting: [Key source, quality, color temperature]
Subject: [Detailed visual description -- wardrobe, hair, distinguishing features]
Action: [What happens, described in 2-3 beats]
Dialogue: [Character] says: "[line under 7 words]"
SFX: [Sound effect anchored to visual action]
Ambience: [2-3 specific environmental audio cues]
Style: [Artistic treatment, color grade]
Negative: [Elements to exclude -- subtitle, text, blur]
```

**Example**:
```
A medium shot in a dimly lit jazz club at night. The camera slowly dollies forward. Warm amber light from table candles with blue neon accent from a sign behind the bar. A woman in her forties with short silver hair and a black turtleneck sits at the bar, turns to camera. She says: "You're late." SFX: Ice clinks in a glass. Ambient: Muffled jazz trumpet, low conversation hum, glasses clinking. Cinematic, shallow depth of field, warm film grain. No subtitles, no on-screen text.
```

### Template C: Action/Dynamic Shot

```
[Dynamic camera movement] following [subject] as they [action verb] through [environment]. [Atmospheric detail]. [Speed/pacing note]. [Lens and style].
```

**Example**:
```
Handheld tracking shot following a parkour runner in a gray hoodie as he vaults over concrete barriers in an abandoned warehouse. Shafts of dusty light cut through broken skylights. Energetic pacing, medium speed. Wide-angle lens, desaturated cool tones, documentary style.
```

### Template D: Multi-Shot Consistency Block

Use this as a header for all prompts in a multi-clip project:

```
PROJECT CONSTANTS:
- Character: [exact description, repeated verbatim]
- Palette: [3-5 named colors]
- Lighting: [dominant direction and quality]
- Aspect ratio: [16:9 / 9:16]
- Resolution: [720p / 1080p]
- Style: [artistic treatment]
- Audio note: [ambient baseline if applicable]
- Negative: no subtitles, no on-screen text
```

Then each shot prompt references these constants and adds shot-specific camera, action, and dialogue.

### Template E: The Iteration Workflow

```
Pass 1: Generate shortest viable shot (4s) with core elements.
         Check: Is the main beat present? Is dialogue clean?

Pass 2: Adjust ONE variable (camera OR lighting OR action).
         Generate 2-3 variants. Pick best.

Pass 3: Extend duration to 6-8s if stable.
         Add secondary audio layers (SFX, ambience).
         Final quality check.
```

---

## 11. Model-Specific Notes

### Google Veo 3.1
- Duration: 4, 6, or 8 seconds. Resolution: 720p or 1080p. Aspect: 16:9 or 9:16.
- Up to 3 reference images per generation (character, object, scene).
- Native audio generation (dialogue, SFX, ambient, music).
- Colon syntax for dialogue prevents subtitle artifacts.
- Use "Highest Quality (Experimental Audio)" mode when speech is needed.
- veo-3.1 does not support referenceImages.style -- use veo-2.0-generate-exp for style images.
- Seed values (uint32) enable deterministic generation for iteration.

### Runway Gen-4
- Thrives on simplicity. Short, clear prompts.
- Input image establishes visual starting point; prompt should describe motion, not re-describe the image.
- Refer to characters as "the subject" or simple pronouns for smoother motion.
- No negative prompt support -- use only positive descriptions.
- Timestamp prompting available for rough action sequencing (not frame-precise).

### OpenAI Sora 2
- Creates entire scenes with multiple camera angles in single generation.
- Responds well to professional camera language and scene progression.
- One camera idea per shot -- either dolly-in or crane rise, not both.
- Palette anchors (3-5 colors) critical for multi-shot consistency.
- No formal negative prompt parameter; phrase exclusions inside prompt ("avoid Dutch angles; no on-screen text").
- Higher resolutions produce better motion consistency.
- Two 4-second clips stitched in post often outperform one 8-second generation.

### Pika 2.5
- Strong at stylized/animation-like aesthetics.
- Good for short clips with consistent character identity.
- Best for quick iteration on concept and mood.

---

## 12. Advanced Techniques

### The 5-10-1 Rule (Budget Optimization)
Generate 5 variations on a budget/fast model. Refine the best through 10 iterations. Produce 1 premium final render.

### Style Reference Stacking
Combine 2-3 film references for precise aesthetic control:
```
"Blade Runner 2049 color grading plus Heat camera movement using anamorphic lens and cinematic bokeh"
```

### Use Gemini to Expand Prompts
Google's own recommendation: use Gemini to expand a basic concept into a detailed prompt before submitting to Veo. Gemini can add cinematographic detail, suggest camera movements, and flesh out atmospheric descriptions.

### JSON-Structured Prompts (Veo API)
For programmatic generation, Veo supports JSON formatting that separates each prompt element into distinct key-value pairs. More consistent results for commercial projects requiring strict creative specifications.

### Physics-Aware Prompting
Veo excels at fluid dynamics. Use specific terminology:
- "Viscous honey dripping slowly off a spoon"
- "Raindrops hitting a puddle with concentric ripples"
- "Silk fabric caught in wind, billowing and folding"
- Material properties: fabric weight, metal reflectivity, glass transparency

### Cross-Cut Continuity Sound
Carry a signature sound across cuts for perceived continuity:
- Rain outdoors transitions to faint drip indoors
- Music from a radio continues muffled through a closing door
- Traffic noise fades as character enters building

---

## Quick Reference Card

```
BEFORE GENERATING:
1. What is the shot? (type, angle, framing)
2. How is it framed? (camera move, lens, DOF)
3. What is the visual style? (lighting, grade, atmosphere)
4. What happens? (one action, in beats)
5. What do we hear? (dialogue, SFX, ambient -- separate sentences)

CONSISTENCY CHECKLIST:
[ ] Same character description, word for word
[ ] Same palette anchors (3-5 colors named)
[ ] Same lighting direction and quality
[ ] Same aspect ratio and resolution
[ ] Same style/grade language
[ ] "No subtitles, no on-screen text" included
[ ] Reference image from previous shot's last frame

ITERATION RULE:
Change ONE variable at a time. Generate 2-3 variants per pass.
Use 4s duration for testing. Extend to 6-8s only when stable.
```
