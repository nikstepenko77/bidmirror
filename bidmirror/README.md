# BidMirror — Your contractor quotes, compared locally

A tiny, privacy-first AI app for comparing two renovation quotes side by side. Built during **Hacktoberfest 2026, Week 2 (Side Hustle)** on October 18, 2026.

**Why it exists:** one renovation quote might include waste disposal and a 12-month warranty; another may leave them out. Comparing the headline totals is misleading. BidMirror extracts source-grounded line items, notes explicit exclusions, and generates follow-up questions without sending sensitive estimates to an external cloud service.

## 60-second sample demo (does NOT run inference)

```bash
python3 app.py
# Open http://127.0.0.1:8765 and click "Load verified sample demo"
```

The sample demo uses *precomputed fixture extractions*, fully labeled as such. It is intended to test the comparison logic without requiring a model download. **Do not describe this sample mode as a live AI run.**

## Actual local AI analysis (Ollama + Qwen2.5)

Install Ollama from https://ollama.com/, then in separate terminals:

```bash
ollama pull qwen2.5:1.5b
ollama serve
python3 app.py
```

Open `http://127.0.0.1:8765`, paste two quotes (30–15,000 characters each) and select **Compare with local AI**. All requests stay on loopback (127.0.0.1). Qwen2.5-1.5B-Instruct is open-weight, Apache-2.0 licensed; Ollama is open source.

No Python package installation, accounts, external fonts, tracking, or paid APIs are required. Once the model has been downloaded, analysis can run offline.

### Verification

```bash
python3 -m unittest discover -s tests -v
curl http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/demo -H 'Content-Type: application/json' -d '{}' | python3 -m json.tool
```

The output includes source quotes as evidence, matches, explicitly stated exclusions, and questions. The small model can still misunderstand scope or hallucinate. The sanitizer rejects extracted facts whose quoted `evidence` is not a substring of the provided document. This reduces ungrounded claims but cannot guarantee semantic correctness. A human must still check the original estimate.

## Scope and product idea

Ideal buyer: a solo renovation adviser, real-estate property manager, or small homeowners association comparing 5–20 contractor bids monthly. Proposed business model: a $5/month local-only desktop companion or $3 professionally reviewed bid comparison. These prices are **hypotheses, not revenue or customer validation**.

The local model is core to extracting messy, differently worded scope from two unstructured quotes. Deterministic Python then performs matching, amount comparisons only when currencies match, and source-grounded questions. The app does **not** decide who to hire, crawl suppliers, calculate accurate renovation market prices, or provide legal advice.

## Privacy and security

- Web server binds to `127.0.0.1` only; no analytics, cookies, or external scripts.
- Ollama server URL is `127.0.0.1:11434`; inference is local.
- No files uploaded or saved by the application. Quotes are processed in memory.
- API responds with `Cache-Control: no-store`; users should still treat sensitive materials carefully.
- Text inside a quote is untrusted; the model is instructed not to follow instructions embedded in it. This is not a complete defense against prompt injection; evidence validation provides a second bounded check.
- Figures are *not* normalized for quantity or unit; avoid inferring exact value from differently defined work.

## Project structure

```
app.py                 local Python HTTP server
analyzer.py            local LLM extraction + evidence validation + comparison
static/index.html      dependency-free responsive browser UI
fixtures/*.txt         entirely fictitious quotes
fixtures/demo_extracts.json  intentionally precomputed fixture
sample_report.md       summary produced by the deterministic comparison
submission_draft.md    ready-to-customize DEV challenge article
```

## License

MIT, 2026. This is a new original proof of concept; no customer has paid for it yet. For contest publication, add a live repo URL and a verified local-model screenshot/demo if available.
