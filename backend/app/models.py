from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    class Classes(models.TextChoices):
        A1 = "A1", _("1.A")
        A2 = "A2", _("2.A")
        A3 = "A3", _("3.A")
        A4 = "A4", _("4.A")
        A5 = "A5", _("5.A")
        A6 = "A6", _("6.A")
        B1 = "B1", _("1.B")
        B2 = "B2", _("2.B")
        B3 = "B3", _("3.B")
        B4 = "B4", _("4.B")
        B5 = "B5", _("5.B")
        B6 = "B6", _("6.B")
        C1 = "C1", _("1.C")
        C2 = "C2", _("2.C")
        C3 = "C3", _("3.C")
        C4 = "C4", _("4.C")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cls = models.CharField(max_length=2, choices=Classes.choices, blank=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        return f"{full_name} | {self.cls}" if self.cls else f"{full_name}"
