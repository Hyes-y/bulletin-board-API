from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from .models import Post
import bcrypt
import re


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'password', 'weather', 'created_at', 'updated_at')
        read_only_fields = ['id', 'weather', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        데이터 직렬화 할 때 비밀번호 제외하는 함수
        """
        res = super().to_representation(instance)
        del res['password']
        return res

    def validate(self, data):
        """
        입력 데이터 유효성 검사 함수
        조건 1. 제목(title) 이 1글자 이상 20글자 이하인지
            2. 본문(content) 가 1글자 이상 200글자 이하인지
            3. 비밀번호(password) 가 숫자 1개 이상을 포함하며 6자리 이상인지
        """
        # 비밀번호 유효성 검증을 위한 정규식
        reg = re.compile(r'\d+')

        if not (1 <= len(data['title']) <= 20):
            raise ValidationError("ERROR: 제목은 1글자 이상 20글자 이하 여야 합니다.")

        elif not (1 <= len(data['content']) <= 200):
            raise ValidationError("ERROR: 제목은 1글자 이상 20글자 이하 여야 합니다.")

        elif (len(data['password']) < 6) or not reg.search(data['password']):
            raise ValidationError("ERROR: 비밀번호는 6자리 이상이어야 하며, 숫자 1자리 이상 필수 포함 입니다.")

        else:
            return data

    def create(self, validated_data):
        """
        글 생성 함수
        암호화된 비밀번호 저장
        """
        password = validated_data['password'].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        decoded_password = encrypted_password.decode('utf-8')
        validated_data['password'] = decoded_password
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        게시글 수정 함수
        비밀번호가 일치해야 수정 가능
        """
        password = validated_data.pop('password').encode('utf-8')
        real_password = instance.password.encode('utf-8')
        if not bcrypt.checkpw(password, real_password):
            raise ValidationError("ERROR: 비밀번호가 일치하지 않습니다.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostDeleteSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        게시글 삭제 함수
        비밀번호가 일치해야 삭제 가능
        삭제: is_deleted = True
        """
        password = validated_data.pop('password').encode('utf-8')
        real_password = instance.password.encode('utf-8')
        if not bcrypt.checkpw(password, real_password):
            raise ValidationError("ERROR: 비밀번호가 일치하지 않습니다.")

        instance.is_deleted = True

        instance.save()
        return instance

