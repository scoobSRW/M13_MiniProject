from flask_swagger_ui import get_swaggerui_blueprint

# Define Swagger variables
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/static/swagger.yaml"  # Path to the Swagger YAML file

# Create the blueprint
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Your API's Name"}
)
