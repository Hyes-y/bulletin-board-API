from django.db import models


class Post(models.Model):
    """
    게시판 글 모델 (Post)
    정렬 - 최신순
    Input - title, content, author, password
    """
    created_at = models.DateTimeField(verbose_name='등록 날짜', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정 날짜', auto_now=True)

    title = models.CharField(verbose_name='제목', max_length=20)
    content = models.CharField(verbose_name='본문', max_length=200)
    # TextField 의 max_length 는 form area 에만 영향을 주고 model 혹은 database 레벨 에서는 영향을 주지 않는다.
    # 길이 제한이 필요하면 CharField 를 써야 한다.
    # 무얼 쓰면 좋을까?
    # content = models.TextField(verbose_name='본문')

    author = models.CharField(verbose_name='글쓴이', max_length=10)
    password = models.CharField(verbose_name='비밀번호', max_length=255)
    is_deleted = models.BooleanField(verbose_name="삭제 여부", default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
