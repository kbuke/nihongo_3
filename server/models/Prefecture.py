from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db 

from info.prefectures import japanese_prefectures

class PrefectureModel(db.Model, SerializerMixin):
    __tablename__ = "prefectures"

    id = db.Column(db.Integer, primary_key=True)
    prefecture_name = db.Column(db.String, nullable=False, unique=True)
    kanji = db.Column(db.String)
    prefecture_img = db.Column(db.String)
    prefecture_intro = db.Column(db.String)

    @validates("prefecture_name")
    def validate_name(self, key, value):
        prefecture = value if key == "prefecture_name" else self.prefecture_name

        if prefecture in japanese_prefectures:
            exisiting = PrefectureModel.query.filter(PrefectureModel.prefecture_name == prefecture).first()
            if exisiting and exisiting.id != self.id:
                raise ValueError(f"Prefecture {value} is already registered on the app.")
            return value 
        else:
            raise ValueError(f"{prefecture} is not a Japanese Prefecture.")
        
    __table_args__ = (
        db.UniqueConstraint("prefecture_name", name="unique_prefecture_name"),
    )


