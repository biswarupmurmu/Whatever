"""
Run the Flask application.

This script creates and runs the Flask application using the create_app function from the ourapp package.

If this script is executed directly, it runs the Flask application with debug mode enabled.

Note:
    This script is typically executed to start the Flask application.

Example:
    python run.py

Attributes:
    app: The Flask application created using the create_app function.

"""
from ourapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
