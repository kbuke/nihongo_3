from sqlalchemy_serializer import SerializerMixin
from config import db 
from datetime import time, datetime
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

class BusinessHoursModel(db.Model, SerializerMixin):
    __tablename__ = "business_hours"

    id = db.Column(db.Integer, primary_key=True)

    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("BusinessModel", back_populates="hours")
    opening_time = db.Column(db.Time, nullable = False)
    closing_time = db.Column(db.Time, nullable = False)
    closes_next_day = db.Column(db.Boolean, nullable = False)

    applies_to = db.Column(db.String, nullable = False)
    
    # validate applies_to
    @validates("business_id", "applies_to")
    def validate_business_info(self, key, value):
        if key == "applies_to":
            # Look at making validations for if the business has
                # same operating hours every day
                # same operating hours every week day
                # same operating hours every weekend 
            allowed_values = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if value not in allowed_values:
                raise ValueError(f"{value} is not a day of the week.")
            
        business_id = value if key == "business_id" else self.business_id
        applies_to = value if key == "applies_to" else self.applies_to

        if business_id is not None and applies_to is not None:
            existing = BusinessHoursModel.query.filter_by(
                business_id=business_id,
                applies_to=applies_to
            ).first()
            if existing and existing.id != self.id:
                raise ValueError(f"Business {business_id} already has hours defined for {applies_to}")
        return value

    
    # validate businesses times
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
        



