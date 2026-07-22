import streamlit as st
from BackEnd import workflow
from langchain_core.messages import HumanMessage
import uuid

#**********************************************************MAin UI************************************************************
st.title("CHAT BOT")
st.subheader("You Can Ask Any Question Here...")

# *****************************************************Utility Functions*******************************************************
#Dynamic Thread ID generation
def GenerateThreadId():
    thread_id = uuid.uuid4()
    return thread_id 

def ResetChat():
    thread_id= GenerateThreadId()
    st.session_state['thread_id'] = thread_id
    Add_threadID(st.session_state['thread_id'])
    st.session_state['messageHistory'] = []


def Add_threadID(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation_history(thread_id):
    return workflow.get_state(config= {"configurable" : {'thread_id' :thread_id}} ).values['message']


#********************************************************Session State Setup*********************************************************
if 'messageHistory' not in st.session_state:
    st.session_state['messageHistory'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = GenerateThreadId()


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []
    
Add_threadID(st.session_state['thread_id'])

#********************************************************SideBar UI**************************************************
st.sidebar.title("Chat History")

if st.sidebar.button("New Chat"):
    ResetChat()
    
st.sidebar.header("My Conversations :")


#*******************************************************OnClick History Loading**********************************************

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        message = load_conversation_history(thread_id)
        
        temp_msg =[]
        
        for m in message:
            if isinstance(m ,HumanMessage):
                Role = "User"
            else:
                Role="Assistant"
            temp_msg.append({"Role":Role,"Content":m.content})
            #{"Role":"_____","Content":______}
            
        st.session_state['messageHistory'] =temp_msg


#*******************************************************Loading History***********************************************
for message in st.session_state['messageHistory']:
    with st.chat_message(message["Role"]):
        st.text(message["Content"])
#{"Role":"_____","Content":______}


config = {"configurable":{"thread_id":st.session_state['thread_id']}} #Thread_id added


#******************************************************User Input******************************************************

UserInput = st.chat_input("Type Here..") 

if UserInput:
    #Adding History in UI
    st.session_state['messageHistory'].append({"Role":"User","Content":UserInput})
    
    with st.chat_message("User"):
        st.text(UserInput)
    #Old COde Without Streaming
    # response = workflow.invoke({"message":[HumanMessage(content=UserInput)]},config=config)
    # AIMessage = response['message'][-1].content
    
    with st.chat_message("Assistant"): #ICON
        #Streaming Inplementation
        AIMessage = st.write_stream(
            message_chunk.content for message_chunk ,metadata in workflow.stream(
                {"message":[HumanMessage(content=UserInput)]},
                config=config,
                stream_mode="messages"
            )
        )
    #Adding History in UI
    st.session_state['messageHistory'].append({"Role":"Assistant","Content":AIMessage})
    # st.success(AIMessage)



