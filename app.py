from flask import Flask, request, render_template, jsonify
import pickle
import os

app = Flask(__name__)

# Check if saved observations exist. If yes, load them, simulating offline data storage.
if os.path.exists("observations.pkl"):
    with open("observations.pkl", "rb") as f:
        observations = pickle.load(f)
else:
    observations = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'photo': request.files['photo'].filename,
            'datetime': request.form['datetime'],
            'landscape_position': request.form['landscape_position'],
            'vegetation_type': request.form['vegetation_type'],
            'development_stage': request.form['development_stage'],
            'burn_severity': request.form['burn_severity'],
            'ground_layer_recovery': request.form['ground_layer_recovery'],
            'shrub_layer_recovery': request.form['shrub_layer_recovery'],
            'sub_canopy_layer_recovery': request.form['sub_canopy_layer_recovery'],
            'tallest_tree_layer_recovery': request.form['tallest_tree_layer_recovery'],
            'species_name': request.form['species_name'],
            'bird_animal_calls': request.form.get('bird_animal_calls', None),
            'flowering_plants_state': request.form.get('flowering_plants_state', None),
            'altitude': request.form.get('altitude', None),
            'barometric_pressure': request.form.get('barometric_pressure', None),
            'compass_direction': request.form.get('compass_direction', None),
            'accelerometer_data': request.form.get('accelerometer_data', None)
        }

        # TODO: While the filename of the photo is captured in the data dictionary, the actual photo isn't saved. 
        # Consider saving the photo in a directory and storing the path to that file in the data dictionary.

        # Simulate offline caching
        observations.append(data)
        with open("observations.pkl", "wb") as f:
            pickle.dump(observations, f)
        
        # TODO: Instead of returning a JSON response, consider redirecting back to the form page with a success message.
        return jsonify({'status': 'success', 'message': 'Data saved locally!'}), 200

    return render_template('data_collection.html', observations=observations)

@app.route('/sync', methods=['GET'])
def sync():
    # TODO: Implement the actual synchronization operation to a backend once online.
    return render_template('data_collection.html', observations=observations)

if __name__ == "__main__":
    app.run(debug=True)

# TODO: For scalability and security, consider using a proper database or other storage mechanism instead of pickle.
# TODO: Add error handling for potential issues like missing fields, incorrect data formats, or storage errors.
# TODO: Be aware of potential security considerations when storing sensitive or personal data in plaintext pickles.

# Do not delete the following lines
# Commands to run:
# pip install flask
# python3 app.py
# http://127.0.0.1:5000/
