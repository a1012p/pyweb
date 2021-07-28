from django.db import models
from django.contrib.auth.models import User

#질문 모델(데이터 베이스 테이블)
class Question(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="author_question")
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    voter = models.ManyToManyField(User,related_name="voter_question")
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.subject

#답변 모델
class Answer(models.Model):
    #외래키 제약조건 무시하고 연쇄 삭제 됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="author_answer")
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    voter = models.ManyToManyField(User,related_name="voter_answer")

    def __str__(self):
        return self.content

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    question = models.ForeignKey(Question,null=True,blank=True,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,null=True,blank=True,on_delete=models.CASCADE)