from flask import Flask, request, render_template_string
import pandas as pd
import joblib

app = Flask(__name__)

# Load the necessary models and data once when the app starts
le = joblib.load("le.joblib")
loaded_model = joblib.load("voting_en.joblib")
expected_columns = pd.read_csv("columns.csv").iloc[:, 0].tolist()

# Dictionary to hold disease descriptions and cures
disease_info = {
    "RHB": {
        "description": "Rheumatic Heart Disease (RHD) is a condition in which the heart valves are damaged by rheumatic fever, a complication of untreated strep throat. Symptoms can include chest pain, shortness of breath, and fatigue. Long-term effects may lead to heart failure.",
        "cure": "Treatment may include medications like antibiotics, anti-inflammatory drugs, and in severe cases, surgery to repair or replace damaged heart valves."
    },
    "MED": {
        "description": "Medical Disease (MED) is a broad term that can refer to any number of conditions that affect the body's normal functioning. This term encompasses a wide range of health issues, and specific details would depend on the context of the diagnosis.",
        "cure": "Cures vary widely depending on the specific medical condition and should be discussed with a healthcare professional."
    },
    "EPD": {
        "description": "Epilepsy and Other Seizure Disorders (EPD) are neurological conditions characterized by recurrent seizures. These seizures are caused by sudden, excessive electrical discharges in the brain. Symptoms can vary widely, including convulsions, loss of consciousness, and unusual sensations.",
        "cure": "Management may include antiepileptic medications, lifestyle changes, and in some cases, surgery."
    },
    "JPA": {
        "description": "Juvenile Polymyositis or Juvenile Idiopathic Arthritis (JPA) are autoimmune diseases that cause inflammation in the muscles and joints of children. Symptoms may include muscle weakness, joint pain, and fatigue, impacting the child's ability to perform daily activities.",
        "cure": "Treatment often involves corticosteroids, immunosuppressive drugs, and physical therapy."
    },
    "MGL": {
        "description": "Megaloblastic Anemia (MGL) is a type of anemia characterized by the presence of large, abnormal red blood cells in the bone marrow. It is often caused by a deficiency of vitamin B12 or folate, leading to symptoms such as fatigue, weakness, and pale skin.",
        "cure": "Treatment typically involves vitamin B12 or folate supplementation, along with dietary changes."
    }
}

# HTML template for the upload form
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        .error {
            color: red;
            margin: 10px 0;
            text-align: center;
        }
    </style>
    <script>
        function validateFile() {
                    const fileInput = document.getElementById('file');
            const errorDiv = document.getElementById('error');
            errorDiv.innerHTML = ''; // Clear previous errors
            const file = fileInput.files[0];

            if (!file) {
                errorDiv.innerHTML = 'Please select a file.';
                return false;
            }
            if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
                errorDiv.innerHTML = 'Please upload a valid CSV file.';
                return false;
            }
            return true; // File is valid
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Upload CSV for Prediction</h1>
        <div id="error" class="error"></div>
        <form method="POST" enctype="multipart/form-data" onsubmit="return validateFile()">
            <div class="form-group">
                <label for="file">Choose CSV File</label>
                <input type="file" id="file" name="file" required>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
'''

# HTML template for displaying results
result_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .results {
            margin-top: 20px;
        }
        .results ul {
            list-style: none;
            padding: 0;
        }
        .results li {
            padding: 10px;
            background: #e9ecef;
            margin: 5px 0;
            border-radius: 4px;
        }
        .description, .cure {
            margin-top: 10px;
            padding: 10px;
            background: #f0f8ff;
            border-left: 4px solid #007bff;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            text-align: center;
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .disclaimer {
            margin-top: 20px;
            font-style: italic;
            color: #666;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prediction Results</h1>
        <div class="results">
            <h4>Predictions:</h4>
            <ul>
                {% for prediction in predictions %}
                    <li>{{ prediction }} 
                        <div class="description">{{ descriptions[prediction]['description'] }}</div>
                        <div class="cure">{{ descriptions[prediction]['cure'] }}</div>
                    </li>
                {% endfor %}
            </ul>
        </div>
        <div class="disclaimer">
            *This is not medical advice but an AI-Generated response, kindly consult Doctors for further advice.
        </div>
        <a href="/">Upload Another File</a>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        if file:
            try:
                # Read the uploaded CSV file
                train_df1 = pd.read_csv(file)

                # Prepare the data for prediction
                train_rem1 = train_df1.iloc[:, 1]
                train_rem1 = pd.DataFrame(train_rem1).T.reindex(columns=expected_columns)

                # Make predictions
                num_out = loaded_model.predict(train_rem1)
                test_class = le.inverse_transform(num_out.astype(int))

                # Create a dictionary of descriptions and cures for the predicted classes
                descriptions = {pred: disease_info.get(pred, {"description": "Description not available.", "cure": "Cure not available."}) for pred in test_class}

                return render_template_string(result_html, predictions=test_class, descriptions=descriptions)
            except Exception as e:
                return render_template_string(index_html, error=f"An error occurred: {str(e)}")

    return render_template_string(index_html)

if __name__ == '__main__':
    app.run(debug=True)