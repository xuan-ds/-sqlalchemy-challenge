# 1. import Flask
from flask import Flask

# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "List all available api routes."


@app.route("/api/v1.0/precipitation")
def precipitation():


@app.route("/api/v1.0/tobs")
def tob():

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

