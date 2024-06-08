from datetime import datetime

import pytz

from yacut import db

timezone = pytz.timezone('UTC')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=lambda: datetime.now(timezone))

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp.isoformat() if self.timestamp else None,
        )

    def from_dict(self, data):
        for field in ['original', 'short', 'timestamp']:
            if field in data:
                if field == 'timestamp' and isinstance(data[field], str):
                    data[field] = datetime.fromisoformat(data[field]
                                                         ).astimezone(timezone)
                setattr(self, field, data[field])
