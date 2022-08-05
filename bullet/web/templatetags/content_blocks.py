from django import template
from django.db.models import Q
from django.utils.safestring import mark_safe
from web.models import ContentBlock

register = template.Library()


@register.simple_tag(name="load_blocks", takes_context=True)
def load_blocks(context, *groups):
    if "__blocks" not in context:
        context["__blocks"] = {}
        context["__blocks_loaded"] = set()

    groups = set(groups)
    groups.difference_update(context["__blocks_loaded"])

    if not len(groups):
        return ""

    req = context.request
    blocks = ContentBlock.objects.filter(
        (Q(branch__isnull=True) | Q(branch=req.BRANCH.id))
        & (Q(country__isnull=True) | Q(country=req.COUNTRY_CODE.upper()))
        & Q(language=req.LANGUAGE_CODE)
        & Q(group__in=groups)
    )

    context["__blocks"].update(
        {
            (b.group, b.branch, b.country.code.lower(), b.reference): b.content
            for b in blocks
        }
    )
    context["__blocks_loaded"].update(groups)
    return ""


@register.simple_tag(name="content_block", takes_context=True)
def content_block(context, combined_ref):
    group, ref = combined_ref.split(":", 1)

    if "__blocks" not in context:
        raise KeyError("No content blocks were loaded.")
    if group not in context["__blocks_loaded"]:
        raise KeyError(f"Content block group '{group}' is not loaded.")

    request = context.request
    keys = [
        (group, request.BRANCH.id, request.COUNTRY_CODE, ref),
        (group, request.BRANCH.id, None, ref),
        (group, None, request.COUNTRY_CODE, ref),
        (group, None, None, ref),
    ]

    for key in keys:
        if key in context["__blocks"]:
            c = context["__blocks"][key]
            if request.GET.get("showblocks", 0):  # TODO: limit to admin users
                return mark_safe(
                    f"<a href='#' class='cb-edit' title='{group}:{ref}'>{c}</a>"
                )
            return mark_safe(c)

    return mark_safe(f"<span class='cb-missing'>Missing '{group}:{ref}'</span>")
