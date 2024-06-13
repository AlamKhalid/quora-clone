from django import forms
from .models import Topic, Question, Answer


class CreateTopicForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'class': 'form-control form-control-lg'}), max_length=50, required=True)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Description', 'class': 'form-control form-control-lg'}), required=True)
    picture = forms.ImageField(required=True)

    class Meta:
        model = Topic
        fields = ['picture', 'title', 'description']


class CreateQuestionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Description', 'class': 'form-control form-control-lg'}), required=True)
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control form-control-lg'}), required=True)

    class Meta:
        model = Question
        fields = ['topic', 'description']


class CreateAnswerForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Description', 'class': 'form-control form-control-lg'}), required=True)

    class Meta:
        model = Answer
        fields = ['description']
