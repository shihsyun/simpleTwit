from django.db import models
from .managers import AuthUserManager, AuthTokenManager, TwitManager, CommentManager


class AuthUser(models.Model):

    id = models.IntegerField('id', primary_key=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AuthUserManager()

    def __str__(self):
        return '< User id: {} email: {} name: {}'.format(self.id, self.email, self.nickname)


class AuthToken(models.Model):
    id = models.IntegerField('id', primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    code = models.CharField('code', max_length=40, unique=True)
    expire_at = models.DateTimeField()

    objects = AuthTokenManager()

    def __str__(self):
        return '< Token id: {} username: {} token: {} expre at: {}'.format(self.id, self.user, self.code, self.expire_at)


class Twit(models.Model):
    id = models.IntegerField('id', primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT)
    content = models.CharField('content', max_length=140, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(null=True)
    likeit = models.ManyToManyField(AuthUser, related_name='likeit')

    objects = TwitManager()

    def __str__(self):
        return '< Twit id: {} username: {} twit: {} created at: {}'.format(self.id, self.user, self.content, self.created_at)


class Comment(models.Model):
    id = models.IntegerField('id', primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT)
    twit = models.ForeignKey(Twit, on_delete=models.CASCADE)
    content = models.CharField('content', max_length=140, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(null=True)

    objects = CommentManager()

    def __str__(self):
        return '< Comment id: {} username: {} cooment: {} created at: {}'.format(self.id, self.user, self.content, self.created_at)
