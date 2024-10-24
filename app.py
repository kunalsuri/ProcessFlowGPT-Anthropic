import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Function to get the API key
def get_claude_api_key():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please add it to the .env file.")
    return api_key

# Streaming response using Claude API
def generate_response_with_claude_stream(prompt, model="claude-3-5-sonnet-20241022", max_tokens=1024, temperature=0.7):
    api_key = get_claude_api_key()

    # Initialize the client
    client = anthropic.Anthropic(api_key=api_key)

    # Stream the API response
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text  # Yield each piece of text as it's streamed

# Streamlit app UI
def main():
    st.title("Claude 3.5 Streaming Response App")
    st.write("""
    Welcome! Enter any text prompt, and Claude 3.5 will generate a response in real-time. This can be anything from general questions to code generation.
    """)

    # Create a form for user input
    with st.form(key="claude_form"):
        prompt = st.text_area("Enter your prompt", height=200, placeholder="Ask anything, such as a code request or general question...")
        max_tokens = st.slider("Max Tokens", min_value=100, max_value=5000, value=1024)
        submit_button = st.form_submit_button(label="Generate Response")

    # When the user submits the form
    if submit_button:
        if prompt.strip() == "":
            st.error("Prompt cannot be empty!")
        else:
            st.info("Generating response... please wait.")
            try:
                # Placeholder to display the response as it streams
                response_placeholder = st.empty()

                # Stream the response in real-time and update the output as it comes in
                full_response = ""
                for streamed_text in generate_response_with_claude_stream(prompt, max_tokens=max_tokens):
                    full_response += streamed_text
                    response_placeholder.text(full_response)  # Update placeholder with the current streamed text

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
