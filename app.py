from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Load the pickled model (update the path as per your setup)
model_filename = 'LinearRegressionModel.pkl'  # Use the path to your actual model
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Define the home route to render the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the form data from the POST request
        price_per_unit = float(request.form['Price per Unit'])
        units_sold = float(request.form['Units Sold'])
        operating_margin = float(request.form['Operating Margin'])
        year = int(request.form['Year'])
        sales_method = int(request.form['Sales Method_Online'])

        # Adjust the sales method as per the new options (0, 1, 2)
        if sales_method == 2:
            sales_method_online = 1
            sales_method_outlet = 0
        elif sales_method == 1:
            sales_method_online = 0
            sales_method_outlet = 1
        else:
            sales_method_online = 0
            sales_method_outlet = 0

        # Create a DataFrame for the input data
        input_data = pd.DataFrame([[price_per_unit, units_sold, operating_margin, year, sales_method_online, sales_method_outlet]], 
                                  columns=['Price per Unit', 'Units Sold', 'Operating Margin', 'Year', 'Sales Method_Online', 'Sales Method_Outlet'])

        # Use the model to make predictions
        prediction = model.predict(input_data)

        # Round the prediction to 2 decimal places
        rounded_prediction = round(prediction[0], 2)

        # Return the prediction in the response
        return render_template('index.html', prediction=rounded_prediction)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
