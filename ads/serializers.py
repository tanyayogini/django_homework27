from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import BooleanField
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category, Selection
from users.models import User


class IsNotFalseValidator:
    def __call__(self, value):
        if value is True:
            raise ValidationError("Is_published cannot be True")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ad


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = BooleanField(validators=[IsNotFalseValidator()], required=False)

    class Meta:
        fields = '__all__'
        model = Ad


class AdListSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    class Meta:
        exclude = ['description']
        model = Ad


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Ad


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Selection


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = SlugRelatedField(slug_field='username', read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Selection

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Selection


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Selection
