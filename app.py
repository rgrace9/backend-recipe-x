from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import git

# Initialize a new Git repository in the current directory
repo = git.Repo.init('.')

app = Flask(__name__)
CORS(app)
api = Api(app)

class Quotes(Resource):
    def get(self):
        return {
            'Beatles': {
        'quote': ["All you need is love.",
                  "Let it be."]
    }
        }

api.add_resource(Quotes, '/')

if __name__ == '__main__':
    app.run(debug=True)