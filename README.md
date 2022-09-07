# 게시판 CRUD API (Bulletin-Board API)
원티드 프리온보딩 백엔드 기업 과제

____

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [과제 요구사항 분석](#과제-요구사항-분석)
- [프로젝트 기술 스택](#프로젝트-기술-스택)
- [개발 기간](#개발-기간)
- [ERD](#ERD)
- [API 목록](#API-목록)
- [프로젝트 시작 방법](#프로젝트-시작-방법)


---

<br>

## 프로젝트 개요

---

Django Rest Framework 를 이용한 REST API 서버로

- 게시글 CRUD
- 게시글 Pagination(20개씩)
- weather API 연동(게시글 등록시 실시간 날씨 반영)

위 기능을 제공합니다.

<br>

## 과제 요구사항 분석

---

### 1. 게시판 CRUD

#### 1) 글 작성

- 글 작성시 제목, 본문, 비밀번호(암호화) 필요

    - 비밀번호 암호화는 `bcrypt` 모듈 사용
- 제목은 최대 20자, 본문은 최대 200자

  - serializer의 validate() 함수 이용
      
  - model field의 경우 두 속성 다 `CharField` 사용 <br>
  😮 `TextField` 의 `max_length`는 폼의 area에 크기에 영향 <br> 
  → 길이 제한 위해 `CharField`로 결정 
- 비밀번호는 최소 6자 이상, 숫자는 1개 이상 반드시 포함

    - 정규표현식(`re` 모듈)을 이용하여 해당 조건 유효성 검사 

- create 요청시 해당 유저의 IP를 기반으로 실시간 날씨 반영
  
    - 기본값 : 서울 날씨
    - weather api(https://www.weatherapi.com/) 이용
    - weather 필드에 포함 (ex. '맑음')

<br>

#### 2) 글 조회

- 글 조회시 최신순으로 정렬

  - model Meta 클래스에 `ordering=['-created_at']` 적용

- 글 개수가 많은 경우 페이지네이션 (20개씩)

    - rest_framework 에서 제공하는 `CursorPagination` 사용
  
  <br>
  
#### 3) 글 수정, 삭제

- 비밀번호를 이용하여 글 수정, 삭제 가능

    - 암호화된 비밀번호와 비교하여 일치하면 요청 수행
    - 삭제할 때 soft delete 방식 사용
    - 비밀번호 입력받고 `is_deleted` 속성을 수정하므로 `PUT` 메소드 사용


<br>

### 기능 목록

| 버전   | 기능 | 설명                                          | 상태 |
|------| --- |---------------------------------------------| --- |
| v1   | 글 생성 | 제목, 본문, 작성자, 비밀번호를 입력받아 글 생성                | ✅ |
| -    | 전체 글 조회 | 최신순으로 정렬된 글을 20개씩 조회 (pagination=True)      | ✅ |
| -    | 특정 글 조회 | id 에 해당하는 글을 조회                             | ✅ | 
| -    | 글 수정 | (변경할 내용 포함) 제목, 본문, 작성자, 비밀번호를 입력받아 변경사항 저장 | ✅ |
| -    | 글 삭제 | 비밀번호를 입력 받아 해당 글 삭제 처리(is_deleted = True)   | ✅ |
| -    | 날씨 정보 받아오기 | weather-api 를 이용해 실시간 날씨 정보 얻어오기 | ✅ | 
| -    |

🔥 추가 기능 구현시 업데이트 예정

<br>

## 프로젝트 기술 스택

---

### Backend
<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB
<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools
<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord-5865F2?logo=Discord&logoColor=white">
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>


<br>


## 개발 기간

---

- 2022/09/06~2022/09/07


<br>


## ERD

---

- made by ERDCLOUD

![](http://drive.google.com/uc?export=view&id=1FsXlMNzyytnI4HYA80u7_WKKPsQDPcZk)

<br>


## API 목록

---

[Postman API Document](https://documenter.getpostman.com/view/19274775/VVBRynns)

<br>


## 프로젝트 시작 방법

---

1. 로컬에서 실행할 경우

```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b main --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt
# 실행
python manage.py runserver
```

<br>
