from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 1. Web Page Route (Flask Template)
@app.route('/')
def home():
    # Renders the index.html file from the templates/ folder
    return render_template('index.html', title="Home Page", message="Welcome to my Flask App!")

# 2. REST API Route
@app.route('/api/data', methods=['GET'])
def get_data():
    # Returns data in JSON format
    sample_data = {
        "status": "success",
        "message": "This is data from your REST API.",
        "items": [1, 2, 3, 4]
    }
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
