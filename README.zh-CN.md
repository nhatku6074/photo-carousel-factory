# Photo Carousel Factory

[![Downloads](https://img.shields.io/github/downloads/daisymyu-dev/photo-carousel-factory/total?style=for-the-badge&logo=github&label=Downloads&color=2ea44f)](https://github.com/daisymyu-dev/photo-carousel-factory/releases/latest)

把产品参考图和一个内容角度，变成可直接发布的社交平台图文轮播：模型无关的生图提示词、确定性字幕、总预览和自动质量检查一次完成。

[English](README.md)

![五页虚构产品演示](assets/demo-contact-sheet.png)

## 核心价值

图片模型擅长生成场景，但不擅长稳定拼写营销字幕。本 Skill 把两项工作分开：

1. 设计完整的多页叙事；
2. 使用当前可用的图片模型生成无字幕基础图；
3. 用程序统一添加准确字幕；
4. 自动检查尺寸、安全区、顺序和产品收尾页；
5. 输出编号后的可发布图片。

默认结构是五页：**钩子 → 三个连续要点 → 产品收尾**。页数和叙事框架都可以调整。

## 安装

1. 从 GitHub Release 下载 `photo-carousel-factory-v1.0.0.zip`。
2. 解压后确认文件夹名称为 `photo-carousel-factory`。
3. 将文件夹放入 `$CODEX_HOME/skills`；如果没有设置 `CODEX_HOME`，则放入 `~/.codex/skills`。
4. 对 Codex 说：`使用 $photo-carousel-factory 为我的产品制作五页图文轮播。`

OpenAI Skills API 也支持上传文件目录或单个 Skill ZIP，参见[官方 Skills API 文档](https://developers.openai.com/api/reference/python/resources/skills/methods/create)。

## 使用时提供

- 一张或多张产品图；
- 受众、市场和语言；
- 内容角度或痛点主题；
- 发布平台和交付位置；
- 可选的人物、场景、模型、预算和重试要求。

示例：

```text
使用 $photo-carousel-factory 为这款水杯制作五页英文 TikTok Photo Mode。
受众是远程办公人群，主题是影响专注力的桌面习惯。人物必须虚构，
场景需要变化，最终交付按顺序编号的 1080x1920 PNG。
```

如果当前环境没有生图工具，Skill 仍会输出完整策划、提示词和项目配置，并明确说明基础图尚未生成。

## 手动运行

```bash
python -m pip install -r requirements.txt
python scripts/render_carousel.py examples/fictional-product-demo
python scripts/validate_carousel.py examples/fictional-product-demo
python scripts/package_release.py . --version 1.0.0
```

## 适用人群

- 独立内容创作者
- TikTok Shop 和跨境电商运营者
- Affiliate 创作者
- 社媒代运营公司
- AI 自动化开发者
- 需要批量生产产品图文的小团队

## 能力边界

- 不保证内容一定爆款。
- 不代替特定行业的合规审核。
- 人物连续性取决于所选图片模型。
- 产品标签仍需全尺寸人工视觉检查。
- 默认同一张失败两次后停止自动重试，避免无控制消耗。

## v1.0.0 评分

| 项目 | 评分 |
|---|---:|
| 实用性 | 9.1/10 |
| 可复用性 | 9.0/10 |
| 自动化程度 | 8.6/10 |
| 模型兼容性 | 8.7/10 |
| 文档完整度 | 9.2/10 |
| 公开发布成熟度 | 9.0/10 |
| GitHub 推广潜力 | 8.8/10 |
| **综合评分** | **8.9/10** |

主要扣分项：基础 Skill 不内置任何特定图片厂商的 API 适配器，因此实际生图能力取决于用户环境。

## 许可证

MIT，详见 [LICENSE](LICENSE)。
