from flask import render_template
import config

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
   return render_template("home.html")

# Use ssl_context to run API over HTTPS
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, ssl_context='adhoc')