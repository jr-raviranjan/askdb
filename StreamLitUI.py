import streamlit as st
import requests
import json
import uuid

# Set the title of the Streamlit application (this sets the browser tab title)
st.set_page_config(page_title="askDB", layout="centered")

# --- Centering the Logo Image ---
col1_img, col2_img, col3_img = st.columns([0.5, 2, 1])  # Adjust the ratios as needed for better centering

with col2_img:  # Place the image in the middle column
  st.image("logo-transparent.png", width=None)  # Adjust width as necessary

# Initialize session_id in Streamlit's session state if it doesn't exist
if "session_id" not in st.session_state:
  st.session_state.session_id = str(uuid.uuid4())

col1_input, col2_button = st.columns([5, 1], vertical_alignment='bottom')
with col1_input:
  # Create a text input box in the middle of the page
  user_input = st.text_input(label='text input', label_visibility='hidden', placeholder="Ask Anything",key="user_input_box")

with col2_button:  # Place the button in the middle column
  submit_button = st.button("Ask")

if submit_button:  # Check if the button was clicked
  if user_input:
    # Display a progress bar while waiting for the response
    st.write("Fetching response...")
    progress_bar = st.progress(0)

    try:
      # Define the API endpoint
      api_url = "https://raviranjan2.app.n8n.cloud/webhook/send-message"

      # Prepare the data to be sent with the specified structure
      payload = {
        "chatInput": f'There are 2 collections in the mongo Database - askDB : Products and document_metadata. ' + str(json.dumps(user_input)),
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
