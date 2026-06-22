from flask import Flask, render_template, request
from crawler.crawler import crawl_page

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/crawl", methods=["POST"])
def crawl():

    url = request.form.get("url")

    result = crawl_page(url)

    return render_template(
        "results.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)