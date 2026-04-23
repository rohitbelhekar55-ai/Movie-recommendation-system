# Machine Learning Based Movie Recommendation System

This project is a web-based movie recommendation system and data analysis tool built using Python, Flask, and Machine Learning libraries. It uses content-based filtering for recommendations, regression models for rating predictions, and statistical methods for hypothesis testing.

## Table of Contents
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Machine Learning Models](#machine-learning-models)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Folder Structure](#folder-structure)

## Features

1. **Movie Recommendations:**
   - Provides personalized movie recommendations based on specified genres, ratings, and release years.
   - For searching by specific titles, it computes content-based similarity to suggest alike movies.
   - Ranks recommendations using an IMDB-style Weighted Rating formula.

2. **Rating Prediction:**
   - Predicts the possible average rating for a hypothetical or upcoming movie using machine learning regression.
   - Analyzes the influence of release year and genres to forecast the score.

3. **Hypothesis Testing:**
   - Conducts statistical hypothesis testing to find significant differences between categories of movies.
   - Compares average ratings of Old vs. New movies.
   - Investigates comparative rating differences between distinct genres (e.g., Action vs. Drama).

4. **Web UI:**
   - A minimalist, cohesive Flask frontend providing interfaces for inputting constraints and viewing dynamic model outputs seamlessly.

## Project Architecture

The core architecture follows a standard MVC pattern applied to a Flask web server, separating routing logic (`app.py`), UI views (`templates/`), and business/ML logic (`model/`):

- **Backend Framework:** Flask (Python)
- **Data Processing:** pandas, NumPy
- **Machine Learning / Statistics:** scikit-learn (TF-IDF, Linear Regression, Pipeline), SciPy (T-Tests)
- **Frontend UI:** HTML, CSS

## Machine Learning Models

The repository encapsulates three major mathematical / ML concepts within the `model/` directory:

### 1. Recommender Engine (`model/recommender.py`)
- **Content-Based Filtering:** Uses Scikit-Learn's `TfidfVectorizer` to convert genre strings into numerical term-frequency vectors. Then, it utilizes `linear_kernel` to compute Cosine Similarity between movie genre vectors.
- **IMDB Weighted Rating:** Uses the formula: `(v / (v+m)) * R + (m / (v+m)) * C` to penalize movies with very few votes, surfacing more popular/proven high-quality content.

### 2. Rating Predictor (`model/predictor.py`)
- **Ridge Regression:** Builds a `Pipeline` utilizing a `ColumnTransformer`. 
- Incorporates `StandardScaler` to normalize the numeric release `year` feature.
- Extracts text features utilizing `TfidfVectorizer` on movie genres.
- It fits a `Ridge(alpha=1.0)` model to find the best linear relationship predicting a movie's `vote_average` score.

### 3. Hypothesis Tester (`model/hypothesis.py`)
- Uses SciPy's `stats.ttest_ind` function to perform Welch's t-tests (which do not assume equal population variance).
- Validates significance (p-value, t-statistic thresholding) locally inside hypothesis domains.

## Installation and Setup

### Prerequisites
Make sure you have Python 3.7+ installed.

### Step 1: Clone or download the repository
Have the project folder on your local machine. Ensure both `movies.csv` and `ratings.csv` datasets are present in the project's root folder.

### Step 2: Install required packages
It is recommended to run this inside a virtual environment. Install dependencies via pip:
```bash
pip install flask pandas scikit-learn scipy
```

### Step 3: Run the Flask Web App
Start the app by running the main Python file:
```bash
python app.py
```
By default, the server will start in debug mode and listen on `http://127.0.0.1:5000/`.

## Usage
Navigate to `http://127.0.0.1:5000/` in your browser. Use the provided navigation bar to access the different Machine Learning interfaces:
- **Home/Recommend**: Submit queries to find custom movies.
- **Predict**: Interactively provide a launch Year and Genre to predict theoretical success.
- **Hypothesis**: Run hypothesis tests on historical IMDb-like datasets.

## Folder Structure
```
Ml based MRS/
│
├── .gitignore
├── app.py                   # Main Flask application and routing definitions
├── movies.csv               # Dataset: movies metadata
├── ratings.csv              # Dataset: individualized rating votes
│
├── model/                   # Core Data Science / ML implementations
│   ├── hypothesis.py        # Contains `HypothesisTester` class logic
│   ├── predictor.py         # Contains `RatingPredictor` regression pipeline
│   └── recommender.py       # Contains algorithms for `MovieRecommender`
│
├── static/                  # Static web assets
│   └── style.css            # Stylesheets
│
└── templates/               # Flask Jinja2 HTML templates
    ├── hypothesis.html
    ├── index.html
    ├── notfound.html
    └── predict.html
```
