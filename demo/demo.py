import random
import json
import pymapcluster as clust
from globalmaptiles import GlobalMercator
from flask import Flask
from flask import render_template
app = Flask(__name__)

# Bounds for data generation
bounds = {'lat': (46.057, 47.561),
          'lng': (7.13, 9.32)}
markers = [(random.uniform(*bounds['lat']), random.uniform(*bounds['lng']))
           for i in xrange(1000)]

mercator = GlobalMercator()
centers, clusters = clust.cluster_markers(mercator, markers, 8);
clust_markers = [markers[i] for i in centers]

@app.route("/")
def index():
    return render_template('index.html',
                           markers=json.dumps(markers),
                           clust_markers=json.dumps(clust_markers))

if __name__ == "__main__":
    app.run(debug=True)
