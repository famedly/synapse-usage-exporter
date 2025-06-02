"""WSGI module"""

from app import app

# WSGI servers expect an 'application' callable
application = app

if __name__ == "__main__":
    app.run()
