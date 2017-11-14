from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from register.qa.models import (Answer, AnswerComment, Question,
                       QuestionComment)

admin.site.register(Question)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
