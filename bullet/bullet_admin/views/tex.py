from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_htmx.http import HTMX_STOP_POLLING
from documents.models import TexJob, TexTemplate

from bullet_admin.access import AdminAccess, CountryAdminAccess
from bullet_admin.forms.tex import LetterCallbackForm, TexTemplateForm
from bullet_admin.utils import get_active_competition
from bullet_admin.views import GenericForm


@method_decorator(csrf_exempt, name="dispatch")
class LetterCallbackView(View):
    def post(self, *args, **kwargs):
        job = get_object_or_404(TexJob, pk=kwargs["pk"], output_file="")

        form = LetterCallbackForm(self.request.POST, self.request.FILES)
        if not form.is_valid():
            print(form.errors)
            return HttpResponse("invalid data", status=400)

        job.output_log = form.cleaned_data.get("tectonic_output", "")
        job.output_file = form.cleaned_data.get("file", "")
        job.output_error = form.cleaned_data.get("error", "")
        job.completed = True
        job.save()

        return HttpResponse("ok")


class JobDetailView(LoginRequiredMixin, DetailView):
    require_unlocked_competition = False

    def get_queryset(self):
        return TexJob.objects.filter(Q(creator=self.request.user) | Q(creator=None))

    def render_to_response(self, context, **response_kwargs):
        resp = super().render_to_response(context, **response_kwargs)

        if self.request.htmx and self.object.completed:
            resp.status_code = HTMX_STOP_POLLING

        return resp

    def get_template_names(self):
        if self.request.htmx:
            return ["bullet_admin/tex/job_output.html"]
        return ["bullet_admin/tex/job.html"]


class TemplateListView(AdminAccess, ListView):
    template_name = "bullet_admin/tex/template/list.html"

    def get_queryset(self):
        competition = get_active_competition(self.request)
        return TexTemplate.objects.filter(competition=competition)


class TemplateCreateView(CountryAdminAccess, GenericForm, CreateView):
    form_title = "Create TeX Template"
    form_class = TexTemplateForm
    form_multipart = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.competition = get_active_competition(self.request)
        self.object.save()

        return redirect("badmin:tex_template_list")


class TemplateUpdateView(CountryAdminAccess, GenericForm, UpdateView):
    form_title = "Update TeX Template"
    form_class = TexTemplateForm
    form_multipart = True

    def get_queryset(self):
        competition = get_active_competition(self.request)
        return TexTemplate.objects.filter(competition=competition)

    def get_success_url(self):
        return reverse("badmin:tex_template_list")
