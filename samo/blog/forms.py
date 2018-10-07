# pylint: disable=no-member,line-too-long
"""
This module contains the definitions of the forms used by the blog blueprint.
"""
from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Regexp, DataRequired, Email


class PostForm(Form):
    """
    Defines a post form. Contains method to validate it.
    """
    title = StringField('Title:')
    content = TextAreaField('Content:')
    ptags = StringField('Tags',
                        validators=[Regexp(r'^[a-zA-Z0-9, ]*$', message="Tags can only contain letters and numbers")])

    def validate(self):
        """
        Validates the Post form contents.

        :return: True if Post Form is validated, False otherwise
        """
        if not Form.validate(self):
            return False

        stripped = [t.strip() for t in self.ptags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.ptags.data = ",".join(tagset)

        return True


class CommentForm(Form):
    """
    Defines a comment form.
    """
    name = StringField('Name', validators=[DataRequired("Please enter your name.")])
    email = EmailField('Email', validators=[DataRequired("Your e-mail adress is required to add a comment."),
                                            Email("Please enter a valid e-mail address.")])
    content = TextAreaField('Comment', validators=[DataRequired("Please enter your comment.")])

    def validate(self):
        if not Form.validate(self):
            return False
        return True


class SearchForm(Form):
    """
    Defines a search form
    """
    search = StringField('')
