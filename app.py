from flask import Flask, request, render_template
from nlp_backend import handle_query

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        user_input = request.form["query"]
        result = handle_query(user_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
