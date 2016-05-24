from django import forms
from django.shortcuts import get_object_or_404

from qa.models import Question, Answer, salt_and_hash, do_signup, do_login, Session


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

    def save(self, user):
        q = Question(author=user, **self.cleaned_data)
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

    def save(self, user):
        q = get_object_or_404(Question, id=self.cleaned_data['question'])
        a = Answer(author=user, question=q, text=self.cleaned_data['text'])
        a.save()
        return a


class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        return do_signup(username=username, password=salt_and_hash(password), email=email)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        return do_login(username=username, password=salt_and_hash(password))
