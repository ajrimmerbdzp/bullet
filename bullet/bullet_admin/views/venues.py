from competitions.models import Venue
from django.contrib import messages
from django.forms import Form
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from documents.generators.certificate import certificates_for_venue
from documents.generators.team_list import team_list
from documents.generators.tearoff import TearoffGenerator
from problems.logic.results import save_venue_ranks
from problems.models import CategoryProblem, Problem
from users.logic import get_venue_waiting_list, move_eligible_teams
from users.models import Team

from bullet_admin.access import AdminAccess, CountryAdminAccess, VenueAccess
from bullet_admin.forms.documents import CertificateForm, TearoffForm
from bullet_admin.forms.venues import VenueForm
from bullet_admin.mixins import AdminRequiredMixin, RedirectBackMixin
from bullet_admin.utils import get_active_competition
from bullet_admin.views import GenericForm


class VenueListView(AdminAccess, ListView):
    require_unlocked_competition = False
    template_name = "bullet_admin/venues/list.html"
    paginate_by = 100

    def get_queryset(self):
        # For whatever reason, when you annotate the queryset, it loses
        # the default ordering...
        return (
            Venue.objects.for_request(self.request).annotate_teamcount().natural_order()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["venue_count"] = Venue.objects.for_request(self.request).count()
        return ctx


class VenueFormMixin(GenericForm):
    form_class = VenueForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["user"] = self.request.user
        kw["competition"] = get_active_competition(self.request)
        return kw


class VenueDetailView(VenueAccess, DetailView):
    require_unlocked_competition = False
    template_name = "bullet_admin/venues/detail.html"

    def get_permission_venue(self) -> Venue:
        return self.get_object()

    def get_queryset(self):
        return Venue.objects.for_request(self.request)


class VenueUpdateView(VenueAccess, VenueFormMixin, UpdateView):
    form_title = "Edit venue"
    template_name = "bullet_admin/venues/form.html"

    def get_permission_venue(self) -> Venue:
        return self.get_object()

    def get_queryset(self):
        return Venue.objects.for_request(self.request)

    def get_success_url(self):
        messages.success(self.request, "Venue edited succesfully.")
        return reverse("badmin:venue_list")


class VenueCreateView(CountryAdminAccess, VenueFormMixin, CreateView):
    form_title = "New venue"

    def get_success_url(self):
        messages.success(self.request, "Venue created succesfully.")
        return reverse("badmin:venue_list")


class VenueMixin(VenueAccess):
    template_name = "bullet_admin/venues/form.html"

    def get_permission_venue(self) -> "Venue":
        return self.venue

    @cached_property
    def venue(self):
        return get_object_or_404(
            Venue.objects.for_request(self.request), id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["venue"] = self.venue
        return ctx


class CertificateView(VenueMixin, GenericForm, FormView):
    require_unlocked_competition = False
    form_class = CertificateForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["competition"] = get_active_competition(self.request)
        return kw

    def form_valid(self, form):
        data = certificates_for_venue(
            self.venue,
            form.cleaned_data["template"],
            form.cleaned_data["count"],
            form.cleaned_data["empty"],
        )
        return FileResponse(data, as_attachment=True, filename="certificates.pdf")


class TeamListView(VenueMixin, GenericForm, FormView):
    require_unlocked_competition = False
    form_class = Form

    def form_valid(self, form):
        venue = self.venue
        data = team_list(
            Team.objects.competing().filter(venue=venue, number__isnull=False),
            f"Team list: {venue.name}",
        )
        return FileResponse(data, as_attachment=True, filename="team_list.pdf")


class WaitingListView(AdminRequiredMixin, VenueMixin, ListView):
    require_unlocked_competition = False
    template_name = "bullet_admin/venues/waiting_list.html"

    def get_queryset(self):
        return get_venue_waiting_list(self.venue)


class WaitingListAutomoveView(AdminRequiredMixin, VenueMixin, View):
    def post(self, request, *args, **kwargs):
        move_eligible_teams(self.venue)
        return HttpResponseRedirect(self.get_redirect_url())

    def get_redirect_url(self):
        return reverse("badmin:waiting_list", kwargs={"pk": self.venue.id})


class TearoffView(VenueMixin, GenericForm, FormView):
    form_class = TearoffForm
    form_multipart = True
    template_name = "bullet_admin/venues/tearoffs.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        competition = get_active_competition(self.request)
        problem_count = Problem.objects.filter(competition=competition).count()
        first_problem = (
            CategoryProblem.objects.filter(category=self.venue.category)
            .order_by("number")
            .first()
        )
        kw["problems"] = problem_count
        kw["first_problem"] = first_problem.number if first_problem else 1
        return kw

    def form_valid(self, form):
        t = TearoffGenerator(form.cleaned_data["problems"])
        teams = list(
            Team.objects.competing()
            .filter(venue=self.venue, number__isnull=False)
            .all()
        )
        for i in range(form.cleaned_data["backup_teams"]):
            teams.append(Team(venue=self.venue, name="???", number=999 - i))
        data = t.generate_pdf(
            teams, form.cleaned_data["first_problem"], form.cleaned_data["ordering"]
        )
        return FileResponse(data, filename="tearoffs.pdf")


class FinishReviewView(VenueMixin, RedirectBackMixin, GenericForm, FormView):
    form_class = Form
    form_title = "Finish venue review"
    form_submit_color = "green"
    form_submit_label = "Finish review"
    form_submit_icon = "mdi:check"
    template_name = "bullet_admin/venues/finish_review.html"

    def get_default_success_url(self):
        return reverse("badmin:venue_detail", kwargs={"pk": self.venue.id})

    def form_valid(self, form):
        if self.venue.has_unreviewed_teams:
            messages.error(self.request, "This venue has unreviewed teams.")
            return redirect("badmin:venue_finish_review", self.venue.id)

        self.venue.is_reviewed = True
        self.venue.save()

        save_venue_ranks.delay(self.venue.id)

        return super().form_valid(form)
