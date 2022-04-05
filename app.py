import os
from web import create_app
from flask import send_from_directory
app = create_app()

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
    
if __name__ == "__app__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))

#if __name__ == '__app__':
#    app.run(debug=True)
