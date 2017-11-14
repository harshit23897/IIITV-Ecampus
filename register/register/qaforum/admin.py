from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import (QaAnswer, QaAnswerComment, QaQuestion,
                       QaQuestionComment)

admin.site.register(QaQuestion)
admin.site.register(QaAnswer, MarkdownModelAdmin)
admin.site.register(QaAnswerComment)
admin.site.register(QaQuestionComment)
