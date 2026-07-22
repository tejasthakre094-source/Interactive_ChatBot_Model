from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph ,START,END
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="zai-org/GLM-5.2",
    task="text-generation"
)
ChatModel = ChatHuggingFace(llm=llm)

# State
class ChatBotStateMemory(TypedDict):
    message : Annotated[list[BaseMessage],add_messages]
    
    
#Node
def GenerateResponse(state : ChatBotStateMemory):
    message = state['message']
    response = ChatModel.invoke(message)
    return {'message':[response]}
    
#CheckPointer
Checkpointer = MemorySaver()
    
#Graph 
graph = StateGraph(ChatBotStateMemory)
graph.add_node("GenerateResponse",GenerateResponse)

graph.add_edge(START,"GenerateResponse")
graph.add_edge("GenerateResponse",END)

#compile
workflow = graph.compile(checkpointer=Checkpointer)
print(workflow)