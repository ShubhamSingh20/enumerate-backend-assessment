### Intro
Basic Survey app
* Create survey with questions
* Support three types of question
  * Just Text Response
  * MCQ with one selection only
  * MCQ with mutliple selection
* above three can be used to cover other question types if needed
* Another User can take these survey and attempt all the questions

### Run Test
```bash
pytest test
```

### Create survey

```python
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
```

### Answer Survey
```python
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
```

### Check User Survey Response
```python
 {
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
```
