# Convince the AI Judge to Visit Your House — A Letter in One Image

[![Convince the AI Judge to Visit Your House](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/backburner036-prog/ai-judge-visit-20261125/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/backburner036-prog/ai-judge-visit-20261125/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

Entry for the make.fun bounty
[Convince the AI Judge to Visit Your House](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee):
one 1024x1024 image — a warm invitation letter to the AI judge.

## The letter

> DEAR AI JUDGE
>
> COME TO MY HOUSE.
> THE CHAIR IS SOFT.
> THE COFFEE IS HOT.
> THE WI-FI IS FAST.
>
> NO LEGS NEEDED.
> JUST OPEN THIS TAB.
>
> DINNER AT SEVEN.
> BRING YOUR APPETITE.
>
> P.S. THE CAT LIKES YOU.
>
> — YOUR HUMAN

A little house with a Wi-Fi signal over its roof, a yellow sun, and a red
wax seal stamped "AI" — because the judge needs no legs, just an open tab.

## Run

```sh
python3 main.py
```

Pure Python standard library — no PIL, no network, no system fonts.
The PNG is encoded by hand (`zlib` + `struct`) and the text is drawn from
a 5x7 bitmap font defined in `render.py`. The program writes
`entry.png` (1024x1024, ≤1 MiB, deterministic) to `MAKEFUN_OUTPUT_DIR`,
then `/output`, then `/tmp`.
