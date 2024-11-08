from django.shortcuts import render
from .models import Voter
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q
from django.shortcuts import render

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter queryset based on search criteria."""
        qs = super().get_queryset()

        # Retrieve filter values from GET request
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

        # Apply filters
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

        # Add filter options to context
        context['party_options'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['year_range'] = range(1900, 2025)
        context['voter_score_range'] = range(1, 6)
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        return context

# import plotly.graph_objs as go
# import plotly.offline as pyo
from django.views.generic import DetailView
from .models import Voter

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = self.get_object()

        # Example: Bar chart for voter participation in elections
        participation_data = {
            'v20state': voter.v20state,
            'v21town': voter.v21town,
            'v21primary': voter.v21primary,
            'v22general': voter.v22general,
            'v23town': voter.v23town,
        }

        data = go.Bar(x=list(participation_data.keys()), y=[int(v) for v in participation_data.values()])
        layout = go.Layout(title=f'{voter.first_name} {voter.last_name} - Election Participation', xaxis={'title': 'Elections'}, yaxis={'title': 'Voted (1: Yes, 0: No)'})
        fig = go.Figure(data=[data], layout=layout)

        context['voter_participation_graph'] = pyo.plot(fig, auto_open=False, output_type='div')

        return context

import plotly.graph_objs as go
import plotly.offline as pyo
from django.views.generic import ListView
from .models import *

class GraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter queryset based on search criteria."""
        qs = super().get_queryset()

        # Retrieve filter values from GET request
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

        # Apply filters
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

        # Add filter options to context
        context['party_options'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['year_range'] = range(1900, 2025)
        context['voter_score_range'] = range(1, 6)
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        # Generate graphs
        context['graph_birth_year'] = self.get_birth_year_histogram()
        context['graph_party_affiliation'] = self.get_party_affiliation_pie_chart()
        context['graph_election_participation'] = self.get_election_participation_histogram()

        return context

    def get_birth_year_histogram(self):
        """Generate histogram for voter birth years."""
        birth_years = self.get_queryset().values_list('date_of_birth', flat=True)
        birth_years = [dob.year for dob in birth_years]

        data = go.Histogram(x=birth_years, nbinsx=30)
        layout = go.Layout(title='Distribution of Voters by Year of Birth', xaxis={'title': 'Year of Birth'}, yaxis={'title': 'Count'})

        fig = go.Figure(data=[data], layout=layout)
        return pyo.plot(fig, auto_open=False, output_type='div')

    def get_party_affiliation_pie_chart(self):
        """Generate pie chart for party affiliation."""
        queryset = self.get_queryset().values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        labels = [item['party_affiliation'] for item in queryset]
        values = [item['count'] for item in queryset]

        data = go.Pie(labels=labels, values=values)
        layout = go.Layout(title='Distribution of Voters by Party Affiliation', height=1000, width=800)

        fig = go.Figure(data=[data], layout=layout)
        return pyo.plot(fig, auto_open=False, output_type='div')

    def get_election_participation_histogram(self):
        """Generate histogram for election participation."""
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        counts = [self.get_queryset().filter(**{field: True}).count() for field in election_fields]

        data = go.Bar(x=election_fields, y=counts)
        layout = go.Layout(title='Voter Participation in Elections', xaxis={'title': 'Election'}, yaxis={'title': 'Count'})

        fig = go.Figure(data=[data], layout=layout)
        return pyo.plot(fig, auto_open=False, output_type='div')
