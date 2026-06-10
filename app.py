from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from models import db, Service, ServiceStatus

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    page_title = "Home Page"
    services = Service.query.order_by(Service.id).all()

    return render_template(
        "index.html",
        page_title=page_title,
        services=services
    )

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        services = Service.query.all()

        for service in services:
            new_status_id = request.form.get(f"status_{service.id}")

            if new_status_id:
                service.status_id = int(new_status_id)

        db.session.commit()

        return redirect(url_for("admin"))

    services = Service.query.order_by(Service.id).all()
    service_statuses = ServiceStatus.query.order_by(ServiceStatus.id).all()

    return render_template(
        "admin.html",
        page_title="Admin Page",
        services=services,
        service_statuses=service_statuses
    )


if __name__ == "__main__":
    app.run(debug=True)