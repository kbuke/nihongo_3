# This model is created as businesses will have certain days where their hours are not usual
# Public holidays are the main example
# Can also be used for days the business is open for longer such as events

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db

from datetime import date, time, datetime

class BusinessHourExceptionsModel(db.Model, SerializerMixin):
    __tablename__ ="business_hour_exceptions"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable = False)
    is_closed = db.Column(db.Boolean, nullable = False)

    # Business times
    opening_time = db.Column(db.Time, nullable = True)
    closing_time = db.Column(db.Time, nullable = True)
    closes_next_day = db.Column(db.Boolean, nullable = True)

    # Define relationship
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("BusinessModel", back_populates="hour_exceptions")

    # Add validation
        # ensure date format is correct
    @validates("date", "business_id")
    def validate_exception_date(self, key, value):
        specific_date = value if key == "date" else self.date 
        business_id = value if key == "business_id" else self.business_id

        if key in ("date"):
            if isinstance(value, date):
                return value
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                raise ValueError("Date must be in date format YYYY-MM-DD")
            
        if business_id is not None and specific_date is not None:
            existing = BusinessHourExceptionsModel.query.filter_by(
                business_id = business_id,
                date = specific_date
            ).first()
            if existing and existing.id != self.id:
                raise ValueError(f"Business {business_id} already has hours set for {specific_date}")
        return value

        # if is_closed is true then Business Time variables do not need values
        # if is_closed is false then Business Times will need values with following logic
            # if closes_next_day is true:   
                # opening_time must be set after closing_time ie (10:00 - 02:00)
            # if it is false:
                # closing_time must not be set to before opening_time
    @validates("is_closed", "opening_time", "closing_time", "closes_next_day")
    def validate_operating_hours(self, key, value):
        closed = value if key == "is_closed" else self.is_closed
        opening_time = value if key == "opening_time" else self.opening_time
        closing_time = value if key == "closing_time" else self.closing_time
        closes_next_day = value if key == "closes_next_day" else self.closes_next_day

        if closed is True:
            # logic for if the business is closed that day
            if opening_time is not None or closing_time is not None or closes_next_day is not None:
                raise ValueError("If the business is closed we do not need to input operating hours.")
            
        elif closed is False:

            if key in ("opening_time", "closing_time"):
                if isinstance(value, time):
                    return value 
                try:
                    return datetime.strptime(value, "%H:%M").time()
                except (ValueError, TypeError):
                    raise ValueError("Time must be in time format")
                
            elif key in ("is_closed", "closes_next_day"):
                if not isinstance(value, bool):
                    raise ValueError(f"{key} must be either True or False")
                return value
                
            # logic for if the business is open that day
            if closes_next_day is not None and opening_time is not None and closing_time is not None:
                if closes_next_day:
                    if not (opening_time > closing_time):
                        raise ValueError("When a business closes the day after opening it's closing time must be set before opening time.")
                else:
                    if not (opening_time < closing_time):
                        raise ValueError("When a business closes the same day, it's closing hour can not be before the opening hour.")
                    
        else:
            raise ValueError("is_closed must be explicitly true or false")

    __table_args__ = (
        db.UniqueConstraint("business_id", "date", name="unique_business_date"),
    )


        
