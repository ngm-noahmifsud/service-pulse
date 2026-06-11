from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ServiceStatus(db.Model):
    __tablename__ = "service_status"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("service_status.id"), nullable=False)

    status = db.relationship("ServiceStatus")

class IncidentService(db.Model):
    __tablename__ = "incident_service"

    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id", ondelete="CASCADE"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id", ondelete="CASCADE"), primary_key=True)


class Incident(db.Model):
    __tablename__ = "incident"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("service_status.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)

    status = db.relationship("ServiceStatus")

    affected_services = db.relationship(
        "Service",
        secondary="incident_service",
        backref="incidents"
    )