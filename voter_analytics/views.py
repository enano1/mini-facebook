from django.db.models import Count, Q
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .forms import VoterFilterForm
from .models import Voter
import plotly.graph_objs as go
import plotly



class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 50  

    def get_queryset(self):
        """Filter qs based on search criteria."""
        qs = super().get_queryset()

        # Add filters here
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        voted_in = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        if party_affiliation:
            qs = qs.filter(party_affiliation=party_affiliation)
        if min_dob:
            qs = qs.filter(date_of_birth__gte=min_dob)
        if max_dob:
            qs = qs.filter(date_of_birth__lte=max_dob)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        for field, value in voted_in.items():
            if value == 'on':
                qs = qs.filter(**{field: True})

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_options'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['year_range'] = range(1900, 2025)
        context['voter_score_range'] = range(1, 6)
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = self.get_object()

        participation_data = {
            'v20state': voter.v20state,
            'v21town': voter.v21town,
            'v21primary': voter.v21primary,
            'v22general': voter.v22general,
            'v23town': voter.v23town,
        }

        return context

class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    paginate_by = 100  

    def get_queryset(self):
        """Filter voters based on form data."""
        qs = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                qs = qs.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_date_of_birth']:
                qs = qs.filter(date_of_birth__gte=form.cleaned_data['min_date_of_birth'])
            if form.cleaned_data['max_date_of_birth']:
                qs = qs.filter(date_of_birth__lte=form.cleaned_data['max_date_of_birth'])
            if form.cleaned_data['voter_score']:
                qs = qs.filter(voter_score=form.cleaned_data['voter_score'])
            for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if self.request.GET.get(election):
                    qs = qs.filter(**{election: True})
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # yob dist
        yob_counts = voters.annotate(year_of_birth=ExtractYear('date_of_birth')).values('year_of_birth').annotate(count=Count('id')).order_by('year_of_birth')
        fig1 = go.Bar(x=[item['year_of_birth'] for item in yob_counts], y=[item['count'] for item in yob_counts])
        context['yob_chart'] = plotly.offline.plot({"data": [fig1], "layout": {"title": "Distribution of Voters by Year of Birth"}}, auto_open=False, output_type="div")

        # pie chart
        party_counts = voters.values('party_affiliation').annotate(count=Count('id'))
        fig2 = go.Figure(data=[go.Pie(labels=[item['party_affiliation'] for item in party_counts], 
                                      values=[item['count'] for item in party_counts], 
                                      hole=0.3)])
        fig2.update_layout(title_text="Distribution of Voters by Party Affiliation", height=1000, width=1000)
        context['party_pie_chart'] = plotly.offline.plot(fig2, auto_open=False, output_type="div")

        participation_data = [
            {'election': '2020 State', 'count': voters.filter(v20state=True).count()},
            {'election': '2021 Town', 'count': voters.filter(v21town=True).count()},
            {'election': '2021 Primary', 'count': voters.filter(v21primary=True).count()},
            {'election': '2022 General', 'count': voters.filter(v22general=True).count()},
            {'election': '2023 Town', 'count': voters.filter(v23town=True).count()},
        ]
        fig3 = go.Bar(x=[item['election'] for item in participation_data], y=[item['count'] for item in participation_data])
        context['participation_chart'] = plotly.offline.plot({"data": [fig3], "layout": {"title": "Voting Participation"}}, auto_open=False, output_type="div")

        context['form'] = VoterFilterForm(self.request.GET)

        return context
