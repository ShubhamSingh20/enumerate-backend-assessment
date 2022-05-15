from app import db
from app.models import *
from app.models.survey import Survey
from app.models.question import Question, QuestionOption, QuestionTypeEnum


def seed(db):
    db.create_all()
    db.session.commit()

    survey = Survey(name="Initial Survey")

    db.session.add(survey)
    db.session.commit()
    db.session.refresh(survey)

    # Create a text question
    db.session.add(Question(survey_id=survey.id, text=f"Text Question", type=QuestionTypeEnum.TEXT))

    # Create a single select question
    question = Question(survey_id=survey.id, text=f"Single Select", type=QuestionTypeEnum.SINGLE_SELECT)
    
    db.session.add(question)
    db.session.commit()
    db.session.refresh(question)

    db.session.add_all([
        QuestionOption(question_id=question.id, text='Single Select Option - 1'),
        QuestionOption(question_id=question.id, text='Single Select Option - 2'),
        QuestionOption(question_id=question.id, text='Single Select Option - 3')
    ])

    # Create a multi select question
    question = Question(survey_id=survey.id, text=f"Mutli Select Question", type=QuestionTypeEnum.MULTIPLE_SELECT)

    db.session.add(question)
    db.session.commit()
    db.session.refresh(question)

    db.session.add_all([
        QuestionOption(question_id=question.id, text='Single Multi Option - 1'),
        QuestionOption(question_id=question.id, text='Single Multi Option - 2'),
        QuestionOption(question_id=question.id, text='Single Multi Option - 3')
    ])

    db.session.commit()

if __name__ == '__main__':
    seed(db=db)
