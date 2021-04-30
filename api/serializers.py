from django.contrib.auth.models import User
from rest_framework import serializers

from api.models.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True, required=False)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                           required=False,
                                           read_only=True)
    deadline = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = Task
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
