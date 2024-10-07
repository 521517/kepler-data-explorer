import streamlit as st
import requests
import base64

# Function to add background image and style text
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);  # Adjust the last value (0.5) to change opacity
        z-index: -1;
    }}
    /* Change text color to white for better visibility */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {{
        color: white !important;
    }}
    /* Ensure input text remains dark for readability */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {{
        color: black !important;
    }}
    /* Style the title */
    .stApp h1 {{
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
    }}
    /* Style other headers if needed */
    .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: white !important;
    }}
    /* Style expander content */
    .streamlit-expanderContent {{
        color: white !important;
    }}
    /* Style expander header */
    .streamlit-expanderHeader {{
        color: white !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
    }}
    /* Custom button style */
    .custom-button {{
        background-color: white;
        color: black;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        border-radius: 4px;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Add background image
add_bg_from_local('image.jpg')  # Replace with your image path

# FastAPI server URL
API_URL = "http://localhost:8000"  # Adjust this if your FastAPI server is running on a different URL

st.title("Kepler Data Explorer")

# Input for Kepler ID
kepid = st.number_input("Enter Kepler ID", min_value=1, step=1)

# Custom button
button_clicked = st.markdown("""
<button class="custom-button" id="get-data-button">Get Kepler Data</button>
""", unsafe_allow_html=True)

# Check if button is clicked
if button_clicked:
    try:
        # Send request to FastAPI server
        response = requests.get(f"{API_URL}/kepler/{kepid}", timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Display star system information
        st.header(f"Star System: {data['star_system']}")
        st.write(f"Number of Planets: {data['number_of_planets']}")
        st.write(f"Star Temperature: {data['star_temperature']}")
        st.write(f"Star Size: {data['star_size']}")
        if data['star_mass']:
            st.write(f"Star Mass: {data['star_mass']}")
        if data['star_age']:
            st.write(f"Star Age: {data['star_age']}")
        st.write(f"RA/Dec: {data['ra_dec']}")
        st.write(f"Discovery Date: {data['discovery_date']}")
        st.write(f"Last Update: {data['last_update']}")
        
        # Display smart summary
        st.subheader("Smart Summary")
        st.write(data['smart_summary'])
        
        # Display system note if available
        if data['system_note']:
            st.subheader("System Note")
            st.write(data['system_note'])
        
        # Display planet data
        st.subheader("Potential Planets")
        for planet in data['potential_planets']:
            with st.expander(f"Planet {planet['planet_number']}"):
                st.write(f"Orbit: {planet['orbit']}")
                st.write(f"Size: {planet['size']}")
                st.write(f"Temperature: {planet['temperature']}")
                st.write(f"Sunlight Received: {planet['sunlight_received']}")
                st.write(f"Transit Duration: {planet['transit_duration']}")
                st.write(f"Transit Depth: {planet['transit_depth']}")
                st.write(f"Detection SNR: {planet['detection_snr']}")
                st.write(f"Impact Parameter: {planet['impact_parameter']}")
                st.write("Interesting Features:")
                for feature in planet['interesting_features']:
                    st.write(f"- {feature}")
        
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the API server. Please check if the server is running and the URL is correct.")
    except requests.exceptions.Timeout:
        st.error("The request to the API server timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {str(e)}")

# JavaScript to handle button click
st.markdown("""
<script>
const button = document.querySelector('#get-data-button');
button.addEventListener('click', function() {
    // This will trigger a rerun of the Streamlit app
    button.dispatchEvent(new Event('click'));
});
</script>
""", unsafe_allow_html=True)
