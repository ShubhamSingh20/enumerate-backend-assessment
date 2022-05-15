from typing import List
from app import db
from app.models.question import Question, QuestionOption
from .mixin.serializer import Serializer


class Survey(db.Model, Serializer):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    questions = db.relationship("Question", lazy=True)

    def __init__(self, name) -> None:
        self.name = name

    def serialize(self):
        serialized = super().serialize()
        serialized["questions"] = Question.serialize_list(self.questions)
        return serialized

    @staticmethod
    def create_survey_with_questions(name, questions: List):
        survey = Survey(name=name)

        db.session.add(survey)
        db.session.commit()
        db.session.refresh(survey)

        for question in questions:
            question_instance = Question(
                survey_id=survey.id,
                text=question["text"],
                type=question["question_type"],
            )

            db.session.add(question_instance)
            db.session.commit()
            db.session.refresh(question_instance)


            question_options = [
                QuestionOption(text=option_text, question_id=question_instance.id)
                for option_text in question.get("options", [])
            ]

            db.session.add_all(question_options)
            db.session.commit()

        return survey
