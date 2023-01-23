from rest_framework import serializers

from .models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {
            'email',
            'username',
            'password'
        }

    def validate_password(self, value):
        if value == self.initial_data.get('password1'):
            return value
        raise ValidationError('(password, password1) 불일치')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
        )

        user.is_active = False
        user.save()

        message = render_to_string('template/signup_template.html', {
            'user': user,
            'domain': 'localhost:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token': account_activation_token.make_token(user),
        })

        mail_subject = 'test'
        to_email = user.username
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return validated_data