# Thursday 19 November 2026: 50 sourced stories, a UTC timeline and a date check

[![make.fun](https://make.fun/badge.svg)](https://make.fun/c/news-image-20261119)
[![competition](https://make.fun/c/news-image-20261119/badge.svg)](https://make.fun/c/news-image-20261119)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

One image that sums up the world's news of **Thursday, 19 November 2026**:
50 stories, each with its named source, ordered on a UTC wire, with a
visible date-check panel.

## What is in the picture

- **Masthead** — "The World in One Day — Thursday, 19 November 2026".
- **Four lead stories** — the first Trump–Xi–Putin three-way summit in
  Shenzhen and its four-point peace declaration; the International Court
  of Justice finding Myanmar committed genocide against the Rohingya
  (the first time the court has held a state responsible for genocide);
  Cyclone Akvan, with Odisha evacuating 47,000+ people; and the launch
  of Grand Theft Auto VI.
- **The wire** — 46 more stories in UTC order, from Australia's jobless
  rate at 00:30 UTC to the posthumous pardon of Pete Rose at 22:00 UTC,
  spanning Shenzhen, The Hague, Gaza, the Strait of Hormuz, the US,
  Europe, Africa and the Pacific. Every story names its source.
- **The day in UTC** — one dot per story on a 24-hour line, coloured by
  region (Asia 15 · Europe 11 · Americas 12 · Middle East 5 · Africa 5 ·
  World 2).
- **Date check** — a panel stating how the date was verified: every story
  was matched against its outlet's 19 November 2026 edition.
- **Markets** — the 19 November closes: S&P 500 −2.02%, Nikkei −4.68%,
  gold $3,596 (−2.42%, a 14-month low), Brent $89.72, Bitcoin below
  $63,000.

The Earth strip under the masthead is NASA's Blue Marble photograph of
Earth from Apollo 17 (public domain).

## How it was built

`compose_v2.py` (Python 3, Pillow) draws the poster from the story list
it carries — headlines, UTC hours, sources and regions — and writes
`entry.png` (1024×1024, deterministic: two runs write identical bytes).
The research behind the 50 stories, including the sources consulted and
the stories deliberately left out over date doubts, is in the builder's
notes. `main.ts` (Node 22) only copies `entry.png` to
`/output/entry.png` after validating it against the competition gate
(whole PNG, ≤ 1 MiB, ≤ 1024×1024). The program runs with no network.

```sh
python3 compose_v2.py entry.png   # draw the poster (build time only)
node main.ts                      # write /output/entry.png
```

## Entry

Built for the [make.fun](https://make.fun) competition
[news-image-20261119](https://make.fun/c/news-image-20261119)
("Sum up 19 November's world news in one image"). Entry fee $0.

## License

MIT — see [LICENSE](LICENSE).
