from flask import Flask, render_template
from parse_site import UscisInterface


app = Flask(__name__)
interface = UscisInterface()


@app.route("/<number>",  methods=['GET'])
def get_result(number):
    title, content = interface.check(receipt_number=number)
    return render_template('number_result.html',
                           title=title,
                           content=content,
                           id=number
                           )


@app.route("/")
@app.route("/index",  methods=['GET'])
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=8888)
