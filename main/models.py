from django.db import models


class CV(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    skills = models.TextField(help_text="Skills separated by comma")
    projects = models.TextField(help_text="Projects separated by comma")
    bio = models.TextField(blank=True)
    contacts = models.JSONField(
        help_text="Contact information as a dict. "
                  "Example: {'phone': '+38099...', 'email': 'help@dteam.dev'}",
        default=dict,
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
