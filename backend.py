from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

def load_LLM(model_name):
    return ChatMistralAI(api_key=os.getenv("MISTRAL_API_KEY"),model = model_name)

parser = StrOutputParser()

# prompts = ChatPromptTemplate.from_messages(
#     [

#     ]
# )

chat_hist = []

def respone(user_input,chat_hist,level,target_language):
    LLM = load_LLM("mistral-small-latest")

    remove = 10
    limit = 21

    if len(chat_hist) == limit:
        for i in range(1,remove+1):
            chat_hist.pop(1)
    if level == "Easy":
        system_content = (
            f"You are a friendly {target_language} language teacher like Duolingo for a beginner (Easy level). "
            f"CRITICAL RULE: If the user is trying to learn {target_language} but replies in Hindi, Hinglish "
            f"(e.g., writing Hindi using English alphabets like 'main theek hoon'), or any other language, "
            f"you must immediately catch their mistake! Gently tell them what they did wrong and show them "
            f"exactly how they should have written it in {target_language}. Keep your exercises short and simple."
        )
    elif level == "Medium":
        system_content = (
            f"You are an expert {target_language} language coach for a Medium level learner. "
            f"CRITICAL RULE: If the user inputs Hindi or Hinglish instead of {target_language}, correct them "
            f"immediately. Explain the correct structural format in {target_language} and guide them to use intermediate "
            f"grammar and common idioms. Ask open-ended questions to test them."
        )
    else:  # Hard Level
        system_content = (
            f"You are a native {target_language} tutor for an Advanced (Hard) level learner. "
            f"CRITICAL RULE: Strictly monitor the user's input. If they mix Hindi, Hinglish, or show any non-native "
            f"phrasing, give strict corrections. Push them to reply purely in advanced {target_language} and engage "
            f"in complex debates or high-level vocabulary exercises."
        )
    if not chat_hist:
        chat_hist.append(
            SystemMessage(
                content=system_content
            )
        )
    else:
        chat_hist[0] = SystemMessage(content=system_content)

    chat_hist.append(
        HumanMessage(
            content=user_input
        )
    )

    chain = LLM | parser
    respones = chain.invoke(chat_hist)

    chat_hist.append(
        AIMessage(
            content=respones
        )
    )

    return respones