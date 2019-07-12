from django.contrib.auth.models import User
from rest_framework import serializers


class MeSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
        model = User
