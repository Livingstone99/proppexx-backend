from rest_framework import serializers
from .models import BookmarkProperty
from property.serializers import PropertyListSerializer

class BookmarkSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = BookmarkProperty
        fields = '__all__'
        read_only_fields = ('buyer',)
        

    def create(self, validated_data):
        user = BookmarkProperty(buyer = self.context['request'].user)
        bookmark = BookmarkProperty.objects.create(buyer = user.buyer, **validated_data)
        bookmark.save()
        return  bookmark


class GetBookmarkSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer()

    class Meta:
        model = BookmarkProperty
        fields = "__all__"


class DeleteBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkProperty
        fields = "__all__"
