from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *


class GithubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubUser
        fields = [
            "id",
            "name",
            "github_handle",
            "blurb",
            "location",
            "github_profile_link",
            "twitter_handle",
            "email",
            "created_at",
            "updated_at",
        ]


class FetchParameterSerialzier(serializers.Serializer):
    query_keyword = serializers.ListField(child=serializers.CharField())
    location = serializers.CharField(required=False)
    language = serializers.ListField(child=serializers.CharField(), required=False)
    sort = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs["sort"].lower() not in ["followers", "repositories", "joined"]:
            raise ValidationError({"message": "invalid sort for users"})
        return super().validate(attrs)
