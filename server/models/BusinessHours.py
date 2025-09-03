from sqlalchemy_serializer import SerializerMixin
from config import db 
from datetime import time, datetime
from sqlalchemy.orm import validates

class BusinessHoursModel(db.Model, SerializerMixin):
    __tablename__ = "business_hours"

    id = db.Column(db.Integer, primary_key=True)

    applies_to = db.Column(db.String, nullable = False)

    opening_time = db.Column(db.Time, nullable = False)
    closing_time = db.Column(db.Time, nullable = False)
    closes_next_day = db.Column(db.Boolean, nullable = False)

    @validates("opening_time", "closing_time", "closes_next_day")
    def validate_hours(self, key, value):
        if key in ("opening_time", "closing_time") and isinstance(value, str):
            try:
                value = datetime.strptime(value, "%H:%M").time()
            except ValueError:
                raise ValueError("Time must be in time format")
        
        opening = value if key == "opening_time" else self.opening_time
        closing = value if key == "closing_time" else self.closing_time
        next_day = value if key == "closes_next_day" else self.closes_next_day

        if opening is not None and closing is not None and next_day is not None:
            if next_day:
                if not (opening > closing):
                    raise ValueError("When a business is open till the next day, it's opening hours must be after it's closing hour.")
            
            else:
                if not (opening < closing):
                    raise ValueError("When a business closes the same day, it's closing hour can not be before the opening hour.")
        return value
        



