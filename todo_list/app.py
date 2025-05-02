from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from routes.task_routes import TaskRoutes
from database import Database
from routes.auth_routes import AuthRoutes


class App:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.config['JWT_SECRET_KEY'] = '9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8'
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
        self.jwt = JWTManager(self.app)

        self.db = Database()

        self.auth_routes = AuthRoutes(self.app, self.db)
        self.task_routes = TaskRoutes(self.app, self.db)

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    app = App()
    app.run()
