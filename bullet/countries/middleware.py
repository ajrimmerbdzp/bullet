import re

from countries.logic import country
from countries.logic.cache import get_country_cache
from countries.models import BranchCountry
from django.http import HttpResponseNotFound
from django.utils import timezone, translation

country_language_re = re.compile(r"^/([a-z]{2})/([^/]+)/")


def country_language_from_request(request):
    match = country_language_re.match(request.path_info)
    if not match:
        return None, None

    return match.groups()


class CountryLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        c, lang = country_language_from_request(request)

        if c and not request._is_admin_domain:
            cache = get_country_cache()
            if request.BRANCH is not None and (
                c not in cache[request.BRANCH.id]
                or lang not in cache[request.BRANCH.id][c]
            ):
                return HttpResponseNotFound(
                    "BranchCountryLanguage combination not found."
                )

            country.activate(c)
            request.COUNTRY_CODE = c

            branch_country = BranchCountry.objects.get(
                branch=request.BRANCH, country=c.upper()
            )
            timezone.activate(branch_country.timezone)

            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)

        if c and not request._is_admin_domain:
            ckie = request.COOKIES.get("bullet_country", "")
            expected = f"{c}|{lang}"
            if ckie != expected:
                response.set_cookie(
                    "bullet_country",
                    expected,
                    expires=365 * 24 * 60 * 60,
                    samesite="Lax",
                )

        return response
