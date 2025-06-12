import streamlit as st
import requests
import json
import uuid

# Set the title of the Streamlit application (this sets the browser tab title)
st.set_page_config(page_title="askDB", layout="centered")

# Custom CSS for centering the text box and improving aesthetics with blue shades
st.markdown("""
<style>
    /* Blue shades for text input border */
    .stTextInput > div > div > input {
        text-align: center;
        font-size: 1.2em;
        padding: 0px;
        border-radius: 8px;
        border: 1px solid #4682B4; /* SteelBlue */
    }
    /* Primary blue for buttons */
    .stButton > button {
        background-color: #1E90FF; /* DodgerBlue */
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1.1em;
        transition: background-color 0.3s ease;
    }
    /* Darker blue on button hover */
    .stButton > button:hover {
        background-color: #1874CD; /* Darker shade of DodgerBlue */
    }
    .main .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding-top: 20px; /* Reduced padding-top to bring elements closer */
    }
    .stProgress > div > div > div > div {
        background-color: #1E90FF; /* DodgerBlue */
    }
    .response-box {
        background-color: #E0F2F7; /* Very light blue */
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        width: 100%;
        max-width: 700px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        word-wrap: break-word;
        text-align: left;
    }
    .response-title {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333; /* Keeping dark text for readability */
    }
</style>
""", unsafe_allow_html=True)

# --- Centering the Logo Image ---
col1_img, col2_img, col3_img = st.columns([1, 2, 1]) # Adjust the ratios as needed for better centering

with col2_img: # Place the image in the middle column
    st.image("logo-transparent-bg.png", width=300) # Adjust width as necessary

# Initialize session_id in Streamlit's session state if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Create a text input box in the middle of the page
user_input = st.text_input("Enter your query here:", key="user_input_box")

# --- Centering the Submit Button ---
# Create columns to center the button
col1_btn, col2_btn, col3_btn = st.columns([1.4, 1, 1]) # Adjust ratio if button doesn't center perfectly

with col2_btn: # Place the button in the middle column
    submit_button = st.button("Submit Data")

if submit_button: # Check if the button was clicked
    if user_input:
        # Display a progress bar while waiting for the response
        st.write("Fetching response...")
        progress_bar = st.progress(0)

        try:
            # Define the API endpoint
            api_url = "https://isha-vankineni.app.n8n.cloud/webhook/f610096a-b5d7-4ea6-a46b-3315f6d8865c"

            # Prepare the data to be sent with the specified structure
            payload = {
                "chatInput": json.dumps(user_input),
                "sessionId": st.session_state.session_id,
                "user": "user"
            }

            # Make the API call
            response = requests.post(api_url, json=payload)

            # Update the progress bar to 100%
            progress_bar.progress(100)

            # Check if the API call was successful
            if response.status_code == 200:
                st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                st.markdown("<div class='response-title'>API Response:</div>", unsafe_allow_html=True)

                # Try to parse the response as JSON
                try:
                    json_response = response.json()
                    st.json(json_response)
                except json.JSONDecodeError:
                    st.write(f"Raw text response: {response.text}")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Display error message if API call was not successful
                st.error(f"Error: API call failed with status code {response.status_code}")
                st.error(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            # Catch network or request-related errors
            st.error(f"An error occurred: {e}")
        finally:
            progress_bar.empty()

    else:
        st.warning("Please enter some data before submitting.")