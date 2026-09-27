import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View

from lib.scripting import run_hook


class WebhookTestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("invalid json")
        sample_event = data.get("sample_event", {})
        outcome = run_hook(data["transform"], context=sample_event)
        return JsonResponse(outcome)
