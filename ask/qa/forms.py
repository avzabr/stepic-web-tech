from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title.strip():
            raise forms.ValidationError('title text is wrong', code=12)
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text.strip():
            raise forms.ValidationError('text text is wrong', code=12)
        return text

    def save(self):
        u, _ = User.objects.get_or_create(first_name='Unknown', last_name='Unknown')
        q = Question(author=u, **self.cleaned_data)
        q.save()
        return q


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput())

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text.strip():
            raise forms.ValidationError('text text is wrong', code=12)
        return text

    def save(self):
        u, _ = User.objects.get_or_create(first_name='Unknown', last_name='Unknown')
        q = get_object_or_404(Question, id=self.cleaned_data['question'])
        a = Answer(author=u, question=q, text=self.cleaned_data['text'])
        a.save()
        return a
