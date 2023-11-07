from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)

@app.route('/analisis_geoespacial', methods=['GET'])
def analisis_geoespacial():
    # Crear un conjunto de datos ficticio
    np.random.seed(42)
    n_samples = 1000
    data = pd.DataFrame({
        'Latitud': np.random.uniform(37.5, 38, n_samples),
        'Longitud': np.random.uniform(-122.5, -122, n_samples),
        'Denuncias': np.random.randint(0, 50, n_samples),
        'Homicidios': np.random.randint(0, 10, n_samples)
    })

    # Utilizar KMeans para agrupar áreas con densidad similar de denuncias y homicidios
    X = data[['Latitud', 'Longitud']]
    kmeans = KMeans(n_clusters=3, random_state=42)
    data['Cluster'] = kmeans.fit_predict(X)

    # Convertir resultados a formato JSON
    results = {
        'denuncias': data['Denuncias'].tolist(),
        'homicidios': data['Homicidios'].tolist(),
        'clusters': data['Cluster'].tolist()
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
