---
title: "BidMirror: The $0 local AI that checks what contractor quotes don't say"
published: false
tags: devchallenge,hf26challenge,opensource,ai
---

*Submission for [Hacktoberfest Open-Source AI Challenge — Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12). AI-assisted project; technical implementation and tests completed using ChatGPT. The data in this post is fictional demo material.*

## What I Built

**BidMirror** is a lightweight local-first tool for anyone comparing two contractor quotes — especially a solo property manager or home-renovation adviser.

You already know the problem: Contractor A quotes $2,850; Contractor B quotes $2,920. Which is cheaper? You cannot tell from the totals. Perhaps A includes debris removal, while B excludes it. One has a workmanship warranty, while the other never mentions one. In a busy week, those gaps get missed.

BidMirror takes two pasted text estimates, uses a **local open-weight AI model** to extract line items and exact supporting language, and generates:

- A side-by-side scope comparison;
- A list of items found in one quote but not matched in the other;
- Clearly stated exclusions, rather than treating absence as proof of exclusion;
- Source-backed questions to ask before accepting the bid.

The differentiator is deliberate restraint. If the model cannot point to the exact words in a quote, the program discards the claimed fact. And when two quotes use different currencies, it refuses to calculate misleading differences.

**Who might pay?** A solo renovation consultant or small property manager who compares bids routinely. A $5/month local-only companion or a $3 report are *pricing experiments*, not existing sales. No customers or revenue have been claimed for this prototype.

## Demo

**[ADD A SCREENSHOT/SHORT VIDEO CAPTURED WHEN RUNNING THE SAMPLE DEMO. Clearly label it as fixture-based, not live AI inference.]**

The app includes a one-click sample based on two **fictional** kitchen renovation quotes. For example:

- Northline lists tile removal **including disposal**. BrightEdge lists tile removal but explicitly says disposal is not included.
- Northline provides a **12-month workmanship warranty**. BrightEdge gives no warranty information; BidMirror correctly asks for clarification rather than calling the warranty "excluded."
- Both list installation and cleanup, but with different pricing and delivery timelines.

The sample mode uses a documented **precomputed fixture**, not a claim of live model execution. Real quote analysis uses a running local Ollama model.

Try the sample:

```bash
python3 app.py
# visit http://127.0.0.1:8765 and click "Load verified sample demo"
```

## Code

**[INSERT PUBLIC GITHUB REPOSITORY LINK HERE]**

To analyze your own text with the open-weight model:

```bash
ollama pull qwen2.5:1.5b
ollama serve
python3 app.py
```

Open `http://127.0.0.1:8765`, paste two text quotes, and click "Compare with local AI." The source includes unit tests and fully synthetic sample quotes. Requires Python 3.10+ and Ollama for actual model inference. The demo requires neither a GPU nor an API key.

## How I Built It

BidMirror intentionally uses minimal moving parts:

1. **Qwen2.5 1.5B through Ollama** (open-weight model and open-source local runner) extracts irregular contractor terminology into bounded JSON.
2. **Evidence validation** discards extracted line items or exclusions without direct verbatim source support.
3. **Deterministic Python comparison** matches similar descriptions and flags mismatches. It only calculates price differences when two amounts are explicitly present and the quote currencies match.
4. **A dependency-free browser UI** runs from a Python standard-library HTTP server bound to `127.0.0.1` and calls only the local service.

I wrote and ran five deterministic tests covering evidence filtering, matched items, currency mismatches, warranty-mention uncertainty, and the central "missing does not mean excluded" rule. The fixture HTTP route has also been tested locally. **Live inference with an installed Ollama model has not been verified in my build environment; this is an explicit limitation, not a silent success claim.**

### One important design choice

Most quote comparison demos say "Quote B doesn't include X" when they really mean "X wasn't detected." That is risky. BidMirror says "I couldn't match X in Quote B — ask the vendor if it's included." A small change in wording can prevent a big incorrect assumption.

## Why Does Open Innovation Matter?

Home-improvement quotes often contain addresses, customer details and budgets. A hosted AI tool usually requires sending that text off the device. With an open-weight model running in Ollama, users can analyze estimates locally, swap models without rewriting the whole app, and run the tool after the initial model download without an internet connection.

Local inference matters to the *business model* too. There is no per-document cloud inference fee to erode a small monthly subscription. A property manager can work in a basement or an offline office. The tradeoff is that a tiny local model may miss or misread details, so we rely on source evidence and human review instead of automatic approval.

## My Agent Session

I used ChatGPT to help plan, implement and test the prototype. There is no public agent-session recording for this build. The complete source, samples and test suite are in the repository.

## Prize Categories

**Overall prize only.** I did not integrate partner technology and am not claiming eligibility for partner-specific awards.

---

### What I would improve next

Real support for PDFs and scanned estimates, better quote-line matching with local embeddings, unit/quantity normalization, and optional export to a client-facing PDF. First, though, I would ask a renovation adviser to test the prototype against real quotes and validate whether the questions are useful enough to pay for.
