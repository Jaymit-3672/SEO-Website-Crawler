from flask import Flask, render_template, request

# Import crawler
from crawler.crawler import crawl_website

# Import SEO audit engine
from crawler.seo_audit import audit_seo

app = Flask(__name__)


# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# Crawl Website
# ----------------------------
@app.route("/crawl", methods=["POST"])
def crawl():

    # Get URL from form
    url = request.form.get("url")

    # Validation
    if not url:
        return render_template(
            "results.html",
            results=[],
            audit={
                "total_pages": 0,
                "missing_titles": [],
                "missing_meta": [],
                "missing_h1": [],
                "duplicate_titles": [],
                "duplicate_meta": []
            }
        )

    # Crawl website
    results = crawl_website(
        start_url=url,
        max_pages=20
    )

    # Run SEO audit
    audit = audit_seo(results)

    # Send data to results page
    return render_template(
        "results.html",
        results=results,
        audit=audit
    )


# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == "__main__":
    app.run(
        debug=True
    )