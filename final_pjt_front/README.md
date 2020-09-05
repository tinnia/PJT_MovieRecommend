# README

<hr>
![](README.assets/20200618175925.png)



<hr>

### 0. Local 실행 방법

git clone 후 해야하는 작업

#### FrontEnd

```sh
$ npm install
$ npm run serve
```

#### BackEnd

```sh
$ python -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
$ python manage.py migrate	
$ python manage.py createsuperuser
$ python manage.py runserver
$ python manage.py loaddata {data.json}		# data.json = moviedata.json
$ python manage.py collectstatic
```





### 1. 팀원 정보 및 업무 분담 내역

* 정다솜 : 프론트엔드 담당
  - Html, CSS, Bootstrap4를 활용한 화면 설계 및 디자인, Vue.js 로직 구현 및 핵심적인 UI 구현
* 박명수 :  백엔드 담당
  - Django API Server, API를 활용한 Data Seeding 구현





### 2. 목표 서비스 구현 및 실제 구현 정도

#### 목표 서비스

* 영화 정보 기반 추천 서비스 구성

* 커뮤니티 서비스 구성

* HTML, CSS, JavaScript, Vue.js, Django, REST API, DataBase 등을 활용한 실제 서비스 설계

* 서비스 배포 및 관리

  

#### 실제 구현도

* Vue.js 와 Django를 활용한 서비스 설계
* 영화 정보 기반 추천 서비스, 커뮤니티 서비스 구성
* HTML, CSS, JS을 활용한 화면 설계 및 디자인
* AWS , Ubunta를 활용한 서비스 배포



### 3. 프로젝트 과정

```sh
200611 : 프로젝트 계획 수립 및 명세 기반으로 기본적인 사이트 틀 작업
200612 : Data Seeding, Accounts와 Movie 기능 구현, Accounts 화면 설계 및 디자인(sign up, login, logout)
200613 ~ 14 : Movie 화면 설계 및 디자인, Accounts 기능 추가 및 화면 설계(Profile, admin)
200615 : Community 기능 구현, Community 화면 설계 및 디자인(리뷰, 댓글 조회/생성/수정/삭제)
200616 : Movie 기능 추가 및 화면 설계(추천 알고리즘, 평점 등록), Accounts 추가 기능 구현(성향)
200617 : Movie 기능 추가 및 화면 설계(Pagination, 기준별 조회), UCC와 PPT 작업
200618 : 오류 수정 및 디자인 추가 작업, 배포 시도..
```





### 3. 개발 환경

##### Frontend (Vue.js)

- axios : 0.19.2

- bootstrap : 4.5.0

- bootstrap-vue : 2.15.0

- vue : 2.6.11

- vue-cookies : 1.7.0

- vue-router : 3.3.2

- vue-star : 0.0.4

  

##### Backend (Django REST API 서버)

- Django : 2.1.12

- Django REST framework : 3.11.0

- Python : 3.7.4

  

##### 서비스 배포 환경

Ubuntu / Amazon Linux 





### 4. 데이터베이스 모델링(ERD)

![](README.assets/KakaoTalk_20200617_160838930.png)





### 5. 기능

#### Accounts

- 유저 프로필 화면
- 관리자 권한으로 유저 관리
- 등록한 리뷰, 평점을 기반으로 자신의 성향 파악 가능
- 자신이 작성한 평점과 리뷰 확인



#### Movie

* 추천 알고리즘을 통해 기본적인 영화 추천 가능
* 등록한 평점을 기반으로 새로운 영화 추천 알고리즘 구현
* 검색 기능을 통해 바로 원하는 영화에 접근 가능
* 원하는 기준으로 영화 목록을 볼 수 있음



#### Community

* 회원은 평점, 리뷰 등록 가능

* 자신의 리뷰에서 댓글을 통해 다른 유저들과 소통 가능

  



### 6. 배포 서버 URL

-



### 7. 기타(느낀점)

* 처음으로 1주일이라는 기간을 가지고 팀프로젝트를 진행했습니다. 저는 프론트엔드부분을 위주로 작업을 하게 되었는데, Vue를 쓸 때 컴포넌트를 구성하고 작업하는 것에 있어서 많은 어려움이 느껴졌습니다. 생각보다 많은 시간을 vue에서 쓰게 되어 디자인, ucc부분에 있어서 아쉬움이 크고, 좀 더 다양한 기능을 구현하지 못한 것이 아쉬웠습니다. 이 프로젝트를 통해서 백엔드 부분과 프론트 엔드 부분 모두 가능한 사람이 되고 싶다고 느꼈고, 이것을 시작으로 다양한 프로젝트를 진행해 보고 싶다는 생각이 들었습니다.

