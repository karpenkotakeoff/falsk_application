from flasgger import Swagger
from flask import Flask
from api.resources import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)
swagger = Swagger(app)

if __name__ == "__main__":
    app.run(debug=True)
