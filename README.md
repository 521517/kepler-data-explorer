# kepler-data-explorer
Kepler Data Explorer: A Streamlit web app with FastAPI backend for visualizing and exploring exoplanet data from NASA's Kepler mission. Offers interactive queries and displays of star systems and their potential planets, with AI-generated summaries powered by OpenAI.

## Overview

This application is designed to run locally but can be easily adapted to run on various hosting platforms. Its modular architecture, built around a FastAPI backend with RESTful endpoints, allows for flexibility in the choice of frontend interface. While the current implementation uses Streamlit, the backend can be integrated with any frontend technology that can make HTTP requests.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/kepler-data-explorer.git
   cd kepler-data-explorer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up API key:
   - Copy `.env.example` to `.env`: 
     ```
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key

4. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

5. In a new terminal, run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

6. Open your web browser and go to `http://localhost:8501`

## API Key

This project uses the OpenAI API for generating smart summaries of the Kepler data. You can get a key from your [OpenAI account](https://platform.openai.com/account/api-keys).

Please ensure you have the key set up in your `.env` file before running the application.

**Note:** Never share your API key publicly or commit it to the repository.

## Features

- Interactive exploration of Kepler mission exoplanet data
- AI-generated summaries of star systems and potential planets
- User-friendly interface with Streamlit
- Fast and efficient data processing with FastAPI backend
- Modular design with RESTful endpoints for easy integration with other frontends
- Designed to run locally but easily adaptable for deployment on various platforms

## Architecture

The application is split into two main components:

1. **Backend (FastAPI)**: Provides RESTful endpoints for data retrieval and processing. This modular design allows for easy integration with various frontend technologies.

2. **Frontend (Streamlit)**: Offers an interactive user interface for data exploration. While Streamlit is used in this implementation, the backend can be used with any frontend capable of making HTTP requests.

This separation of concerns allows for flexibility in deployment and future development. You can easily swap out the Streamlit frontend for another technology without changing the backend logic.

## Deployment

While this app is designed to run locally, it can be adapted for deployment on various platforms:

- **Heroku**: Use a Procfile to specify how to run both the FastAPI and Streamlit components.
- **AWS**: Deploy the FastAPI backend on EC2 or Lambda, and the Streamlit frontend on EC2 or Elastic Beanstalk.
- **Google Cloud**: Use App Engine or Compute Engine to host both components.
- **Docker**: Containerize both the backend and frontend for easy deployment on any container orchestration platform.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.