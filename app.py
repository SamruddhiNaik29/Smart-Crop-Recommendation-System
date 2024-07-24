from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle

# importing model
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

app = Flask(__name__)

# Placeholder user database
users = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]

# Placeholder feedback database
feedbacks = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate registration (you can add proper validation logic here)
        if any(user['username'] == username for user in users):
            return render_template('register.html', error='Username already exists')
        else:
            users.append({'username': username, 'password': password})
            return render_template('login.html', message='Registration successful. Please login.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_login(username, password):  # Change this line
            # Redirect to the 'predict' route upon successful login
            return redirect(url_for('predict'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html', error=None)


def check_login(username, password):
    # Placeholder login function
    return any(user['username'] == username and user['password'] == password for user in users)





@app.route('/predict', methods=['GET', 'POST'])
def predict():
    result = None  # Initialize result to None

    if request.method == 'POST':
        N = request.form['Nitrogen']
        P = request.form['Phosporus']
        K = request.form['Potassium']
        temp = request.form['Temperature']
        humidity = request.form['Humidity']
        ph = request.form['Ph']
        rainfall = request.form['Rainfall']

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
        return render_template('result.html', result=result)  # Redirect to result.html

    return render_template('predict.html', result=None)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Placeholder code for feedback submission
        feedback_text = request.form['feedback']
        feedbacks.append(feedback_text)
        return render_template('index.html', message='Feedback submitted successfully!')
    return render_template('feedback.html')


if __name__ == "__main__":
    app.run(debug=True)

