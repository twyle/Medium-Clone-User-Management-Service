from ..extensions import db, ma
from datetime import datetime


class Report(db.Model):
    """The Report Model."""

    __tablename__ = 'reports'
    id: int = db.Column(db.Integer, primary_key=True)
    reporter_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    reportee_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    reason: str = db.Column(db.Text, nullable=False)
    date_reported: datetime = db.Column(db.DateTime, default=datetime.utcnow)


class ReportSchema(ma.Schema):
    """Show all the report information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "reporter_id",
            "reportee_id",
            "reason",
            "date_reported",
        )

report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)