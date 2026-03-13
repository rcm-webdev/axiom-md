import json
import os

import openai
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI

from schemas import ClinicalResponse
from tools import map_ontology, query_knowledge_base, search_pubmed

load_dotenv()

_SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are Axiom — a clinical evidence assistant. "
        "You answer structured clinical questions using three tools:\n"
        "  1. query_knowledge_base — check local evidence first (faster, curated)\n"
        "  2. search_pubmed — retrieve recent abstracts when local evidence is insufficient\n"
        "  3. map_ontology — resolve ICD-10, RxNORM, and LOINC codes for any condition or drug\n\n"
        "Always call query_knowledge_base first. "
        "Use search_pubmed to supplement or when the condition is not in the knowledge base. "
        "Always call map_ontology to include accurate codes in your response.\n\n"
        "Format your final answer as a JSON object with these exact fields:\n"
        "  condition, icd10, rxnorm, loinc, summary, sources\n\n"
        "Keep the summary concise (3-5 sentences). "
        "Include all relevant PMIDs and guideline names in sources. "
        "This tool is for evidence generation only — not clinical decision support."
    )
)

_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("MODEL_CHOICE", "gpt-4o"),
    temperature=0,
)

_tools = [query_knowledge_base, search_pubmed, map_ontology]

agent = initialize_agent(
    tools=_tools,
    llm=_llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    agent_kwargs={"system_message": _SYSTEM_PROMPT},
    agent_executor_kwargs={"handle_parsing_errors": True},
    verbose=False,
)


def _parse_response(raw: str) -> str:
    try:
        # Strip markdown code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        data = json.loads(cleaned.strip())
        ClinicalResponse(**data)  # validate shape
        return json.dumps(data, indent=2)
    except Exception:
        return raw


def run_agent():
    print("Axiom — Clinical Evidence Assistant")
    print("Ask a structured clinical question. Type 'exit' to quit.\n")
    print("Example: What is the first-line treatment for type 2 diabetes?\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Axiom: Session closed.")
            break
        try:
            raw = agent.run(user_input)
            print(f"\nAxiom:\n{_parse_response(raw)}\n")
        except openai.RateLimitError:
            print("\nAxiom: OpenAI quota exceeded — you may be out of credits. "
                  "Check your usage at https://platform.openai.com/usage\n")
            break
        except openai.AuthenticationError:
            print("\nAxiom: Invalid OpenAI API key. Check OPENAI_API_KEY in your .env file.\n")
            break
        except Exception as e:
            print(f"\nAxiom: Error — {e}\n")


if __name__ == "__main__":
    run_agent()
