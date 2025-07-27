
from src.workflow import visa_question_answering_batch

import streamlit as st
import time


# Initialize session state for chat history and country selection
if "messages" not in st.session_state:
    st.session_state.messages = []
if "country" not in st.session_state:
    st.session_state.country = None
if "greeting_displayed" not in st.session_state:
    st.session_state.greeting_displayed = False

# Streamlit app title
st.title("VisaGenie: Your Visa Application Assistant")

# Country selection dropdown
country = st.selectbox(
    "Which country's visa process would you like assistance with?",
    options=["Select a country", "US", "Canada", "UK"],
    index=0
)

# Update country in session state when selection changes
if country != "Select a country" and country != st.session_state.country:
    st.session_state.country = country
    st.session_state.messages = []  # Clear previous chat history
    st.session_state.greeting_displayed = False  # Reset greeting

# Display greeting if country is selected and greeting not yet shown
if st.session_state.country and not st.session_state.greeting_displayed:
    greeting = f"Hello, I am Genie. How are you today? I am ready to answer any of your questions about visa application in {st.session_state.country}."
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.greeting_displayed = True

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for user question
if st.session_state.country:
    user_input = st.chat_input("Ask your visa-related question here:")
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Processing your question..."):
                # Call the visa_question_answering_batch function
                response = visa_question_answering_batch(
                    question=user_input,
                    country=st.session_state.country,
                    model="gpt-4o"
                )
                # Simulate streaming effect
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                message_placeholder.markdown(full_response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.write("Please select a country to start the conversation.")