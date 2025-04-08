from flask import Flask, request, jsonify
import util
app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        "locations": util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():

    total_sqft = float(request.form["total_sqft"])
    bhk = int(request.form["number_bedrooms"])
    location = request.form["location"]
    bath = int(request.form["bath"])

    response = jsonify({
        "estimated_price": util.get_estimated_price(bath, bhk, total_sqft, location)
        
    })
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

if __name__ == "__main__":
    print("Starting python Flask Server for home price prediction")
    util.load_saved_artifacts()
    app.run()
