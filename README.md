# Vega

![Vega](public/vega-scientist.jpg)

> Vega: "Ah! Splendid! A new mind has connected to my neural network! What phenomenon shall we unravel today?"
>
> You: "What can you tell me about the One Piece?" 
>
> Vega: "..."
>
> You: "😭"


**Vega** is an *AI Agent* ready to answer questions across multiple disciplines (computer science, biology, physics, mathematics, etc.)

Users can interact with Vega through the console. 

## How its made: 
### Tech Stack
- Python
- LangChain
- OpenAI API

### AI first development: 
- Initial goal is to build a simple AI Agent using langchain as a wrapper.
- LangChain was my first choice as it does most of the heavy lifting when it comes to building AI agents. 
- Wanted to learn more about computer science concepts in an fun & interactive way. 
- This evolved into building an agent based on a One Piece anime character, Vegapunk, who is a genius in all things. 
- Final product: an all in one interactive CLI AI Agent - **Vega**. 

## Optimizations
- Currently users can only interact with Vega through the console, looking to build a user interface. 
- Vega currently does not have any memory/context with a specific user. When the session is closed, he has no idea about any previous conversations or who he was talking to.
- Looking to include memory using mem0(mem-zero)
- Plan to utilize a SQL db like Supabase for authentication to create user profiles as well as using the db to store vector data as long-term memory allowing Vega to remember previous conversations
- With Mem0 and Supabase on board, Vega will transform into an intelligent system that will learn and adapt the longer users interact with the tool.
- Potentially add any rate-limits, because, obvious reasons...costs...

## Lessons Learned
- Build an AI Agent leveraging the LangChain framework
- Quickly learned about limitations with the current setup. In the future, I look to expand this project to build an intelligent context aware system that will likely help others in a fun/interactive way. 
- Learned more about building agents in general - the idea is to build products that deliver value. To me, this agent allowed me to ask questions and workshop with an intelligent/lightweight system.

## How to run Vega

- change `.env.sample` to `.env`
- update `.env` with your API credentials and model choice (e.g.gpt-4o-mini)
- setup and activate your virtual environment

Install dependencies:
  
```bash
pip install -r requirements.txt
```
Running the agent: 

```bash
python vega.py
```

This starts an interactive CLI loop. Type `exit` to quit.
  




