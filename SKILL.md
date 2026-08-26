---
name: photo-carousel-factory
description: Plan and produce product-focused social photo carousels when a user needs multi-slide Photo Mode images, model-agnostic generation prompts, deterministic captions, contact sheets, or publish-ready numbered outputs.
---

# Photo Carousel Factory

Turn product references and a content angle into a coherent, publish-ready photo carousel. Default to five vertical slides: one hook, three connected points, and one product reveal.

## Route the work

1. Collect or infer the product, audience, market, language, platform, content angle, and output location. Preserve explicit user choices.
2. Inspect every product reference before prompting. Identify the details that must remain stable: shape, color, cap, label hierarchy, logo placement, and scale.
3. Choose a narrative structure and write one short idea per slide. Read [references/copy-frameworks.md](references/copy-frameworks.md) when selecting or adapting a framework.
4. Plan varied people, locations, time of day, wardrobe, and framing without changing product identity.
5. Generate text-free base images with the best available image tool. Read [references/prompt-guide.md](references/prompt-guide.md) before writing prompts or comparing providers.
6. Create a portable project configuration, then render captions and contact sheets with `scripts/render_carousel.py`. Read [references/project-schema.md](references/project-schema.md) when creating or repairing the configuration.
7. Run `scripts/validate_carousel.py` and visually inspect the contact sheet plus every product-reveal slide.
8. Deliver numbered images in upload order, the contact sheet, configuration, and QA report. Read [references/workflow.md](references/workflow.md) for the complete operating procedure and retry rules.

## Invariants

- Generate base images without captions, watermarks, prices, invented badges, or extra brand claims.
- Add large captions deterministically after image generation; do not rely on an image model to spell marketing copy.
- Keep one message per slide and make the sequence understandable without audio.
- Default to 1080 × 1920, but honor the configured canvas and safe areas.
- Use fictional people unless the user provides an authorized identity reference.
- Vary scenes deliberately; do not create five near-identical portraits.
- Preserve product identity more strictly than character continuity.
- Do not claim success before the requested files exist and pass validation.

## Provider selection

Remain model-agnostic. Prefer, in order: product-reference fidelity, believable hands and anatomy, vertical composition control, cost, latency, and current availability. If no image tool is available, produce the complete plan, prompts, and project configuration, then clearly report that base-image generation remains pending.

Do not install providers, expose credentials, make paid calls, or publish files externally unless the user has authorized those actions. Follow any provider-specific confirmation or cost rules. After two failed generations for the same slide, stop retrying automatically and report the observable defect unless the user has requested persistent retries.

## Completion standard

Before handoff, confirm:

- every configured slide exists and is non-empty;
- output filenames are unique and ordered;
- all images match the declared dimensions;
- captions stay inside safe areas and remain readable at contact-sheet size;
- the product-reveal slide is present when required;
- the product label and shape are acceptably faithful at full resolution;
- delivery contains the numbered slides and a QA summary.
