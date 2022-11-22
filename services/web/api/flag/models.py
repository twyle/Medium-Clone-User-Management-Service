from ..extensions import db, ma
from datetime import datetime


class Flag(db.Model):
    """The Report Model."""

    __tablename__ = 'flags'
    id: int = db.Column(db.Integer, primary_key=True)
    moderator_id: int = db.Column(db.Integer, db.ForeignKey('moderators.id'))
    author_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    reason: str = db.Column(db.Text, nullable=False)
    date_flagged: datetime = db.Column(db.DateTime, default=datetime.utcnow)

class FlagSchema(ma.Schema):
    """Show all the flag information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "moderator_id",
            "author_id",
            "reason",
            "date_flagged",
        )

flag_schema = FlagSchema()
flags_schema = FlagSchema(many=True)