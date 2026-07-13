from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Placeholder for future ML model integration
    return "Prediction functionality will be implemented here."

if __name__ == '__main__':
    app.run(debug=True)
