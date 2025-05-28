from flask import Flask, jsonify
from controllers.upload_controller import upload_bp
from models.resume import Resume

def create_app():
    app = Flask(__name__)

    app.register_blueprint(upload_bp)

    @app.route("/", methods=["GET"])
    def empty_resume():
        empty = Resume()
        return jsonify(empty.get())
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


