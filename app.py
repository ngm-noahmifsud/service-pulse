from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from models import db, Service, ServiceStatus, Incident, IncidentService

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    page_title = "Home Page"
    services = Service.query.order_by(Service.id).all()
    incidents = Incident.query.order_by(Incident.id).all()

    return render_template(
        "index.html",
        page_title=page_title,
        services=services,
        incidents=incidents
    )

@app.route("/admin")
def admin():
    services = Service.query.order_by(Service.id).all()
    service_statuses = ServiceStatus.query.order_by(ServiceStatus.id).all()
    incidents = Incident.query.order_by(Incident.id).all()

    return render_template(
        "admin.html",
        page_title="Admin Page",
        services=services,
        service_statuses=service_statuses,
        incidents=incidents
    )

@app.route("/admin/remove_incidents", methods=["POST"])
def remove_incidents():
    incident_ids = request.form.getlist("remove_incidents")

    for incident_id in incident_ids:
        incident = Incident.query.get(int(incident_id))

        if incident:
            db.session.delete(incident)

    db.session.commit()

    return redirect(url_for("admin"))

@app.route("/admin/update_status", methods=["POST"])
def update_status():
    services = Service.query.all()

    for service in services:
        new_status_id = request.form.get(f"status_{service.id}")

        if new_status_id:
            service.status_id = int(new_status_id)

    db.session.commit()

    return redirect(url_for("admin"))


@app.route("/admin/create_incident", methods=["POST"])
def create_incident():
    name = request.form.get("name")
    status_id = request.form.get("status_id")
    message = request.form.get("message")

    affected_service_ids = request.form.getlist("affected_services")

    incident = Incident(
        name=name,
        status_id=int(status_id),
        message=message
    )

    db.session.add(incident)
    db.session.flush()  # creates incident.id before commit

    for service_id in affected_service_ids:
        incident_service = IncidentService(
            incident_id=incident.id,
            service_id=int(service_id)
        )

        db.session.add(incident_service)

    db.session.commit()

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)