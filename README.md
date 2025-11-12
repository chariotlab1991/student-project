# Machine Learning Project: Student Dropout & Mastery Prediction

A comprehensive educational project demonstrating end-to-end machine learning workflows for predicting student outcomes in an EdTech context. This project is designed for students to learn practical ML concepts including data generation, feature engineering, model training with multiple frameworks, and deployment considerations.

## Project Overview

This project predicts two key student outcomes:
- **Dropout Prediction**: Binary classification to identify students at risk of dropping out
- **Mastery Prediction**: Regression to predict final mastery percentage

## Learning Objectives

By working through this project, you will learn:

1. **Data Engineering**
   - Generate synthetic educational data
   - Feature engineering with pandas
   - Data aggregation using Apache Spark
   - Working with multiple data sources (students, courses, events, outcomes)

2. **Machine Learning Frameworks**
   - Scikit-learn for traditional ML
   - TensorFlow/Keras for deep learning
   - PyTorch for neural networks

3. **Model Development**
   - Binary classification (dropout prediction)
   - Regression (mastery prediction)
   - Feature scaling and preprocessing
   - Train-test splitting with stratification
   - Model evaluation and metrics

4. **Real-world ML Pipeline**
   - Data preprocessing and cleaning
   - Feature extraction from raw events
   - Model training and evaluation
   - Model persistence and artifact management

## Project Structure

```
machine-learnin-project/
│
├── data/                      # Dataset directory
│   ├── students.csv          # Student demographics and device info
│   ├── courses.csv           # Course catalog with difficulty levels
│   ├── enrollments.csv       # Student-course enrollment records
│   ├── events.csv            # Raw interaction events (videos, quizzes)
│   ├── outcomes.csv          # Final outcomes (mastery %, dropout status)
│   ├── agg_events.csv        # Aggregated event features
│   ├── features_dropout.npz  # Engineered features for dropout model
│   └── features_mastery.npz  # Engineered features for mastery model
│
├── notebooks/                 # Jupyter notebooks for exploration
│   └── eda.ipynb             # Exploratory Data Analysis
│
├── scripts/                   # Utility scripts
│   └── generate_dummy_data.py # Generate synthetic dataset
│
├── src/                       # Source code for ML models
│   ├── build_features.py     # Feature engineering pipeline
│   ├── spark_aggregates.py   # Spark-based event aggregation
│   ├── train_dropout_keras.py    # Keras model for dropout
│   ├── train_dropout_torch.py    # PyTorch model for dropout
│   ├── train_mastery_sklearn.py  # Sklearn model for mastery
│   └── recommend_sklearn.py      # (Future) Course recommendation
│
├── artifacts/                 # Saved models (created during training)
│
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment tool (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd machine-learnin-project
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # On Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: The `requirements.txt` file needs to include packages like:
   - pandas
   - numpy
   - scikit-learn
   - tensorflow (or tensorflow-macos for Apple Silicon)
   - torch
   - pyspark
   - jupyter
   - matplotlib
   - seaborn

### Usage

#### Step 1: Generate Synthetic Data

Create the sample EdTech dataset:

```bash
python scripts/generate_dummy_data.py
```

This generates 300 students, 8 courses, and simulated learning events in the `data/` directory.

#### Step 2: Explore the Data

Launch Jupyter notebook for exploratory data analysis:

```bash
jupyter notebook notebooks/eda.ipynb
```

#### Step 3: Aggregate Events (Optional Spark Step)

Compute aggregate features from raw events:

```bash
python src/spark_aggregates.py
```

#### Step 4: Build Features

Create engineered feature matrices for ML models:

```bash
python src/build_features.py
```

This script:
- Merges multiple data sources
- Creates numerical and categorical features
- Generates two feature sets: `features_dropout.npz` and `features_mastery.npz`

#### Step 5: Train Models

Train different models for dropout prediction:

**Keras/TensorFlow Model:**
```bash
python src/train_dropout_keras.py
```

**PyTorch Model:**
```bash
python src/train_dropout_torch.py
```

**Scikit-learn Model (for mastery prediction):**
```bash
python src/train_mastery_sklearn.py
```

Models are saved in the `artifacts/` directory.

## Dataset Description

### Students (`students.csv`)
- **id**: Unique student identifier
- **age**: Student age (18-55)
- **locale**: Language/region (e.g., en_US, hi_IN)
- **device_type**: Device used (mobile, desktop, tablet)

### Courses (`courses.csv`)
- **id**: Course identifier
- **subject**: Course topic (Python, ML, Data Science, etc.)
- **level**: Difficulty (beginner, intermediate, advanced)
- **est_hours**: Estimated completion time

### Events (`events.csv`)
- **student_id**: Student identifier
- **course_id**: Course identifier
- **ts**: Timestamp of the event
- **event_type**: Type of interaction (video_watch, quiz_submit)
- **seconds_spent**: Duration of engagement
- **score_delta**: Points gained (for quizzes)

### Outcomes (`outcomes.csv`)
- **student_id**: Student identifier
- **course_id**: Course identifier
- **final_mastery_pct**: Final mastery score (0-100)
- **dropped**: Binary indicator (1 = dropped, 0 = completed)

## Features Used in Models

The feature engineering pipeline creates:

**Numerical Features:**
- age
- est_hours (estimated course hours)
- secs_total (total time spent)
- active_days (days with activity)
- avg_quiz_delta (average quiz score gain)
- quiz_count (number of quizzes taken)

**Categorical Features (one-hot encoded):**
- locale
- device_type
- subject
- level
- cohort

## Model Architecture Examples

### Dropout Prediction (Keras)
- Input layer: number of features
- Dense layer: 128 units, ReLU activation
- Dropout: 0.3
- Dense layer: 64 units, ReLU activation
- Output layer: 1 unit, sigmoid activation (binary classification)

### Mastery Prediction (Scikit-learn)
- Random Forest Regressor
- Standardized features
- Mean Absolute Error (MAE) evaluation

## Extending the Project

Here are ideas for students to extend this project:

1. **Hyperparameter Tuning**: Use GridSearchCV or RandomizedSearchCV
2. **Feature Selection**: Implement feature importance analysis
3. **Additional Models**: Try XGBoost, LightGBM, or neural networks
4. **Cross-validation**: Implement k-fold cross-validation
5. **Interpretability**: Add SHAP or LIME for model explanations
6. **Recommendation System**: Complete the `recommend_sklearn.py` module
7. **Web Interface**: Build a Flask/FastAPI app to serve predictions
8. **MLOps**: Add experiment tracking with MLflow or Weights & Biases

## Common Issues

### Issue: Module not found
**Solution**: Ensure virtual environment is activated and all dependencies are installed.

### Issue: Data files missing
**Solution**: Run `python scripts/generate_dummy_data.py` first.

### Issue: Spark errors
**Solution**: Ensure Java is installed for PySpark (Java 8 or 11 required).

## Contributing

This is an educational project. Feel free to:
- Fork the repository
- Add new features or models
- Improve documentation
- Submit pull requests

## Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

## License

This project is intended for educational purposes.

## Acknowledgments

Created as a learning resource for students studying machine learning and data science. The dataset is synthetically generated for educational use.

---

**Happy Learning!** If you have questions or suggestions, please open an issue on GitHub.
