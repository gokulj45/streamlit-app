import streamlit as st
import json
import os
import requests

# Setup environment credentials (you'll need to change these)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "avid-airway-395106-6bdba380ed64.json" #  GCP key
project = "2021FC04388-Project" #  GCP project
location = "us-central1" #  GCP region
model_name = 'pred_fleet_main'
endpoint = ''

# Define your Vertex AI endpoint and project information
ENDPOINT_ID = "2036913460175962112"
PROJECT_ID = "674751985345"
API_ENDPOINT = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/endpoints/{ENDPOINT_ID}:predict"

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
parameter1 = st.number_input("ENGINE_POWER", min_value=-20.0000000, max_value=20.000000)
parameter2 = st.number_input("ENGINE_COOLANT_TEMP", min_value=-20.0000000, max_value=20.000000)
parameter3 = st.number_input("ENGINE_LOAD",min_value=-20.0000000, max_value=20.000000)
parameter4 = st.number_input("ENGINE_RPM", min_value=-20.0000000, max_value=20.000000)
parameter5 = st.number_input("AIR_INTAKE_TEMP", min_value=-20.0000000, max_value=20.000000)
parameter6 = st.number_input("SPEED", min_value=-20.0000000, max_value=20.000000)
parameter7 = st.number_input("THROTTLE_POS", min_value=-20.0000000, max_value=20.000000)
parameter8 = st.number_input("TIMING_ADVANCE", min_value=-20.0000000, max_value=20.000000)
parameter9 = st.number_input("SHORT_TERM_FUEL_TRIM_BANK", min_value=-20.0000000, max_value=20.000000)

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
        "Authorization": f"Bearer {'ya29.c.b0Aaekm1JD8uc6pLNd0gQCw1iyb1qaRFf5VX8jE3mkR-dHBMNdL3fr6j4mNwXl5Y50Dnuu19uqcyDKCZ3WXc8M2f2LH2BxnZMC2hkdxF3c5amqXf_OvQb_YMDVLx81F9ic_tygCiP4bahBZZiB98vpRtsQhNbc6fq-JvHc6jJdFkfBO9MM7qpaVnTdujrudi2m3mN7iyCIJhlFEPupyNOpqMpKAH034DxvMPP35z7srBF4KGb9kRu5voI3ed71H_WKZXO8hBGIpstwYI1uP5bG5naiUsBMSyPUwysVkujPJiq0nhpePCu8nexoUIKLaSGrL1NV8fkw0hxDe1OyDcznKtm54gH355D9FjawhdjmmzbiZu0gIeWOv3ZW8ZqQjgvw1FJqQp7xtxMFx9gRjQMahWjBXocn-S45VFWVOb5bbcpn2ushh7tMcZpUwvt4q910SXRSVntkvj5ah075wiVMf0mWv9xUUQ0lietnkn83fmI_3gUgBqiJtwSudek7WXgufBxfIm5nSXm6j5pBMnO-2alW-V260RrxuV3M96uqqktlZe2_Y9hwed7BlOst5Bl6mbWkBIM7f6aOoyhy_UBhQvV_w5i5lpnsWb6__ySrk6IRmRopgm1Frqy6bVqQn6aSq1qBgOcz-b4Od0gftzsBswsJs8kzBemjFoviIpR6vVl1bWxcteWqo80UV1M_4sFBrWb4eyctu5djWrWws2B1eSjnq4jcqBMfl_qFMJoSJvuIFymupF76w8fhB_yuZzjXwnujkd3v1J_5Swdp1-ub7r0cUZ9xffYpZekkgaFgvrrmv45o42zs2d2hbhiUFBQpFOjZI6U6o0qqUz75RwRYJkSVej4oUZuw0Mg3stM78Utb86dnX6jRjlftVvZXjrfgoh9Y8RvQ15cJ9xXrm4n8Xk-OROMI5BYgtrBOZtOZWc64flmw4_yQaySoWxSo8hYbVmQVMZ6Z3df562eXbSuy6hVM4vjs16n5U9tvBw8w-Jzeh2eSyB7aptn'}",  # Replace with your access token
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
