from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    '''To validate a new user registration'''
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        '''Override create method foe password Hashing'''
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    '''To validate login credentials'''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
