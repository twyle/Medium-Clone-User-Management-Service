from ..extensions import db, ma
from datetime import datetime


class Suspend(db.Model):
    """The Suspend Model.""" 

    __tablename__ = 'suspend'
    id: int = db.Column(db.Integer, primary_key=True)
    admin_id: int = db.Column(db.Integer, db.ForeignKey('admins.id'))
    author_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    reason: str = db.Column(db.Text, nullable=False)
    date_suspended: datetime = db.Column(db.DateTime, default=datetime.utcnow)


class SuspendSchema(ma.Schema):
    """Show all the suspend information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "admin_id",
            "author_id",
            "reason",
            "date_suspended",
        )

suspend_schema = SuspendSchema()
suspends_schema = SuspendSchema(many=True)