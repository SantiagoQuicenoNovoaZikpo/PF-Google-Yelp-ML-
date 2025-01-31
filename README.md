![WhatsApp Image 2025-01-15 at 1 17 45 AM](https://github.com/user-attachments/assets/941f9a8e-09f0-4efe-a187-bca099eeeff7)

# Yelp Data Analysis Project

## Overview
This project is undertaken by **SJA COSMOS DATA ADVISORS**. We have been contracted by a company that wants to open a new restaurant. Our task is to determine the best city for this new restaurant based on comprehensive data analysis. This involves performing Exploratory Data Analysis (EDA), Extract, Transform, Load (ETL) processes, Machine Learning (ML) modeling, and creating a Power BI dashboard to present our findings.

## Table of Contents
- [Project Setup](#project-setup)
- [Technologies](#technologies)
- [Data Collection and Storage](#data-collection-and-storage)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [ETL Process](#etl-process)
- [Machine Learning](#machine-learning)
- [Deploying the ML Model on Streamlit](#deploying-the-ml-model-on-streamlit)
- [Power BI Dashboard](#power-bi-dashboard)
- [Contributors](#contributors)
- [License](#license)

## Project Setup
1. **Clone the repository**:
    ```sh
    git clone https://github.com/SantiagoQuicenoNovoaZikpo/PF-Google-Yelp-ML-.git
    cd PF-Google-Yelp-ML-
    ```
2. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Technologies
- **Google Cloud Platform (GCP)**:
  - BigQuery
  - Cloud Storage
  - Cloud Functions
  - Cloud Shell
  - AI Platform
- **Python**:
  - pandas
  - numpy
  - scikit-learn
  - seaborn
  - matplotlib
- **Streamlit** for deploying the ML model
- **Power BI** for data visualization
- **Jupyter Notebooks** for interactive coding

## Data Collection and Storage
1. **Collect Yelp data** from the Yelp Dataset Challenge or Yelp API.
2. **Store raw data** in Google Cloud Storage buckets.

## Exploratory Data Analysis (EDA)
1. **Load data into BigQuery** for efficient querying.
2. **Perform EDA** using Jupyter Notebooks:
    - Summary statistics
    - Data visualization
    - Identifying patterns and anomalies

## ETL Process
1. **Extract data** from Google Cloud Storage.
2. **Transform data** using pandas and BigQuery:
    - Data cleaning
    - Data normalization
    - Feature engineering
3. **Load transformed data** back into BigQuery.

## Machine Learning
1. **Select features and labels** from the transformed dataset.
2. **Split data** into training and test sets.
3. **Build and train ML models** using scikit-learn:
    - Linear regression
    - Classification models
    - Clustering
4. **Evaluate model performance** and fine-tune hyperparameters.
5. **Deploy models** using Google AI Platform.

## Deploying the ML Model on Streamlit
1. **Create the `app.py` file**:
    - Contains the Streamlit application code, which loads the ML model and provides an interactive interface.
    - Sample code:
    ```python
    import streamlit as st
    import pandas as pd
    from google.cloud import bigquery
    from sklearn.cluster import KMeans
    import numpy as np

    # Configuration for BigQuery client
    client = bigquery.Client()

    # Load data from BigQuery
    def load_data():
        query = """
        SELECT
            name,
            category,
            avg_rating,
            num_of_reviews,
            state,
            population
        FROM
            `instant-binder-447716-p6.yelp_google_data.processed_table`
        """
        df = client.query(query).to_dataframe()
        return df

    # Preprocess data
    def preprocess_data(df):
        df['category'] = df['category'].astype('category').cat.codes
        df.fillna(0, inplace=True)
        return df

    # Train K-Means model
    def train_model(df, n_clusters=5):
        features = df[['avg_rating', 'num_of_reviews', 'category']]
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(features)
        return df, kmeans

    # Get recommendations
    def recommend(df, business_name):
        cluster = df[df['name'] == business_name]['cluster'].values[0]
        recommendations = df[df['cluster'] == cluster].sort_values(by='avg_rating', ascending=False)
        return recommendations[['name', 'category', 'avg_rating']].head(5)

    # Streamlit app
    st.title("Business Recommendations")

    # Load and preprocess data
    df = load_data()
    df = preprocess_data(df)

    # Train K-Means model
    df, model = train_model(df)

    # User interface for recommendations
    business_name = st.text_input("Business name", "Sample Business Name")
    if st.button("Get recommendations"):
        try:
            recommendations = recommend(df, business_name)
            st.write("Recommendations for the business:", business_name)
            st.write(recommendations)
        except IndexError:
            st.write("Business not found in data.")

    # Information about the cluster
    if st.button("Show cluster information"):
        try:
            cluster = df[df['name'] == business_name]['cluster'].values[0]
            st.write(f"The business '{business_name}' belongs to cluster {cluster}.")
            st.write(f"Number of businesses in the cluster: {len(df[df['cluster'] == cluster])}")
        except IndexError:
            st.write("Business not found in data.")
    ```

2. **Create the `requirements.txt` file**:
    - Lists all the dependencies required for the project.
    - Sample content:
    ```plaintext
    streamlit
    pandas
    google-cloud-bigquery
    scikit-learn
    numpy
    db-dtypes
    google-cloud-storage
    ```

3. **Create the `Dockerfile`**:
    - Used to containerize the Streamlit application.
    - Sample content:
    ```dockerfile
    # Use a base image with Python
    FROM python:3.9-slim

    # Set the working directory
    WORKDIR /app

    # Copy the necessary files
    COPY requirements.txt requirements.txt
    COPY app.py app.py

    # Install the dependencies
    RUN pip install -r requirements.txt

    # Expose the port on which the Streamlit app will run
    EXPOSE 8080

    # Command to run Streamlit
    CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
    ```

4. **Build and Deploy the Docker Image**:
    - Build the Docker image using Cloud Build:
    ```sh
    gcloud builds submit --tag gcr.io/instant-binder-447716-p6/streamlit-app
    ```
    - Deploy the Docker image to Cloud Run:
    ```sh
    gcloud run deploy streamlit-app --image gcr.io/instant-binder-447716-p6/streamlit-app --platform managed --region us-central1 --allow-unauthenticated --timeout 300
    ```

## Power BI Dashboard
1. **Connect Power BI** to BigQuery.
2. **Create interactive visualizations** and reports.
3. **Present insights and recommendations** on the best city to open the new restaurant, backed by data analysis.

## Contributors
- **Santiago Quiceno** - Data Scientist / Cloud Architect
- **Alfredo Sierra** - Data Engineer
- **Jhon Carrillo** - Data Scientist

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

