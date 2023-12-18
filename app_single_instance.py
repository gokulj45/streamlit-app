import streamlit as st
import json
import os
import requests

# Setup environment credentials (you'll need to change these)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "turnkey-diode-408506-8c9ed31a7f72.json" #  GCP key
project = "Streamlit App" #  GCP project
location = "us-central1" #  GCP region
model_name = 'pred_fleet_main'
endpoint = ''

# Define your Vertex AI endpoint and project information
ENDPOINT_ID="7682604402619711488"
PROJECT_ID="753148745137"
API_ENDPOINT = f"https://asia-northeast1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/asia-northeast1/endpoints/${ENDPOINT_ID}:predict"

# Set Streamlit title and description
st.title("Vehicle Fleet Maintenance Predictor")
st.write("Enter OB2 data and get predictions for possible error code")




# Create a function to make predictions
def predict(parameters):
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # Create the Vertex AI Prediction service client
    vertexai = build('ml', 'v1', credentials=credentials, cache_discovery=False)

    # Define the request for online prediction
    request_data = {
        'instances': [parameters]
    }
    
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    return response.predictions

# Create input fields for parameters
parameter1 = st.number_input("ENGINE_POWER", min_value=-20.0, max_value=20.0)
parameter2 = st.number_input("ENGINE_COOLANT_TEMP", min_value=-20.0, max_value=20.0)
parameter3 = st.number_input("ENGINE_LOAD",min_value=-20.0, max_value=20.0)
parameter4 = st.number_input("ENGINE_RPM", min_value=-20.0, max_value=20.0)
parameter5 = st.number_input("AIR_INTAKE_TEMP", min_value=-20.0, max_value=20.0)
parameter6 = st.number_input("SPEED", min_value=-20.0, max_value=20.0)
parameter7 = st.number_input("THROTTLE_POS", min_value=-20.0, max_value=20.0)
parameter8 = st.number_input("TIMING_ADVANCE", min_value=-20.0, max_value=20.0)
parameter9 = st.number_input("SHORT_TERM_FUEL_TRIM_BANK", min_value=-20.0, max_value=20.0)

trouble_codes = { 0:'C0300', 1:'NIL', 2:'P0078B0004P3000', 3:'P0078U1004P3000', 4:'P0079C1004P3000', 5:'P0079P1004P3000', 6:'P0079P2004P3000', 7:'P007EP2036P18D0', 8:'P007EP2036P18E0', 9:'P007EP2036P18F0', 10:'P007FP2036P18D0', 11:'P007FP2036P18E0', 12:'P007FP2036P18F0'}

# Create a button to trigger predictions
# Create a button to trigger predictions
if st.button("Get Prediction"):
    # Create a dictionary with input data
    input_data = {
        "instances": [[parameter1,parameter2,parameter3, parameter4, parameter5, parameter6, parameter7, parameter8, parameter9]]
    }

    # Convert the input data to JSON format
    input_json = json.dumps(input_data)

    # Define headers for the POST request
    headers = {
        "Authorization": f"Bearer {'ya29.c.b0Aaekm1I_T3Fln224QvslqGtgdHL7g7c5Ce6hflJ4eDWowYSYouanhtHXRm_ODB6XEqvUwvnel9SXUlauApiIz2859OawTFxTp_wB4ODbm45_HclCdZNzys749hlluA1qHZArZCrueH1kbG9VdcAYFu7W7A5ExTKPFWNAIblkYuu_a_hqgaFOSkUd8aHe0w10hsTUWRLFWfjAg2F3HyG2H-ARWY8EKuLNuY7oz1yllJ1i1dUI8TVzeGwqVDi2ObdLaP1jho5gJrcufwBX-jDMrw04d5bRa3kMv928k5ZkK9G-PqEWNnuEljkywFOo1NSrqAKcVBNcISwnwKU3QTba4VfPZwT355C4zc-7Q4fXrB6i3hjSf3SczuyeUYu3nbuZ9cqY6n0RMWz7er-7UXVuVoJkc3oJViWBsqhQfcgrnoss1V17jQ7vaqymQig8Utuaw9IOeUoojIm25sac2MBi8WUmFfzvtFQmOv7znqg4zd3fqUX47hyMwqn7rYIaRyfIvwWtBnit7J1_yyUtzS25iykrJ7hoYV2QFZwROdiSzpO71J7UYUZejWysFi8lnR8dnrZmgj3rfMj-ffM0R21oW4uXkyzXQcgjo6e607Wc5uFj9lO4_7vVYQUqRlOZ3v3-e1lzcXZvrX36a8OO8yxz22pQxO05-JX4XQtItM2pliFg5n2nuSyIQ__e9U9IVFq4Zs6Q9vs0Ip2uzZ7X281vFidXX8F_I3axmdtOWpmXsovh7aWlVdzM8__mw8bQphhFnom-ovBewhis0lsYpBOSZQF2kvYtb9SvBqtJ56Y1RQ_9Z3B7_nBfmUyk03wUUB4YVqk26eUqQUmUef4myfetZsYcXOpgMvJRBwxuehrW5pwUbm41XyfoX3ouQhev4era2btx7BnclhIqsR7VRvgtuaVZwccXVcv5S4spBndalkqu2uQQibJ45ZSS3iUvoQklyjbQh7m7MZcbX78sneqVbBsQRZldc7f7FayS4fX7p1UyI4_XMrbZdkh'}",  # Replace with your access token
        "Content-Type": "application/json"
    }

    # Make the POST request to the Vertex AI endpoint
    response = requests.post(API_ENDPOINT, data=input_json, headers=headers)

    if response.status_code == 200:
        prediction = response.json()
        # Display the prediction results
        st.write("Prediction Results:")
        st.write(json.dumps(trouble_codes[prediction["predictions"][0]], indent=4))

    else:
        st.error("Error: Failed to make the prediction request. Check your credentials and input data.")


# Note: You will need to replace 'your-gcp-project-id' and 'your-vertex-ai-model-name' with your actual project ID and model name.
