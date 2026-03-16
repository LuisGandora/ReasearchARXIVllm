import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_research_ideas(paper_text: str, paper_title: str = "Unknown") -> str:
    """
    Takes the full text of an arxiv paper and uses Gemini to generate
    new research ideas inspired by it.
    """

    prompt = f"""You are an expert AI research assistant specializing in 
academic paper analysis and research ideation. Your role is to deeply analyze 
research papers and propose novel, feasible research directions.

You are analyzing the following research paper:

TITLE: {paper_title}

PAPER CONTENT:
{paper_text[:12000]}

---

Please follow these steps carefully:

STEP 1 - SUMMARIZE:
In 3-4 sentences, summarize the core contribution and methodology of this paper.

STEP 2 - IDENTIFY GAPS:
List 3 clear limitations or open questions the authors did NOT fully address.

STEP 3 - GENERATE IDEAS:
For each gap, propose ONE concrete new research idea. For each include:
  - Title:       A short descriptive name
  - Hypothesis:  What you predict and why
  - Methodology: How you would test or implement it
  - Impact:      Why this matters to the field

STEP 4 - RANK:
Rank your 3 ideas from most to least feasible for a small research team 
and briefly explain your reasoning.

Be specific, grounded in the paper's content, and think like a senior researcher.
"""

    print(f"\n🤖 Sending paper to Gemini for analysis...")
    print(f"📄 Paper: {paper_title}\n")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text


def run_agent(paper_text: str, paper_title: str = "Unknown") -> None:
    """
    Main entry point called by your partner's arxiv downloader.
    """
    if not paper_text or len(paper_text.strip()) < 100:
        print("❌ Error: Paper text is too short or empty.")
        return

    ideas = generate_research_ideas(paper_text, paper_title)

    print("=" * 60)
    print("💡 GENERATED RESEARCH IDEAS")
    print("=" * 60)
    print(ideas)
    print("=" * 60)


if __name__ == "__main__":
    sample_text = """
    Abstract: This paper presents a novel approach to transformer-based
    language models using sparse attention mechanisms. We demonstrate that
    by reducing attention to only the top-k tokens per layer, we achieve
    90% of the performance of full attention at 40% of the compute cost.
    Our experiments on GLUE and SuperGLUE benchmarks confirm these findings.
    We propose this as a scalable solution for deploying LLMs on edge devices.
    """
    run_agent(sample_text, "Sparse Attention Transformers for Edge Deployment")