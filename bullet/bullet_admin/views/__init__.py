from competitions.models import Competition
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.views.generic.edit import BaseDeleteView
from django_htmx.http import HttpResponseClientRefresh

from bullet_admin.models import CompetitionRole
from bullet_admin.utils import get_active_competition


class DeleteView(BaseDeleteView):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(permitted_methods=["POST"])


class GenericForm:
    form_title = None
    form_submit_label = "Save"
    form_submit_icon = "mdi:content-save"
    form_submit_color = "blue"
    form_multipart = False
    template_name = "bullet_admin/generic/form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form_title"] = self.form_title
        ctx["form_multipart"] = self.form_multipart
        ctx["form_submit_label"] = self.form_submit_label
        ctx["form_submit_icon"] = self.form_submit_icon
        ctx["form_submit_color"] = self.form_submit_color
        return ctx


class CompetitionSwitchView(LoginRequiredMixin, TemplateView):
    template_name = "bullet_admin/competition_switch.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.user.get_branch_role(self.request.BRANCH).is_admin:
            ctx["competitions"] = Competition.objects.filter(
                branch=self.request.BRANCH
            ).order_by("-competition_start")
            ctx["branch_admin"] = True
        else:
            ctx["branch_admin"] = False

        ctx["roles"] = (
            CompetitionRole.objects.filter(
                user=self.request.user, competition__branch=self.request.BRANCH
            )
            .select_related("competition")
            .prefetch_related("venue_objects")
            .order_by("-competition__competition_start")
            .all()
        )
        ctx["active"] = get_active_competition(self.request)
        return ctx

    def post(self, request, *args, **kwargs):
        if "competition" in request.GET:
            request.session[
                f"badmin_{request.BRANCH.identifier}_competition"
            ] = request.GET.get("competition")
        return HttpResponseClientRefresh()
