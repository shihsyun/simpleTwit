import bcrypt
import secrets
from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class AuthUserManager(models.Manager):

    def verify_password(self, email, password):
        user = self.get(email=email)
        if user is None:
            return False
        return bcrypt.checkpw(password, user.password)


class AuthTokenManager(models.Manager):

    def create(self, user, expire=86400):

        code = secrets.token_urlsafe(30)
        token = self.model(user=user, code=code,
                           expire_at=timezone.now()+timedelta(seconds=expire))

        return token

    def remove(self, code):

        try:
            token = self.get(Q(code=code))
        except ObjectDoesNotExist:
            return False

        token.delete()

        return True

    def verify(self, code):

        token_code = code.split(' ')[1]
        try:
            token = self.get(Q(code=token_code) & Q(
                expire_at__gte=timezone.now()))
        except ObjectDoesNotExist:
            return None

        return token


class TwitManager(models.Manager):

    def create(self, user, text):

        twit = self.model(user=user, content=self._validate_content(text))

        return twit

    def update(self, twit, text):
        twit.content = self._validate_content(text)
        twit.modify_at = timezone.now()

        return twit

    def _validate_content(self, content):
        if len(content) > 140:
            raise ValueError(_(
                'The twit\'s length must less than 140.'))

        return content


class CommentManager(models.Manager):

    def create(self, user, twit, text):

        comment = self.model(user=user, twit=twit,
                             content=self._validate_content(text))

        return comment

    def update(self, comment, text):
        comment.content = self._validate_content(text)
        comment.modify_at = timezone.now()

        return comment

    def _validate_content(self, content):
        if len(content) > 140:
            raise ValueError(_(
                'The comment\'s length must less than 140.'))

        return content
