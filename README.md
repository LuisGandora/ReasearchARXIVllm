# ReasearchARXIVllm

A lightweight AI agent that searches the ARXIV database for research papers and uses the Gemini API to automatically generate new research ideas from them.



## Scripts

### `gemini_bot.py` — The AI Model

This script is responsible for all AI-powered analysis. It connects to the Google Gemini API and generates structured research ideas from a given paper.

#### Key Design Choices

**Library: `google-genai`**
The newer `google-genai` package is used instead of the deprecated `google-generativeai`. This ensures the bot receives ongoing updates and bug fixes from Google.

**Model: `gemini-2.0-flash`**
Selected for its balance of speed and capability. Flash models are optimized for fast responses while still producing high-quality output — ideal for an automated pipeline where the user is waiting for results.

**User Input Prompt**
On launch, the bot asks the user to type in a research topic. This input is passed to `mainParser.py` via `generateContentConfig`, which acts as a custom behavior addon that tells Gemini to use the `parseARXIV` tool when searching for papers. This keeps the workflow fully automated — the user only needs to provide a topic and the agent handles everything else.

**Prompt Engineering — Chain-of-Thought Structure**
The prompt sent to Gemini is broken into four explicit steps to guide the model through a logical reasoning process before producing output:

- **Step 1 — Summarize:** Forces the model to first understand the paper before generating ideas
- **Step 2 — Identify Gaps:** Directs the model to find limitations the authors did not address
- **Step 3 — Generate Ideas:** Produces one concrete research idea per gap, each with a title, hypothesis, methodology, and impact statement
- **Step 4 — Rank:** Asks the model to rank its ideas by feasibility for a small research team

This structure prevents the model from jumping straight to idea generation without grounding its response in the paper's actual content.

**Temperature: `0`**
Temperature controls how creative vs. deterministic the model's responses are, on a scale of 0 to 1. It is currently set to `0`, meaning the model follows the prompt as precisely as possible and produces consistent, reproducible output. This is intentional for a research tool where accuracy matters more than creativity.

> **Note:** If you prefer more varied or creative research ideas, setting temperature to `0.1`–`0.2` is recommended. Going above `0.3` may produce ideas that are less grounded in the paper's content.

**`max_output_tokens`: `2048`**
Sets the maximum length of Gemini's response. This is set explicitly to prevent the model from cutting off mid-response when analyzing longer papers. For very detailed papers, this can be raised to `4096`.

**`topK`**
`topK` limits the number of candidate words the model considers at each generation step. At temperature `0`, this parameter has minimal effect since the model is already behaving deterministically. If temperature is raised to `0.1`–`0.2`, setting `topK` to `20`–`30` is recommended to keep the output focused and academic in tone rather than drifting into overly creative language.

**API Key Handling**
The Gemini API key is loaded from a `.env` file using `python-dotenv`. This keeps the key out of the source code and out of version control. Each developer on the team maintains their own `.env` file locally.

---

### `mainParser.py` — The ARXIV Tool

This script handles paper retrieval from the ARXIV database using the official ARXIV API and Python's `urllib` library.

#### Key Design Choices

**ARXIV API**
The official ARXIV API (`https://export.arxiv.org/api/query`) is used to search for papers programmatically. This avoids scraping and ensures stable, structured results.

**`urllib`**
Python's built-in `urllib` library is used to make HTTP requests to the ARXIV API. No third-party HTTP library is required, keeping dependencies minimal.

**Tool Integration via `generateContentConfig`**
`mainParser.py` is registered as a tool (`parseARXIV`) that Gemini can call during a conversation. The `generateContentConfig` in `gemini_bot.py` tells the model this tool is available, allowing Gemini to automatically trigger a paper search when the user provides a topic — without any additional user interaction.


