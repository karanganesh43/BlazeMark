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
            'species_name': request.form['species_name'],
            'bird_animal_calls': request.form.get('bird_animal_calls', None), # Some fields might be optional
            'flowering_plants_state': request.form.get('flowering_plants_state', None),
            'altitude': request.form.get('altitude', None),
            'barometric_pressure': request.form.get('barometric_pressure', None),
            'compass_direction': request.form.get('compass_direction', None),
            'accelerometer_data': request.form.get('accelerometer_data', None)
            # ... capture other fields in a similar way ...
        }

        # Simulate offline caching
        observations.append(data)
        with open("observations.pkl", "wb") as f:
            pickle.dump(observations, f)
        
        return jsonify({'status': 'success', 'message': 'Data saved locally!'}), 200

    return render_template('data_collection.html')

@app.route('/sync', methods=['GET'])
def sync():
    # Simulate syncing data with backend once online
     return render_template('data_collection.html', observations=observations)

if __name__ == "__main__":
    app.run(debug=True)

# Commands to run:
# pip install flask
# python3 app.py
# http://127.0.0.1:5000/