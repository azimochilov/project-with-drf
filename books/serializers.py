from rest_framework import serializers
from .models import Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title','author', 'isbn','price')

    def validate(self, data):

        title = data.get('title', None)
        author = data.get('author', None)

        if not title.isalpha():
            raise serializers.ValidationError(
                {
                    'status':False,
                    'message':"Title must be alphanumeric"
                })

        if Book.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                {
                    'status':False,
                    'message':"You cant upload book with same author and title"
                }
            )

        return data

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {
                    'status':False,
                    'message':"Price must be greater than 0"
                }
            )