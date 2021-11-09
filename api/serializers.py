from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile,Study

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model=Profile
        fields = (
            'id', 
            'nickName', 
            'userProfile', 
            'created_on', 
            'img',
            'point',
            'twitter_name',
            'github_name'
            )
        extra_kwargs = {'userProfile': {'read_only': True}}



class StudySerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Study
        fields = (
            'id', 
            'userStudy',
            'created_on', 
            'study_time',
            'comment',
            'language'
            )
        extra_kwargs = {'userStudy': {'read_only': True}}

