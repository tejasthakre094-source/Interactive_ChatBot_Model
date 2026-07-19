import streamlit as st
from BackEnd import workflow
from langchain_core.messages import HumanMessage


st.title("CHAT BOT")
st.subheader("You Can Ask Any Question Here...")




#SessionState
if 'messageHistory' not in st.session_state:
    st.session_state['messageHistory'] = []

#Loading History
for message in st.session_state['messageHistory']:
    with st.chat_message(message["Role"]):
        st.text(message["Content"])
        
        
#{"Role":"_____","Content":______}

thread_id = "1"
config = {"configurable":{"thread_id":thread_id}}



UserInput = st.chat_input("Type Here..") 

if UserInput:
    #Adding History in UI
    st.session_state['messageHistory'].append({"Role":"User","Content":UserInput})
    
    with st.chat_message("User"):
        st.text(UserInput)
        
    response = workflow.invoke({"input": [HumanMessage(content=UserInput)]})
    AIMessage = response["messages"][-1].content
    
    with st.chat_message("Assistant"): #ICON
        #Adding History in UI
        st.session_state['messageHistory'].append({"Role":"Assistant","Content":AIMessage})
        st.success(AIMessage)

if st.button("Clear Chat"):
    st.session_state["messageHistory"] = []


