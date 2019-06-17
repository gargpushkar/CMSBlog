from django import forms
from core.models import Vote, Movie
from django.contrib.auth import get_user_model


class VoteForm(forms.ModelForm):
    """Form definition for Vote."""

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput, queryset=get_user_model().objects.all(), disabled=True
        )

    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput, queryset=Movie.objects.all(), disabled=True
        )

    value = forms.ChoiceField(
        label = 'Vote',
        widget = forms.RadioSelect,
        choices=Vote.VALUE_CHOICES
    )

    class Meta:
        """Meta definition for Voteform."""

        model = Vote
        fields = ('value', 'user', 'movie')
