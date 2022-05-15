from app import db


class SelectedOptionResponse(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    selected_option_id = db.Column(
        db.Integer, db.ForeignKey("question_option.id"), nullable=True, default=None
    )

    def __init__(self, question_id, user_id, selected_option_id) -> None:
        self.question_id = question_id
        self.user_id = user_id
        self.selected_option_id = selected_option_id


class TextResponse(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, question_id, text) -> None:
        self.user_id = user_id
        self.question_id = question_id
        self.text = text
