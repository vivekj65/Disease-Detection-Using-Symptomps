import pandas as pd
from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier
import csv

app = Flask(__name__)

training = pd.read_csv('Data/Training.csv')

clf = DecisionTreeClassifier()
clf.fit(training.iloc[:, :-1], training['prognosis'])

severityDictionary = {}
description_list = {}
precautionDictionary = {}

def load_symptom_data():
    try:
        with open(r'C:\Users\vivek\OneDrive\Desktop\Python-Flask\MasterData\Symptom_severity.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) >= 2:
                    symptom, severity = row[0], int(row[1])
                    severityDictionary[symptom] = severity
    except FileNotFoundError:
        print("symptom_severity.csv not found.")

    try:
        with open(r'C:\Users\vivek\OneDrive\Desktop\Python-Flask\MasterData\symptom_Description.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) >= 2:
                    symptom, description = row[0], row[1]
                    description_list[symptom] = description
    except FileNotFoundError:
        print("symptom_Description.csv not found.")

    try:
        with open(r'C:\Users\vivek\OneDrive\Desktop\Python-Flask\MasterData\symptom_precaution.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) >= 5:
                    symptom, precaution1, precaution2, precaution3, precaution4 = row
                    precautionDictionary[symptom] = [precaution1, precaution2, precaution3, precaution4]
    except FileNotFoundError:
        print("symptom_precaution.csv not found.")

load_symptom_data()

@app.route('/')
def index():
    symptoms = ["Fever", "Cough", "Headache", "Fatigue", "Nausea", "Sore Throat", "Shortness of Breath", "Body Aches", "Loss of Taste or Smell"]
    return render_template('index.html', symptoms=symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        selected_symptoms = request.form.getlist('symptoms')
        
        input_vector = [1 if symptom in selected_symptoms else 0 for symptom in training.columns[:-1]]
        predicted_disease = clf.predict([input_vector])[0]
        description = description_list.get(predicted_disease, "Description not found")
        precautions = precautionDictionary.get(predicted_disease, [])

        return render_template('result.html', disease=predicted_disease, description=description, precautions=precautions)

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
