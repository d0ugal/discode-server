import wtforms

from discode_server.utils import highlight

choices = [
   ("DETECT_LANGUAGE", "Detect Language"),
   ("text", "Text Only")
] + highlight.get_lexer_names()


class NewPasteForm(wtforms.Form):
    contents = wtforms.TextAreaField("Contents", [
        wtforms.validators.Length(min=5),
    ])
    language = wtforms.SelectField("language", choices=choices,
                                   default=choices[0][0])


class CommentForm(wtforms.Form):
    contents = wtforms.TextAreaField("Contents", [
        wtforms.validators.Length(min=1),
    ])
    line = wtforms.HiddenField()
