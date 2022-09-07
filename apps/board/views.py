# django rest api
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
# local modules
from .models import Post
from .serializers import PostSerializer, PostDeleteSerializer
from .utils import get_weather_info
from .paginations import CustomCursorPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    게시글 등록, 수정, 조회 ViewSet
    """
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    # pagination_class = CustomCursorPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 날씨 정보
        current_weather = get_weather_info(request)

        self.perform_create(serializer, current_weather)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, pk=None):
        """ DELETE 메소드는 허용하지 않습니다. """
        response = {'ERROR': 'DELETE 메소드는 허용하지 않습니다.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer, weather=None):
        # 날씨 정보도 함께 저장
        serializer.save(weather=weather)


class PostDeleteViewSet(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    게시글 삭제 ViewSet
    """
    queryset = Post.objects.all()
    serializer_class = PostDeleteSerializer

    def update(self, request, *args, **kwargs):
        """ 게시글 삭제 처리 """
        # QueryDict 객체 수정을 위해 copy
        data = request.data.copy()

        data['is_deleted'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = {'Success Deleted': '성공적으로 삭제되었습니다.'}
        return Response(response, status=status.HTTP_204_NO_CONTENT)

