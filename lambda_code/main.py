from flask import Flask, render_template, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint 
from helper.email import send_email
import serverless_wsgi


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/this-website')
def this_website():
    return render_template('this_website.html')

@app.route('/googleea6f05e89766f111.html')
def google_search():
    return render_template('googleea6f05e89766f111.html')

SWAGGER_SPEC = {
    "swagger": "2.0",
    "info": {
        "title": "My Portfolio API",
        "description": "This is the API documentation for Lucas Gutknecht's portfolio website. "
                       "It showcases various API endpoints and their functionalities. "
                       "Explore the available endpoints to understand how they work.",
        "version": "1.0.0"
    },
    "basePath": "/", 
    "schemes": [
        "http",
        "https"
    ],
    "paths": {
        "/api/hello": {
            "get": {
                "summary": "A simple hello world API.",
                "description": "Returns a greeting message.",
                "responses": {
                    "200": {
                        "description": "Returns a greeting",
                        "examples": {
                            "application/json": { "message": "You just made a successful API call!" }
                        }
                    }
                },
                "tags": ["General"]
            }
        },
        "/api/send_portfolio_email": {
            "post": {
                "summary": "Sends a sample email to a specified recipient.",
                "description": "This demonstrates an API endpoint that triggers an email sending process.",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "recipient_email": {
                                    "type": "string",
                                    "format": "email",
                                    "description": "The email address to send the email to."
                                }
                            },
                            "required": ["recipient_email"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Email sent successfully.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": { "type": "string", "example": "Email successfully dispatched to recipient@example.com" }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid request or missing recipient email.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": { "type": "string", "example": "recipient_email is required in the request body." }
                            }
                        }
                    },
                    "500": {
                        "description": "Failed to send email.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": { "type": "string", "example": "Failed to send email." }
                            }
                        }
                    }
                },
                "tags": ["Email"]
            }
        }
    }
}

@app.route('/swagger.json')
def swagger_json():
    return jsonify(SWAGGER_SPEC)

SWAGGER_URL = '/apidocs' 
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Portfolio API Documentation"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="You just made a successful API call!")

@app.route('/api/send_portfolio_email', methods=['POST'])
def send_portfolio_email():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    recipient_email = data.get('recipient_email')

    if not recipient_email:
        return jsonify({"error": "recipient_email is required in the request body."}), 400

    if send_email(recipient_email):
        return jsonify(message=f"Email successfully dispatched to {recipient_email}"), 200
    else:
        return jsonify(error="Failed to send email."), 500


def lambda_handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)