from django.db import models


class SavedFormula(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    expression = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class PricingRule(models.Model):
    code = models.SlugField(unique=True)
    expression = models.TextField(help_text="Python expression over base, qty and region")
    active = models.BooleanField(default=True)
