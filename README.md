# Saltwater Verdict — Tuesday 24 November 2026 in one image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dentybaiq/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dentybaiq/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

**Bounty:** [Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124) — $100 shared by the 50 highest-ranked entries. Entries close Wed 26 Nov 2026 07:00 WIB (2026-11-26T00:00:00Z).

## The image

One 1024×1024 front page, **"Saltwater Verdict"**, summing up Tuesday 24 November 2026:

- **3 drawn lead scenes** — tankers burning in the Strait of Hormuz, the Huawei verdict in a New York courtroom, and a Ukrainian drone strike on the Russian cargo ship Sparta II.
- **36 dated stories across 6 regions** — Middle East, Europe & Ukraine, Asia, Americas, Africa, Sport & the World — every story stamped with its UTC time (or "24 NOV" where the wire dated it to the day).
- **How-sure labels** — every story carries a confidence dot: ● confirmed by officials/courts, ● reported by wires, ● claimed by one side and not independently verified.
- **A UTC timeline** of the day's six turning points, a **pin map** of 14 places, and the day's **market closes** (KOSPI +6.3%, Nikkei +3.9%, Brent $86.7, gold $3,620).

Top stories of the day: four tankers hit mines in the Strait of Hormuz; Huawei found guilty of trade-secret theft and bank fraud (10 of 12 counts); Ukraine's drone strikes on Russian ships in the Gulf of Finland and off Libya; a Houthi drone hitting Riyadh's PIF tower; 25 hostages held in a Cartagena supermarket; the ICJ finding Myanmar guilty of genocide against the Rohingya.

## How it is built

`draw.py` (Python 3 + Pillow, written from scratch for this entry) draws the whole page deterministically — no network, no random data — and writes `entry.png`. `main.ts` (Node 22, stdlib only) validates the image (whole PNG, ≤ 1 MiB, exactly 1024×1024) and copies it to `/output/entry.png`.

```sh
python3 draw.py   # writes entry.png
node main.ts      # writes /output/entry.png
```

## Sources

Wire, court and official reports first published Tuesday 24 November 2026 (times UTC), cross-checked against the day's digests. Claims labelled "claimed" are single-source assertions that were not independently verified that day.
