# Provider-neutral prompt guide

Use this reference to write prompts for any capable image generator. Do not include provider-specific API syntax in reusable prompts.

## Base prompt components

Describe:

1. output format and composition;
2. fictional character and activity;
3. environment and time of day;
4. storytelling cue for the slide's idea;
5. camera and lighting style;
6. caption-safe region;
7. anatomy and product constraints;
8. exclusions.

Template:

```text
Create a photorealistic vertical 9:16 social Photo Mode base image. [Fictional person] is [specific activity] in [specific setting and time]. The scene must clearly communicate [single slide idea]. Use candid smartphone-style photography with [lighting and framing]. Leave a broad low-detail caption-safe area around [position]. Keep hands, face, and proportions realistic. Do not add captions, watermarks, prices, invented badges, or readable unrelated brands.
```

## Product slide additions

When product references are available, add:

```text
Use the product reference faithfully. Preserve the package shape, material, cap, dominant colors, label hierarchy, logo placement, and realistic scale. Show exactly one product unless the brief asks for more. Keep the label facing the camera and the hand grip anatomically credible. Do not invent claims or extra label text.
```

For difficult labels, prefer a clean product cutout composited into a generated scene or a provider with strong reference fidelity. Do not hide identity-critical defects under captions.

## Character continuity

Continuity is useful when a single character carries the narrative. Repeat stable attributes such as approximate age, hair, wardrobe palette, and environment style, but avoid claiming exact identity consistency unless the provider supports it.

## Scene variation

Avoid changing only the background. Change activity, camera distance, light direction, prop layout, and emotional beat. A five-slide set should not look like five frames from one static portrait session.

## Caption-safe composition

Specify the location and character of the negative space: bright wall, dark cabinet, blurred window, clean tabletop, or low-detail shadow band. Do not ask for an empty rectangle unless that graphic treatment is intentional.

## Provider comparison

Evaluate providers using the same prompt and references. Compare:

- product-label fidelity;
- hand and finger anatomy;
- composition control;
- consistency across slides;
- latency and cost.

Choose based on the current project's highest-risk slide, usually the product reveal, not on a generic model ranking.

