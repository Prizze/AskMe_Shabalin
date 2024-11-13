from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + " " + self.user.email 

class TagManager(models.Manager):
    def get_top_tags(self):
        return self.annotate(num_questions=Count('question')).order_by('-num_questions')[:10]

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name        

class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')
    def get_hot(self):
        return self.order_by('-rating')
    def get_questions_by_tag(self, tag):
        return self.filter(tags=tag)

class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return f'{self.title}. Reactions: {self.rating}'


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('-rating')

class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    is_correct = models.BooleanField(null=True, blank=True)

    objects = AnswerManager()

    def __str__(self):
        return f'{self.body}. Reactions: {self.rating}'

class QuestionReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.title + self.reaction

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.reaction == self.LIKE:
                self.question.like_count += 1
            elif self.reaction == self.DISLIKE:
                self.question.dislike_count += 1

        self.question.rating = self.question.like_count - self.question.dislike_count
        self.question.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.reaction == self.LIKE:
            self.question.like_count -= 1
        elif self.reaction == self.DISLIKE:
            self.question.dislike_count -= 1
        
        self.question.rating = self.question.like_count - self.question.dislike_count
        self.question.save()
        super().delete(*args, **kwargs)

    class Meta:
        unique_together = ('profile', 'question')
    
        

class AnswerReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer.body + self.reaction

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.reaction == self.LIKE:
                self.answer.like_count += 1
            elif self.reaction == self.DISLIKE:
                self.answer.dislike_count += 1
        
        self.answer.rating = self.answer.like_count - self.answer.dislike_count
        self.answer.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.reaction == self.LIKE:
            self.answer.like_count -= 1
        elif self.reaction == self.DISLIKE:
            self.answer.dislike_count -= 1
        
        self.answer.rating = self.answer.like_count - self.answer.dislike_count
        self.answer.save()

        super().delete(*args, **kwargs)

    class Meta:
        unique_together = ('profile', 'answer')
