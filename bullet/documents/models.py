import os
import secrets
import subprocess

from django.db import models
from django.template import Context, Template
from web.fields import BranchField

from documents.generators import prepare_rsvg


class SelfServeCertificate(models.Model):
    template = models.ForeignKey("CertificateTemplate", on_delete=models.CASCADE)
    venue = models.OneToOneField("competitions.Venue", on_delete=models.CASCADE)
    # TODO: Languages


class CertificateTemplate(models.Model):
    name = models.CharField(max_length=128)
    for_team = models.BooleanField(default=False)
    branch = BranchField()
    template = models.TextField()
    self_serve = models.ManyToManyField(
        "competitions.Venue", blank=True, through=SelfServeCertificate
    )

    def render(self, context: dict, output_format="pdf") -> bytes:
        template = Template(self.template)
        context = Context(context)
        source = template.render(context)
        env = prepare_rsvg()
        data = subprocess.check_output(
            [
                "rsvg-convert",
                "--format",
                output_format,
                "--dpi-x",
                "300",
                "--dpi-y",
                "300",
            ],
            input=source.encode("utf-8"),
            env=env,
        )
        return data

    def __str__(self):
        return self.name


def tex_template_upload(instance, filename):
    name, ext = os.path.splitext(filename)
    uid = secrets.token_urlsafe(64)
    return os.path.join("tex_templates", f"{uid}{ext}")


class TexTemplate(models.Model):
    competition = models.ForeignKey(
        "competitions.Competition", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    single_team = models.BooleanField(default=False)
    template = models.FileField(upload_to=tex_template_upload)
