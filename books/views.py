from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, status, viewsets


class BookListApiView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True).data
        data = {
            'status': 'success',
            'books': serializer
        }
        return Response(data)

class BookDetailApiView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book).data

            data = {
                'status': 'success',
                'book': serializer
            }
            return Response(data)
        except Exception:
            return Response({
                'status': 'Does not exsists',
                'error': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)


class BookDeleteApiView(APIView):
    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({
                'status': 'success',
                'message': 'Book deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'status': 'Does not exist',
                'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

class BookUpdateApiView(APIView):
    def put(self, request, pk):
        book = get_object_or_404(Book.objects.all(), pk=pk)
        data = request.data
        serializer = BookSerializer(book, data=data, partial=True)
        if serializer.is_valid():
            book_saved = serializer.save()
        return Response({
            'status': 'success',
            'message': 'Book updated successfully',
        }, status=status.HTTP_200_OK)



class BookCreateApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': 'success',
                'data': data
            }
            return Response(data)



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# @api_view(['GET'])
# def book_list_view(request, *args, **kwargs):
#     books = Book.objects.all()
#     serializer = BookSerializer(books, many=True)
#     return Response(serializer.data)

# class BookCreateApiView(generics.CreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class BookDetailApiView(generics.RetrieveAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookDeleteApiView(generics.DestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookUpdateApiView(generics.UpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer