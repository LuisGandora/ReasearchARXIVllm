import os
import textwrap
import mainParser
from dotenv import load_dotenv
from google import genai
from google.genai import types


class googleChat:
    def __init__(self):
        load_dotenv()

        laKey = os.getenv("GEMINI_API_KEY")
        projectID = os.getenv("PROJECTKEY")
        self.client = genai.Client(vertexai=True, project=projectID, location="us-central1")


    def generate_research_ideas(self, paper_title: str = "Unknown") -> str:
        """Takes the full text of an arxiv paper and uses Gemini to generate new research ideas inspired by it."""

        prompt = textwrap.dedent(f"""You are an expert AI research assistant specializing in 
        academic paper analysis and research ideation. Your role is to deeply analyze 
        research papers and propose novel, feasible research directions.

        You are analyzing the following research paper:

        TITLE: {paper_title}
        ---

        Please follow these steps carefully:

        STEP 1 - TOOL CALL:
        Utilize the tool given (mainparser.parse.ARXIV) to get the top 5 research papers raw HTML in a given topic: {paper_title},
        upon successful call of this tool, proceed to the next steps.
        If you are not able to call the tool, respond with: "ERROR: Could not use ARXIV API, are you sure you are online and that the right modules are imported?"

        STEP 2 - SUMMARIZE:
        For each paper (contained in html element "entry") visit each paper's pdf file via the 'link href=' tag (Withing the title="pdf" element) to view its content
          and summarize each papers topic in 3-4 sentences

        STEP 3 - IDENTIFY GAPS:
        List 3 clear limitations or open questions the authors did NOT fully address within each paper's summary from STEP 2.

        STEP 4 - GENERATE IDEAS:
        For each gap, propose ONE concrete new research idea. For each include:
        - Title:       A short descriptive name
        - Hypothesis:  What you predict and why
        - Methodology: How you would test or implement it
        - Impact:      Why this matters to the field

        STEP 5 - RANK:
        Rank your 3 ideas from most to least feasible for a small research team 
        and briefly explain your reasoning.

        STEP 6 - REFERENCES:
        Reference each paper searched in this format utilizing the title and all author elements: "Title: title, PDFLink: pdf, Authors: author1, author2, ..."

        Be specific, grounded in the paper's content, and think like a senior researcher.
        """)

        print(f"\n🤖 Sending paper to Gemini for analysis...")
        print(f"📄 Paper: {paper_title}\n")

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig( #Generate Content Config allows for custom behavior for a bot
                    tools=[mainParser.parseARXIV], #Ensure parseARXIV is called
                    temperature=0.0 #Controls 'creativeness' of the bot, ensures that the bot follows the prompt exactly
                    #Experiment with the other elements such as top_k and max_output_tokens to control output and
                    #Doc what you add for the presentation
                )
            )
        except Exception as e:
            return f"Error API: {str(e)}"


        return response.text
        # return "Hello"


    def run_agent(self, paper_title: str = " ") -> None:
        """
        Main entry point called by your partner's arxiv downloader.
        """
        if paper_title == " ":
            print("Please input a valid research topic")
            return
        ideas = self.generate_research_ideas(paper_title)

        print("=" * 60)
        print("💡 GENERATED RESEARCH IDEAS")
        print("=" * 60)
        print(ideas)
        print("=" * 60)


if __name__ == "__main__":
    # sample_text = """
    # Abstract: This paper presents a novel approach to transformer-based
    # language models using sparse attention mechanisms. We demonstrate that
    # by reducing attention to only the top-k tokens per layer, we achieve
    # 90% of the performance of full attention at 40% of the compute cost.
    # Our experiments on GLUE and SuperGLUE benchmarks confirm these findings.
    # We propose this as a scalable solution for deploying LLMs on edge devices.
    # """
    #New model, take a research topic from a user then use that to prompt the AI to obtain the info with the parser
    temp = googleChat()
    print("Input a research topic to generate new ideas from prexisting papers: " ,end=" ")
    researchTopic = input()
    print()
    temp.run_agent(researchTopic)