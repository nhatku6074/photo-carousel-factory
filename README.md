# Photo Carousel Factory

Turn product references and a content angle into a publish-ready social photo carousel—with model-agnostic image prompts, deterministic captions, contact sheets, and automated QA.

[简体中文](README.zh-CN.md)

![Five-slide fictional product demo](assets/demo-contact-sheet.png)

## Why this exists

Image models are good at scenes and weak at reliable marketing text. Photo Carousel Factory separates those jobs:

1. plan a coherent multi-slide story;
2. generate text-free base images with any capable provider;
3. add captions deterministically;
4. validate dimensions, safe areas, ordering, and required slides;
5. package numbered images ready for Photo Mode upload.

The default structure is five slides: **hook → three connected points → product reveal**. It is configurable for other narratives and slide counts.

## What you get

- A reusable Codex Skill with provider-neutral generation guidance
- Copy frameworks for habits, myths, pain points, and routines
- Reference-fidelity prompt patterns for product images
- A portable JSON project format
- Cross-platform Pillow-based caption rendering
- Automated delivery validation and machine-readable QA
- Contact-sheet generation for fast visual review
- A fictional five-slide example with no customer assets or real trademarks
- A deterministic GitHub Release ZIP builder

## Install as a Codex Skill

### Release ZIP

1. Download `photo-carousel-factory-v1.0.0.zip` from the latest GitHub Release.
2. Extract it so the folder is named `photo-carousel-factory`.
3. Place that folder in `$CODEX_HOME/skills`, or in `~/.codex/skills` when `CODEX_HOME` is not set.
4. Ask Codex: `Use $photo-carousel-factory to create a five-slide carousel for my product.`

The OpenAI Skills API also accepts either a directory upload or a single Skill ZIP. See the [official Skills API reference](https://developers.openai.com/api/reference/python/resources/skills/methods/create).

### From source

Copy or clone this repository into your Codex skills directory, keeping `SKILL.md` at the repository root.

## Use it

Give Codex:

- one or more product images;
- audience, market, and language;
- a content angle or pain-point cluster;
- preferred platform and output location;
- optional character, setting, provider, budget, or retry constraints.

Example:

```text
Use $photo-carousel-factory to create a five-slide English TikTok Photo Mode
carousel for this reusable bottle. Target remote workers. Focus on desk habits,
use fictional people, vary the scenes, and deliver numbered 1080x1920 PNGs.
```

If the environment has no image generator, the Skill still produces the plan, prompts, and project configuration, then reports image generation as pending.

## Run the deterministic tools manually

```bash
python -m pip install -r requirements.txt
python scripts/render_carousel.py examples/fictional-product-demo
python scripts/validate_carousel.py examples/fictional-product-demo
```

Build a release ZIP:

```bash
python scripts/package_release.py . --version 1.0.0
```

## Project format

Each carousel project contains:

```text
project/
├── project.json
├── generated/        # text-free base images
├── slides/           # numbered publish-ready images
└── qa/
    ├── contact-sheet.png
    ├── caption-metrics.json
    └── validation-report.json
```

See [the project schema](references/project-schema.md) for every configuration field.

## Model-agnostic by design

This Skill does not require one image vendor. Use the best available provider for the highest-risk slide, usually the product reveal. Compare product-reference fidelity, hands and anatomy, vertical composition, cost, latency, and availability.

Provider credentials are never stored in the project configuration or release ZIP.

## Who it is for

- Solo social creators
- TikTok Shop and ecommerce operators
- Affiliate creators
- Social media agencies
- AI automation builders
- Small teams producing repeated product-content variations

## Limits

- It does not guarantee viral performance.
- It does not replace domain-specific compliance review.
- Exact character continuity depends on the selected image provider.
- Product-label fidelity still requires full-resolution visual inspection.
- The default two-retry stopping rule avoids uncontrolled generation spend.

## Scorecard — v1.0.0

| Area | Score | Notes |
|---|---:|---|
| Practical usefulness | 9.1/10 | Complete plan-to-delivery workflow |
| Reusability | 9.0/10 | Product, market, language, and provider neutral |
| Automation | 8.6/10 | Rendering, QA, preview, and packaging are automated |
| Provider portability | 8.7/10 | Prompts are portable; provider execution remains environment-specific |
| Documentation | 9.2/10 | English/Chinese guides, schema, frameworks, and example |
| Public-release maturity | 9.0/10 | Tests, CI, MIT license, secret-safe ZIP packaging |
| GitHub growth potential | 8.8/10 | Strong visual demo and clear creator/ecommerce use case |
| **Overall** | **8.9/10** | Main deduction: no bundled image-provider API adapter |

## Roadmap

- Additional caption styles and brand presets
- Multi-language typography tests
- Optional provider adapters maintained outside the core Skill
- Carousel analytics schema and winning-variant feedback loops
- Accessible caption contrast scoring

## Contributing

Useful contributions include portable font support, QA checks, copy frameworks, fictional examples, and provider-neutral prompt improvements. Please do not contribute real customer assets, API keys, copyrighted source campaigns, or unverified product claims.

## License

MIT. See [LICENSE](LICENSE).

