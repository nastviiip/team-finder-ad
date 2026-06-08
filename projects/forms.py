from django import forms

from .models import Project
from team_finder.utils import validate_github_url


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))
