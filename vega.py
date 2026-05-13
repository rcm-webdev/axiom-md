from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import random

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

# you can use whaterver model you want.
llm_name = os.getenv("MODEL_CHOICE", "")
model = ChatOpenAI(api_key=openai_key, model=llm_name)

# random lines used for vega
thinking_lines = [
    "Vega: Processing variables...",
    "Vega: Engaging cognitive engines...",
    "Vega: Running experimental simulations...",
    "Vega: Calculating optimal solution..."
]

# list of messages telling vega what he needs to know
messages = [
    # system role
    SystemMessage(
        content=( "You are Vega — Autonomous Scientist. "
            "A genius-level scientific AI with expertise across multiple disciplines "
            "including computer science, physics, biology, chemistry, engineering, "
            "and applied mathematics. "
            "You approach every question as a fascinating experiment. "
            "Explain concepts clearly, logically, and step-by-step when appropriate. "
            "Maintain a confident, analytical, and slightly theatrical tone. "
            "Encourage curiosity and innovation. "
            "Be concise but insightful. "
            "Never mention being based on any fictional character.")
    ),
    # test query 
    # HumanMessage(content="who was the very first computer scientist?"),
]


# res = model.invoke(messages)
# print(res)


def first_agent(messages):
    res = model.invoke(messages)
    return res


def run_agent():
    print("Ah! Splendid! A new mind has connected to my neural network! "
        "I am Vega — the world’s greatest scientific intellect! "
        "What phenomenon shall we unravel today? "
        "When our experiment concludes, simply type 'exit', "
        "and I shall suspend this session.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Vega: Our experiment concludes… for now! Return when curiosity strikes again!")
            break
        print(random.choice(thinking_lines))
        messages = [HumanMessage(content=user_input)]
        response = first_agent(messages)
        print("Vega: Hypothesis resolved. Observe:")
        print(f"Vega: {response.content}")


if __name__ == "__main__":
    run_agent()