from flask import Flask

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='')


@app.route('/rss.xml', methods=['GET'])
def send_js():
    return app.send_static_file('rss.xml')


if __name__ == "__main__":
    app.run()
