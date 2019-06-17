from django.shortcuts import render, redirect
from .models import Movie, Person, Vote
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.forms import VoteForm
# Create your views here.


class MovieListView(ListView):
    model = Movie
    template_name = "core/movie_list.html"


class MovieDetailView(DetailView):
    queryset = Movie.objects.all_with_related_persons()
    template_name = "core/movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object
                user=self.request.user
            )
            if vote.id:
                vote_from_url = reverse('core:UpdateVote', kwargs={
                                        'movie_id': vote.movie.id, 'pk': vote.id})
            else:
                vote_from_url = reverse('core:CreateVote', kwargs={
                                        'movie_id': self.object.id})
            vote_from = VoteForm(instance=vote)
            context['vote_form'] = vote_from
            context['vote_from_url'] = vote_from_url
        return context


class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()
    template_name = "core/person_detail.html"


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)
    template_name = "TEMPLATE_NAME"
