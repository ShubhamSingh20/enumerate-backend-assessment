import enum
from typing import List
from flask_expects_json import ValidationError

from app import db
from app.models.mixin.serializer import Serializer
from app.models.response import SelectedOptionResponse, TextResponse

# For now schema will support mainly 3 types of question
# 1. Which only require text response
# 2. Single Option Selected response
# 3. Multiple option to be selected


class QuestionTypeEnum(str, enum.Enum):
    TEXT = "text"
    SINGLE_SELECT = "single_select"
    MULTIPLE_SELECT = "mutliple_select"


class Question(db.Model, Serializer):
    id = db.Column("id", db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("survey.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(
        db.Enum(QuestionTypeEnum), nullable=False, default=QuestionTypeEnum.TEXT
    )

    options = db.relationship("QuestionOption", lazy=True)

    def __init__(self, survey_id, text, type) -> None:
        self.survey_id = survey_id
        self.text = text
        self.type = type

    def serialize(self):
        serialized = super().serialize()
        serialized["options"] = QuestionOption.serialize_list(self.options)
        return serialized

    def handle_text_response(self, text: str, **kwargs):
        if text is None or not text.strip():
            raise ValidationError(
                f"'text' cannot be null or empty for question id: f{self.id}"
            )

        db.session.add(TextResponse(text=text, **kwargs))
        db.session.commit()

    def handle_select_response(self, selected_options: List[int], **kwargs):
        if len(selected_options) == 0:
            raise ValidationError(
                f"'selected_option_id' cannot be empty for question id: f{self.id}"
            )

        # ensure only one option is selected
        if self.type == QuestionTypeEnum.SINGLE_SELECT:
            selected_options = [selected_options[0]]

        selected_option_response = []
        for selected_id in selected_options:
            resp = SelectedOptionResponse(selected_option_id=selected_id, **kwargs)
            selected_option_response.append(resp)

        db.session.add_all(selected_option_response)
        db.session.commit()

    def submit_user_response(self, data, **kwargs):
        if self.type == QuestionTypeEnum.TEXT:
            self.handle_text_response(text=data["text"], question_id=self.id, **kwargs)
        else:
            self.handle_select_response(
                selected_options=data["selected_option_id"], question_id=self.id, **kwargs
            )


class QuestionOption(db.Model, Serializer):
    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    def __init__(self, text, question_id) -> None:
        self.text = text
        self.question_id = question_id
