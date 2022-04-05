from web import create_app
from flask import send_from_directory
app = create_app()

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

if __name__ == '__app__':
    app.run(debug=True)
