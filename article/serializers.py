from rest_framework import serializers
from .models import Article


class CreateArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('writer',)
        depth = 1

    def create(self, validate_data):
        user = Article(writer=self.context['request'].user)
        article = Article(
            writer=user.writer,
            title=validate_data['title'],
            body=validate_data['body'],
            images=validate_data['images'],
            tag=validate_data.get('tag', [])
        )
        article.save()
        return article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('writer',)
