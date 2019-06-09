import re
import bcrypt
from rest_framework import serializers
from .models import AuthUser, Twit
from django.utils.translation import ugettext_lazy as _


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ('email', 'nickname', 'password')

    def validate_password(self, password):

        if len(password) < 5:
            raise serializers.ValidationError(_(
                'The password\'s length must more than 5.'))

        if not re.findall('\d', password):
            raise serializers.ValidationError(_(
                'The password must contain at least 1 digit.'))

        if not re.findall('[A-Z]', password):
            raise serializers.ValidationError(_(
                'The password must contain at least 1 uppercase letter.'))

        if not re.findall('[a-z]', password):
            raise serializers.ValidationError(_(
                'The password must contain at least 1 lowercase letter.'))

        return self._hash_password(password)

    def validate_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of the it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def _hash_password(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())


class TwitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Twit
        fields = ('user', 'content')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Twit
        fields = ('user', 'twit', 'content')
