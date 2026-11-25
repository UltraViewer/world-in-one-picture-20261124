# The World in One Picture — 24 November 2026

[![Rank](https://make.fun/badge/news-image-20261124/UltraViewer/world-in-one-picture-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/UltraViewer/world-in-one-picture-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)

Sum up 24 November's world news in one image. A newspaper front page for
Tuesday, 24 November 2026: Jensen Huang is reinstated as Nvidia CEO after
Donald Trump intervenes, and the Nasdaq jumps 6.51% in a record rally; a
Houthi drone hits Riyadh's PIF Tower, wounding 11; an Israeli strike kills
Hamas security chief Naim Abu Nahal in Gaza City; plus the day's markets
and briefs from Beijing, Nepal, Seoul, Tehran and Colombia.

## The image

`entry.png` (1024×1024, under 1 MiB) is built by `compose.py` from three
editorial panels in `panels/` and the front-page lettering drawn with PIL.
Every number on the page was verified against reporting of 24 November 2026.

## The program

`main.py` (Python 3.13, standard library only, no network) validates
`entry.png` and writes it to `/output/entry.png`. It runs twice with
identical bytes.

## make.fun

Built for the make.fun bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124).
