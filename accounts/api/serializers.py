from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from django.db.models import Q

from rest_framework.serializers import (
    EmailField,
    CharField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

User = get_user_model()

class CreateUserSerializer(ModelSerializer):
    email2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        user_obj = User(
            username = username,
            email = email,
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data


class LoginUserSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    #email = EmailField(label='Confirm Email', required=False, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            #'email',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        #email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]
        if not username:
            raise ValidationError("A username or password is required!")

        user = User.objects.filter(
            #Q(email=email) |
            Q(username=username)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password.")

        data["token"] = "SOME RANDOM TOKEN"


        return data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        #email = validated_data['email']

        user_obj = User(
            username = username,
            #email = email,
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data