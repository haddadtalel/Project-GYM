from typing import Any, Union
from myProject import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer = models.BooleanField("trainer", default=True)
    approve = models.BooleanField(default=False)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.approve:
            ######################### mail system #####################################
            try:
                email = self.user.email
                print("\n\n\n", email, settings.EMAIL_HOST_USER)
                htmly = get_template("user/Email.html")
                d = {"username": self.user.username}
                subject = "Welcome to FitMe, you are approved by admin"
                from_email = settings.EMAIL_HOST_USER
                to = email
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                print("email not working")

        img = Image.open(self.image.path)
        print("\n\n\n  -->  try saving image")
        width, height = img.size
        if height >= 300 or width >= 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        db_table = "trainer"


class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainee = models.BooleanField("trainee", default=True)
    trainer_ass = models.ForeignKey(
        Trainer, blank=True, null=True, on_delete=models.SET_NULL
    )
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2)  # Adjusted precision
    age = models.IntegerField()
    current_weight = models.DecimalField(max_digits=5, decimal_places=5)  # Adjusted precision
    body_fat = models.IntegerField()
    goal_weight = models.DecimalField(max_digits=5, decimal_places=2)  # Adjusted precision
    health_condition = models.CharField(max_length=50)
    dob = models.DateField(default=datetime.now)
    gender = models.CharField(max_length=6, default="Male", null=True, blank=True)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        print("\n\n\n  -->  try saving image")
        width, height = img.size
        if height >= 300 or width >= 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            print("no error")
            img.save(self.image.path)
        else:
            print("no error saving")
            img.save(self.image.path)

    class Meta:
        db_table = "trainee"
