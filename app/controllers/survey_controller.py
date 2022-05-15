from flask import jsonify, request
from typing import List
from flask_expects_json import ValidationError

from app import app
from app.helpers import validate_schema
from app.models.question import Question, QuestionTypeEnum
from app.models.survey import Survey
from app.models.user import User


@app.route("/list-surveys", methods=["GET"])
def list_survey():
    return jsonify(surveys=Survey.serialize_list(Survey.query.all()))


@app.route("/list-surveys/<survey_id>", methods=["GET"])
def get_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if survey is None:
        return jsonify(error="Not Found"), 404
    return jsonify(survey=survey.serialize()), 200


take_survey_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "responses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question_id": {"type": "number"},
                    "text": {"type": ["string", "null"]},
                    "selected_option_id": {"type": "array"},
                    "items": {"type": "number"},
                },
                "required": ["question_id", "selected_option_id", "text"],
            },
        },
    },
    "required": ["email", "responses"],
}


@app.route("/take-survey/<survey_id>", methods=["POST"])
@validate_schema(take_survey_schema)
def take_survey(survey_id):
    survey: Survey = Survey.query.get(survey_id)

    if survey is None:
        return jsonify(error="Not Found"), 404

    data = request.json
    responses, email = data["responses"], data["email"]

    survey_questions: List[Question] = survey.questions

    # validate user has answered all the responses
    user_answered_questions = set(map(lambda x: x["question_id"], responses))
    if len(survey_questions) != len(user_answered_questions):
        return jsonify(error="Need To Answer All the Questions"), 400

    try:
        user = User.get_or_create_by_email(email=email)
        for question in survey_questions:
            # For every question get the appropriate response from request data
            user_response = next(
                filter(lambda x: x["question_id"] == question.id, responses)
            )
            question.submit_user_response(user_response, user_id=user.id)
    except ValidationError as ex:
        return jsonify(error=ex.message), 400

    return jsonify(surveys="ok"), 201



create_survey_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "question_type": {"enum": ['text', 'single_select', 'multiple_select']},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["question_type",  "text"],
            },
        },
    },
    "required": ["name", "questions"],
}

@app.route("/survey/create", methods=["POST"])
@validate_schema(create_survey_schema)
def create_survey():
    data = request.json
    questions, name = data["questions"], data["name"]
    survey = Survey.create_survey_with_questions(name, questions)
    return jsonify(survey=survey.serialize()), 201



@app.route("/survey/<survey_id>/user/<user_id>", methods=["GET"])
def get_user_response(survey_id, user_id):
    user: User = User.query.get(user_id)

    if user is None:
        return jsonify(error="No Such User"), 404

    user_responses = [
        {
            "question_id": r.id,
            "text": r.text,
            "selected_option_id": r.selected_option_id,
        }
        for r in user.get_survey_response(survey_id)
    ]

    data = {"user_id": user_id, "survey_id": survey_id, "responses": user_responses}
    return jsonify(data=data), 200
