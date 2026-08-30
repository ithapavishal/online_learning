from django.db import models
from online_learning_app.models import Course
from accounts.models import CustomUserModel

# Create your models here.

# quiz


class Quiz(models.Model):
    course = models.ForeignKey(
        Course, related_name='quizes', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# question


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


# Answer Model


class Answer(models.Model):
    question = models.OneToOneField(
        Question, related_name='correct_answer', on_delete=models.CASCADE
    )
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return f"Correct Answer for: {self.question.question_text}"


# option

class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE
    )
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text

# student progress


class StudentProgress(models.Model):
    user = models.ForeignKey(
        CustomUserModel, related_name='student_progresses', on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz, related_name='quiz', on_delete=models.CASCADE,
        default=''
    )
    question = models.ForeignKey(
        Question, related_name='attempt_questions', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f'Username: {self.user}'


class OverallProgress(models.Model):
    user = models.ForeignKey(
        CustomUserModel, related_name='overall_progress', on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz, related_name='quizes', on_delete=models.CASCADE
    )
    total_questions = models.PositiveIntegerField()
    score = models.PositiveIntegerField()

    def __str__(self):
        return f'Username: {self.user} score: {self.score}'
