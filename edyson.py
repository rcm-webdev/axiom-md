import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents.types import AgentType
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    create_pandas_dataframe_agent,
)

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
llm_name = os.getenv("MODEL_CHOICE", "gpt-3.5-turbo")

model = ChatOpenAI(api_key=openai_key, model=llm_name)

# Load the CSV and fill missing values so the agent doesn't trip on NaNs
df = pd.read_csv("data/hot_wheels.csv").fillna(value=0)

# Create the pandas dataframe agent.
# AgentType.OPENAI_FUNCTIONS uses structured function-calling (more reliable).
# agent_executor_kwargs lets us recover gracefully from LLM parsing errors.
agent = create_pandas_dataframe_agent(
    llm=model,
    df=df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    agent_executor_kwargs={"handle_parsing_errors": True},
)


def run_agent():
    print("Edyson — Hot Wheels CSV Agent")
    print("Ask anything about your collection. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        try:
            result = agent.run(user_input)
            print(f"\nEdyson: {result}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    run_agent()
