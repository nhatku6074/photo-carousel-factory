# Production workflow

Use this reference for end-to-end carousel production, delivery, and retry decisions.

## 1. Define the brief

Required information:

- product name and reference images;
- target audience, market, and language;
- publishing platform;
- content angle or pain point;
- output location.

Useful optional information:

- character demographics and wardrobe;
- preferred settings and visual tone;
- number of sets and slides;
- preferred or prohibited image providers;
- budget and retry limit.

Ask only for missing information that would materially change the result. A safe default is a five-slide, 1080 × 1920 carousel in the user's language.

## 2. Build the narrative

Create a progression rather than five disconnected statements. The default sequence is:

1. a specific hook;
2. the most recognizable behavior or pain;
3. a less obvious supporting behavior or pain;
4. the cumulative consequence or final behavior;
5. a simple routine-oriented product reveal.

Keep captions concise enough to understand in one glance. Prefer two lines or fewer after wrapping.

## 3. Plan visual variation

Create a shot plan before image generation. Across a set, vary at least three of:

- location;
- camera distance;
- camera angle;
- time of day;
- activity;
- wardrobe;
- lighting.

Keep intentional continuity, such as the same fictional character, only when it supports the narrative. A hook may use a four-panel collage when it materially improves comprehension.

## 4. Generate base images

Generate one text-free vertical base image per slide. Keep caption-safe negative space near the configured caption position. Use product references on product slides and whenever the product is visible.

Record the provider, prompt, reference files, generation identifier, and retry count in project metadata when available.

## 5. Render captions

Place generated files in the project's `generated` directory and run:

```bash
python scripts/render_carousel.py path/to/project
```

The renderer reads `project.json`, cover-crops base images, fits captions inside safe areas, creates ordered PNG outputs, writes caption metrics, and creates a contact sheet.

## 6. Validate and inspect

Run:

```bash
python scripts/validate_carousel.py path/to/project
```

Automated validation does not replace visual review. Inspect:

- the full contact sheet for narrative rhythm and repetition;
- every product slide at full resolution;
- hands, fingers, faces, labels, logos, and product scale;
- caption placement over important visual cues.

## 7. Retry rules

Retry only the defective slide, not the entire set. Change the prompt to address the observed defect: label distortion, duplicated product, poor hand grip, missing caption space, anatomy, or scene mismatch.

Default stopping rule: two failed generations for the same slide. After that, report the defect and the best available artifact instead of spending indefinitely. Honor a user's explicit retry or budget policy when provided.

## 8. Deliver

Deliver a folder per set containing numbered PNG files in upload order. Include the contact sheet and QA report beside, not inside, the upload folder unless the user requests otherwise. State the slide count, dimensions, and upload order.

