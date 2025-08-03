from src.workflow import visa_question_answering_batch

import streamlit as st
import time

# Initialize session state for chat history and country selections
if "messages" not in st.session_state:
    st.session_state.messages = []
if "country" not in st.session_state:
    st.session_state.country = None
if "home_country" not in st.session_state:
    st.session_state.home_country = None
if "greeting_displayed" not in st.session_state:
    st.session_state.greeting_displayed = False

# Streamlit app title
st.title("VisaGenie: Your Visa Application Assistant")

# Select home country (origin)
home_country = st.selectbox(
    "What is your home country (your nationality)?",
    options=["Select your home country", "India", "China", "Mexico", "Brazil", "Germany", "Other"],
    index=0
)

# Select destination country
country = st.selectbox(
    "Which country's visa process would you like assistance with?",
    options=["Select a destination country", "US", "Canada", "UK"],
    index=0
)

# Update session state based on selections
if home_country != "Select your home country":
    st.session_state.home_country = home_country
if country != "Select a destination country":
    if country != st.session_state.country:
        st.session_state.country = country
        st.session_state.messages = []  # Clear chat history when destination country changes
        st.session_state.greeting_displayed = False

# Display greeting if both countries are selected
if st.session_state.home_country and st.session_state.country and not st.session_state.greeting_displayed:
    greeting = (
        f"Hello, I am Genie. How are you today? I am ready to answer any of your questions "
        f"about visa application for {st.session_state.country}, considering you're from {st.session_state.home_country}."
    )
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.greeting_displayed = True

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for user question
if st.session_state.home_country and st.session_state.country:
    user_input = st.chat_input("Ask your visa-related question here:")
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Processing your question..."):
                response = visa_question_answering_batch(
                    question=user_input,
                    home_country=st.session_state.home_country,
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

        # Store assistant response
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.write("Please select both your home country and the destination country to begin.")
