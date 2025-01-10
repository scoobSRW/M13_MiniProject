from flask import send_from_directory
from app import create_app
from config import DevelopmentConfig
from app.blueprints.swagger import swagger_blueprint

# Create the Flask app
app = create_app(DevelopmentConfig)

# Add a route to serve static files only once
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Run the app
if __name__ == '__main__':
    app.run()
