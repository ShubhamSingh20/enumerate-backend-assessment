from app import db
from app.models.question import Question
from app.models.response import TextResponse, SelectedOptionResponse

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.Text, nullable=False)

    db.UniqueConstraint(email)

    def get_survey_response(self, survey_id):
        return db.session.query(Question)\
            .with_entities(Question.id, TextResponse.text, SelectedOptionResponse.selected_option_id)\
            .outerjoin(TextResponse, 
                (TextResponse.question_id == Question.id) & 
                (Question.type == 'text') & 
                (TextResponse.user_id == self.id)) \
            .outerjoin(SelectedOptionResponse, 
                (SelectedOptionResponse.question_id == Question.id) & 
                (SelectedOptionResponse.user_id == self.id) & 
                ((Question.type == 'single_select') | (Question.type =='mutliple_select'))
            ).where(Question.survey_id == survey_id).all()

    @staticmethod
    def get_or_create_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        return user
