from rest_framework import status
from rest_framework.test import APITestCase

from apps.board.models import Post
import bcrypt


class BoardAPITest(APITestCase):
    """
    게시글 등록, 수정, 삭제 테스트
    """
    def setUp(self):
        """ test 를 위한 mock 데이터 추가 """

        # mock 데이터에는 암호화한 비밀번호를 저장해야 함.
        password = bcrypt.hashpw("test1234".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.post = Post.objects.create(
            title="테스트 post",
            content="테스트 데이터",
            author="test",
            password=password
        )

    def test_post_success(self):
        """ 게시 성공 테스트 """

        data = {
            "title": "테스트",
            "content": "테스트 입니다.",
            "author": "test",
            "password": "test1234"
        }

        request_url = "/api/v1/board/posts/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_fail_due_to_title(self):
        """ 게시 실패 테스트 : 제목이 20자 초과인 경우 """

        data = {
            "title": "20자 초과 글자수로 인한 게시 실패 테스트입니다.",
            "content": "테스트 입니다.",
            "author": "test",
            "password": "test1234"
        }

        request_url = "/api/v1/board/posts/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_fail_due_to_content(self):
        """ 게시 실패 테스트 : 본문이 200자 초과인 경우 """

        invalid_content = "200자 초과일 경우 게시글이 등록되지 않는 테스트 입니다." * 8
        data = {
            "title": "본문 조건 위배 테스트",
            "content": invalid_content,
            "author": "test",
            "password": "test1234"
        }

        request_url = "/api/v1/board/posts/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_fail_due_to_wrong_password(self):
        """ 게시 실패 테스트 : 비밀번호가 유효하지 않은 경우 """

        data = {
            "title": "비밀번호 조건 위배 테스트",
            "content": "비밀번호 조건 위배 테스트입니다.",
            "author": "test",
            "password": "test"
        }

        request_url = "/api/v1/board/posts/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_success(self):
        """ 게시글 수정 성공 테스트 """

        data = {
            "title": "테스트 수정",
            "content": "테스트 입니다.",
            "author": "test",
            "password": "test1234"
        }

        request_url = f"/api/v1/board/posts/{self.post.id}/"

        response = self.client.put(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_fail_due_to_wrong_password(self):
        """ 게시긑 수정 실패 테스트 : 비밀번호가 일치하지 않는 경우 """

        data = {
            "title": "테스트",
            "content": "테스트 입니다.",
            "author": "test",
            "password": "test123"
        }

        request_url = f"/api/v1/board/posts/{self.post.id}/"

        response = self.client.put(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_fail_due_to_wrong_password(self):
        """ 게시글 삭제 실패 테스트 : 비밀번호가 일치하지 않는 경우 """

        data = {
            "password": "test123"
        }

        request_url = f"/api/v1/board/posts-delete/{self.post.id}/"

        response = self.client.put(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success(self):
        """ 게시글 삭제 성공 테스트 """

        data = {
            "password": "test1234"
        }

        request_url = f"/api/v1/board/posts-delete/{self.post.id}/"

        response = self.client.put(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



