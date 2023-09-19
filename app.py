from flask import Flask, request, render_template, jsonify
import pickle
import os

app = Flask(__name__)

# Check if a file with saved observations exists. 
# If it does, we load these observations to start with, simulating offline data storage.
if os.path.exists("observations.pkl"):
    with open("observations.pkl", "rb") as f:
        observations = pickle.load(f)
else:
    # If there are no previous observations saved, we start with an empty list.
    observations = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form once the form is submitted.
        
        # Extract the filename of the uploaded photo for simplicity.
        # In a real-world scenario, we'd save the photo to a storage system and record its path or URL.
        photo_name = request.files['photo'].filename
        
        # Assembling all data into a dictionary.
        data = {
            'photo': photo_name,
            'date_time': request.form['date_time'],
            'landscape_position': request.form['landscape_position'],
            'vegetation_type': request.form['vegetation_type'],
            'burn_severity': request.form['burn_severity'],
            'ground_layer_recovery': request.form['ground_layer_recovery'],
            # ... Other fields can be added in a similar way ...
        }

        # Simulate saving the data to a local cache when there's no internet connection.
        # This is done by appending the data to our observations list and then pickling (serializing) the list to a file.
        observations.append(data)
        with open("observations.pkl", "wb") as f:
            pickle.dump(observations, f)
        
        # After saving, send a success message to the user.
        return jsonify({'status': 'success', 'message': 'Data saved successfully!'}), 200

    # If the method is GET, display the data collection form to the user.
    return render_template('data_collection.html')

@app.route('/sync', methods=['GET'])
def sync():
    # This route simulates the act of syncing data with a backend when online.
    # For demonstration purposes, we're just fetching data from our local cache.
    return jsonify(observations)

if __name__ == "__main__":
    # Run the Flask application.
    app.run(debug=True)

# To run the app, run the following command in the terminal:
# python3 app.py
