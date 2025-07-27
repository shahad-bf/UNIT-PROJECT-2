from django.db import models
from django.contrib.auth.models import User

# General models for the main app
# You can add general models here that don't belong to specific apps

# Example: Site settings, general configurations, etc.
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="MediConsult")
    site_description = models.TextField(blank=True)

    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name