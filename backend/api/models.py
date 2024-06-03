from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    learning_class = models.CharField(max_length=50, blank=True, null=True)
    learning_level = models.CharField(max_length=50, blank=True, null=True)
    lesson_types = models.JSONField(default=list, blank=True)  # Store lesson types as a list

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

# Store the lesson
class Lesson(models.Model):
    student = models.ForeignKey('Profile', on_delete=models.CASCADE)
    lesson_text = models.TextField(null=True, blank=True)
    lesson_pdf = models.FileField(upload_to='lessons/', null=True, blank=True)

# Store the task result
class TaskResult(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    task_type = models.CharField(max_length=100)
    result = models.TextField()

# Store the feedback
class Feedback(models.Model):
    student = models.ForeignKey('Profile', on_delete=models.CASCADE)
    task_result = models.ForeignKey(TaskResult, on_delete=models.CASCADE)
    feedback_text = models.TextField()


# Store the quiz result
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_data = models.JSONField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"