
![WhatsApp Image 2025-01-15 at 1 17 45 AM](https://github.com/user-attachments/assets/941f9a8e-09f0-4efe-a187-bca099eeeff7)

# Yelp Data Analysis Project

## Overview
This project involves the comprehensive analysis of Yelp data using Google Cloud. We will perform Exploratory Data Analysis (EDA), Extract, Transform, Load (ETL) processes, Machine Learning (ML) modeling, and create a Power BI dashboard. Our goal is to derive valuable insights and build predictive models to improve business decision-making.

## Table of Contents
- [Project Setup](#project-setup)
- [Technologies](#technologies)
- [Data Collection and Storage](#data-collection-and-storage)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [ETL Process](#etl-process)
- [Machine Learning](#machine-learning)
- [Power BI Dashboard](#power-bi-dashboard)
- [Contributors](#contributors)
- [License](#license)

## Project Setup
1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
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
  - AI Platform
- **Python**:
  - pandas
  - numpy
  - scikit-learn
  - seaborn
  - matplotlib
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

## Power BI Dashboard
1. **Connect Power BI** to BigQuery.
2. **Create interactive visualizations** and reports.
3. **Share insights** with stakeholders through the Power BI dashboard.

## Contributors
- **Your Name** - Project Lead
- **Collaborator Name** - Data Scientist
- **Collaborator Name** - ML Engineer

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

