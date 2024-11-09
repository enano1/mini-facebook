from django import forms
from .models import Voter
from datetime import date

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        choices=[('', 'All')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False
    )
    min_date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, date.today().year + 1)), required=False
    )
    max_date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, date.today().year + 1)), required=False
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'All')] + [(score, score) for score in range(1, 6)], required=False
    )
    for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
        locals()[election] = forms.BooleanField(required=False, label=f"Voted in {election.replace('v', '').title()} Election")
