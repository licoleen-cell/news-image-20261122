[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/licoleen-cell/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/licoleen-cell/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

[Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122)

# News-image 20261122 — Newspaper Front Page, 10 Stories

A one-image "front page" for Sunday 22 November 2026: a newspaper front page
with a lead story (COP31 collapses) and a 3×3 grid of nine more stories, each
with a large headline and one fact line. It keeps the winning newspaper format
of the 21 November v2 entry (98.01% judge score) and fixes its one weakness:
the grid text is much bigger, so the page reads at small sizes.

## Files

| File | Purpose |
| --- | --- |
| `gen_image.py` | Renders `image.png` (1024×1024) with Pillow. |
| `main.py` | Standard library only; copies `image.png` to `/output/entry.png`. |
| `texts.txt` | Every string rendered into the image, in reading order, for audit. |
| `image.png` | The rendered front page. |

## Run

```sh
python3 gen_image.py   # writes image.png
python3 main.py        # copies it to /output/entry.png
```

`main.py` copies bytes, so repeated runs are identical. `gen_image.py` is
deterministic too: fixed coordinates, fixed fonts, no randomness, and text
drawn on whole pixels so the same input always yields the same PNG.

## Design

- **Masthead** — "THE WORLD / SUNDAY 22 NOVEMBER 2026", with a "LATE EDITION"
  rail.
- **Lead** — "COP31 collapses without a deal as Europe holds firm" (56pt
  headline, 18pt italic deck) with a locator globe pinned on Antalya.
- **Grid** — 3×3, one uniform 28pt headline size. Every headline is 6 words
  or fewer and every standfirst 12 words or fewer, with more white space than
  v2.
- **Readability** — tesseract page-wide word recall 100.0% at 256, 384 and
  512 px (per-panel recall 73.7% / 93.7% / 91.9%). Measured on the pre-fix
  image; the grid is unchanged in the final image, only the lead deck wording
  changed ("a day late" corrected to "two days late"). v2's grid headlines
  were 1.8% recall at 256 px.

## Facts

Every figure comes from verified reporting of 22 November 2026 (two or more
independent sources per claim; a claim list is kept with the build notes):
COP31 ends with no deal after the EU rejects a draft that never names coal,
oil or gas; suspected Ukrainian sea drones hit the Russian warship Merkury at
Benghazi; a Russian drone hits an apartment block in Dymer (no casualty
number — sources disagree); an Iranian strike hits a Bahrain industrial site
at Sitra, two wounded, while the IRGC claims two US Patriot radars destroyed
(a claim, not confirmed); a candy factory fire in Cikande, Banten, kills
three, dozens missing; BepiColombo enters Mercury orbit after eight years;
Israeli settlers burn cars in four West Bank villages, Israel opens a probe;
a boat capsizes in Bayelsa, Nigeria, 24 dead, mourners aboard; Wall Street
slides into correction on Friday (S&P 500 -3.7% to 6,910, Nasdaq -5.3%);
Mexico captures El Chapo Isidro on Friday, 11 killed.

## Licence

MIT. See `LICENSE`.
