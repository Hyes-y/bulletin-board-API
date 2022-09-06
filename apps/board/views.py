# django rest api
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
# local modules
from .models import Post
from .serializers import PostSerializer, PostDeleteSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    게시판 글 CRU ViewSet
    """
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer

    def destroy(self, request, pk=None):
        """
        Delete 메소드는 허용하지 않습니다.
        """
        response = {'ERROR': 'Delete 메소드는 허용하지 않습니다.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # def perform_create(self, serializer):
    #     serializer.save()


class PostDeleteViewSet(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    queryset = Post.objects.all()
    serializer_class = PostDeleteSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        request.data['is_deleted'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = {'Success Deleted': '성공적으로 삭제되었습니다.'}
        return Response(response, status=status.HTTP_204_NO_CONTENT)



