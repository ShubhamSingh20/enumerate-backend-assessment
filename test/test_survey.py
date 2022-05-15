from app import app, db
from app.config import TEST_DB_URI
from app.models import *
from app.controllers import *
from test.fixture import seed
import pytest
import os


@pytest.fixture()
def flask_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DB_URI
    seed(db)
    yield app
    os.remove(TEST_DB_URI.replace("sqlite:///", ""))


def test_list_survey(flask_app):
    with app.test_client() as client:
        response = client.get("/list-surveys")
        assert response.status_code == 200


def test_create_survey(flask_app):
    with app.test_client() as client:
        response = client.post(
            "/survey/create",
            json={
                "email": "test@test.com",
                "name": "Test Survey",
                "questions": [
                    {"text": "Question text", "question_type": "text"},
                    {
                        "text": "Question single select",
                        "question_type": "single_select",
                        "options": ["first", "second", "third"],
                    },
                ],
            },
        )

        assert response.status_code == 201, response.json

def test_take_survey(flask_app):
    # RUN `python fixture.py`

    with app.test_client() as client:
        response = client.post(
            "/take-survey/1",
            json={
                "email": "test@test.com",
                "responses": [
                    {
                        "question_id": 1,
                        "text": "Text Answer - 1",
                        "selected_option_id": [3, 1],
                    },
                    {
                        "question_id": 2,
                        "text": None,
                        "selected_option_id": [2],
                    },
                    {
                        "question_id": 3,
                        "text": None,
                        "selected_option_id": [5, 6],
                    },
                ],
            },
        )

        assert response.status_code == 201, response.data

        expected_response = {
            "data": {
                "responses": [
                    {
                        "question_id": 1,
                        "selected_option_id": None,
                        "text": "Text Answer - 1",
                    },
                    {"question_id": 2, "selected_option_id": 2, "text": None},
                    {"question_id": 3, "selected_option_id": 5, "text": None},
                    {"question_id": 3, "selected_option_id": 6, "text": None},
                ],
                "survey_id": "1",
                "user_id": "1",
            }
        }

        response = client.get("/survey/1/user/1")
        assert expected_response == response.json, response.json
