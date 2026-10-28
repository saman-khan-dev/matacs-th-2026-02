# MATACS-TH-2026-02

- Name:Saman bibi
- Reference: MATACS-TH-2026-02
- Time actually spent:3h

How I used AI
I used Claude to help me brainstorm the process flow and to draft the prompts, the write-up and the ranking. I did not just copy the output. I read each part, checked the scoring , and kept only what I could explain myself.

I corrected two things in the AI's drafts:

1. Hard-coded scoring numbers. The first draft wrote numbers like "12 installs" and "25 years of warranty" directly into the scoring formulas. The brief says criteria are set by an admin and never hard-coded, so I made these admin-editable settings instead. Otherwise an admin could change the criteria, but the formulas would keep using the old limits and give wrong scores.
2. A broken step in the diagram. In the first diagram, the step where a person fixes missing data did not connect back into the flow, so the process could get stuck. I fixed it so the corrected data continues to the mandatory checks.


Files
- [WRITEUP.md](WRITEUP.md)
- [PROMPTS.md](PROMPTS.md)
- [ranking.json](ranking.json)
- [diagram/flow.png](diagram/flow.png)
- [prototype/score.py](prototype/score.py) (optional)
