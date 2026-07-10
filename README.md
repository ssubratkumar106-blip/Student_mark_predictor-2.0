# Student Marks Prediction Using Machine Learning

Mini AI/ML project that predicts student marks from study hours using **Linear Regression**.

## Technologies
- Python
- Pandas
- Scikit-learn
- Flask

## Project Structure
```
├── app.py
├── train_model.py
├── predict.py
├── data_handler.py
├── dataset/student_scores.csv
├── model/
├── templates/
└── static/
```

## How to Run

```bash
pip install -r requirements.txt
python train_model.py
python app.py
```

Open http://127.0.0.1:5000

## CLI Prediction
```bash
python predict.py 5.5
```

## Features
- Study hours input
- Marks prediction (text + chart)
- Dataset with Pandas
- Train/test ML workflow
- Beginner-friendly supervised learning
