import requests
import pandas as pd
from fastapi import HTTPException
import numpy as np
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Use this variable instead of hardcoded key
client = OpenAI(api_key=OPENAI_API_KEY)

SUMMARY_MODEL = "gpt-4o-mini-2024-07-18"  # or whichever model you prefer

SystemMessage= """You are an AI astronomer assistant. You have to provide a short summary of the data you are receiving. The data is from NASA datasets about exoplanets. It will contain information about stars and potential exoplanets. Respond with a short summary of the data, including units and interesting facts if applicable. For example, if you notice something unusual or interesting in the data, feel free to mention that. Start with the name of the star. No need to format it just row text."""

def query_tce_by_kepid(kepid):
    tap_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    
    query = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "QUERY": f"""
            SELECT *
            FROM q1_q17_dr25_tce 
            WHERE kepid = {kepid}
            ORDER BY tce_plnt_num
        """,
        "FORMAT": "json"
    }
    
    response = requests.get(tap_url, params=query)
    return response

def format_discovery_date(date_value):
    if isinstance(date_value, str):
        return date_value.split()[0]
    elif isinstance(date_value, (float, np.float64)):
        # Assuming the float represents days since a specific epoch, you might need to adjust this
        return f"Day {int(date_value)}"
    else:
        return "Unknown"

def generate_smart_summary(data: dict) -> str:
    print("Generating smart summary")

    # Convert data to string
    data_str = json.dumps(data, indent=2)

    messages_list = [
        {
            "role": "system",
            "content": SystemMessage,
        },
        {
            "role": "user",
            "content": f"Here is the data for a Kepler system:\n\n{data_str}\n\nPlease provide a concise summary of this Kepler system, highlighting its most interesting features and potential for habitability or unusual characteristics."
        }
    ]

    try:
        completion = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=messages_list,
        )

        # Get the result
        summary = completion.choices[0].message.content

        return summary

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Unable to generate summary at this time."

def process_nasa_data(kepid):
    response = query_tce_by_kepid(kepid)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data from NASA")
    
    data = response.json()
    if not data:
        raise HTTPException(status_code=404, detail=f"No data found for KepID {kepid}")
    
    df = pd.DataFrame(data)
    
    result = {
        "star_system": f"Kepler-{kepid}",
        "number_of_planets": len(df),
        "star_temperature": f"{df['tce_steff'].iloc[0]:,.0f} Kelvin (Earth's Sun is about 5,800 Kelvin)",
        "star_size": f"{df['tce_sradius'].iloc[0]:.2f} times the size of Earth's Sun",
        "star_mass": f"{df['tce_smass'].iloc[0]:.2f} times the mass of Earth's Sun" if 'tce_smass' in df.columns else None,
        "star_age": f"{df['tce_sage'].iloc[0]:.2f} billion years" if 'tce_sage' in df.columns else None,
        "ra_dec": f"RA: {df['ra'].iloc[0]:.4f}, Dec: {df['dec'].iloc[0]:.4f}",
        "potential_planets": [],
        "discovery_date": format_discovery_date(df['tce_time0bk'].iloc[0]) if 'tce_time0bk' in df.columns else "Unknown",
        "last_update": "Data from Q1-Q17 DR25 TCE catalog",
        "smart_summary": ""
    }
    
    for _, planet in df.iterrows():
        planet_data = {
            "planet_number": int(planet['tce_plnt_num']),
            "orbit": f"Circles its star every {planet['tce_period']:.2f} days",
            "size": f"About {planet['tce_prad']:.1f} times bigger than Earth",
            "temperature": f"Approximately {planet['tce_eqt']:.0f} Kelvin",
            "sunlight_received": f"{planet['tce_insol']:.0f} times more than Earth gets",
            "transit_duration": f"{planet['tce_duration']:.2f} hours",
            "transit_depth": f"{planet['tce_depth']:.2f} parts per million",
            "detection_snr": planet['tce_model_snr'],
            "impact_parameter": planet['tce_impact'],
            "interesting_features": []
        }
        
        if planet['tce_period'] < 1:
            planet_data["interesting_features"].append("This planet orbits very quickly!")
        if planet['tce_prad'] > 15:
            planet_data["interesting_features"].append("This planet is extremely large!")
        if 200 < planet['tce_eqt'] < 300:
            planet_data["interesting_features"].append("This planet's temperature might allow for liquid water!")
        if planet['tce_insol'] > 10000:
            planet_data["interesting_features"].append("This planet receives an extreme amount of starlight!")
        
        result["potential_planets"].append(planet_data)
    
    if len(df) > 5:
        result["system_note"] = "This star has an unusually high number of potential planets!"
    
    # Generate the smart summary
    result["smart_summary"] = generate_smart_summary(result)

    return result

if __name__ == "__main__":
    kepid = 4276002  # Example KepID
    data = process_nasa_data(kepid)
    print(json.dumps(data, indent=2))

