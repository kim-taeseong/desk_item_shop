
![desker](https://github.com/kim-taeseong/desk_item_shop/assets/124543412/3e6f92e9-f614-4817-8f52-a1ad1b3fb01b)


# DESKER 
**DESKER**는 데스크 셋업에 관한 정보를 공유하는 커뮤니티와 데스크 셋업에 관련 상품을 판매/구매할 수 있는 Django 프로젝트입니다.

<br>

## 주요 기능
**1.로그인&회원가입**
- 구매자회원과 판매자회원 별도 회원가입을 지원합니다.
- 하나의 쇼핑몰 사이트에서 구매자, 판매자 기능 구현

<br>

**2.회원정보수정 & 회원탈퇴**
- 회원탈퇴 시, 바로 탈퇴되는 것이 아닌 일주일 후 탈퇴되도록 기능 구현

<br>

**3.상품 CRUD**
- 판매자 회원 계정으로 상품 등록, 수정, 삭제 기능 구현

<br>

**4.상품 review**
- 구매자 회원이 구매한 상품에 대한 리뷰 작성
- 별점 작성, 이미지 첨부 기능 구현

<br>

**5.상품 문의**
- 상품의 상세페이지에서 판매자에게 상품에 대한 문의 작성

<br>

**6.상품 카테고리별 상품 리스트**
- 상품의 카테고리에 따라 보이는 상품이 다르게 메인페이지 구축

<br>

**7.장바구니**
- 상품의 상세페이지에서 수량을 선택해 장바구니 담기
- 장바구니에 담긴 상품을 선택해 주문할 수 있도록 기능 구현

<br>

**8.상품 주문**
- 토스 결제 API를 이용해 결제 시스템 구현

<br>

**9.주문 결제**
- 도시&여행기간&동행자&여행스타일을 선택하면 AI가 여행일정을 추천해주는 기능입니다.
- 추천받은 일정을 내 여행에 저장할 수 있습니다.

<br>

**10.커뮤니티 게시판**
- 데스크셋업에 관한 정보 공유를 위한 커뮤니티 게시판
- 게시글 내에 `DESKER`에서 판매되고 있는 상품 링크 기능 구현
- 상품 링크를 통해 상품 상세페이지로 이동
- 게시글 좋아요 기능 구현
- 게시글 댓글, 댓글 좋아요 기능 구현
- 작성자 팔로우 기능 구현

<br>

**11.판매자 스토어페이지**
- 특정 판매자가 등록한 상품 리스트를 볼 수 있음
- 상품의 카테고리에 따라 보이는 상품이 다름
- 커뮤니티 게시글에서 특정 판매자의 상품이 링크 되었을 경우 `스타일링샷` 리스트에 해당 게시글이 보이도록 구현
- 구매자 고객일 경우, 해당 판매자 스토어찜 기능 구현

<br>

**12.구매자 마이페이지**
- 구매내역, 장바구니, 스토어찜, 팔로우/팔로잉 기능 연결

<br>

**13.판매자 마이페이지**
- 새로 등록한 상품 리스트 
- 판매중인 상품 문의에 대한 답변 작성
- 상품 등록, 수정, 판매 기능 연결

<br>

**14.고객센터**
- 쇼핑몰에 대한 문의를 할 수 있는 게시판
- 자주묻는질문 리스트
- 1대1 질문 작성, 수정, 삭제
- 1대1 질문 리스트

<br>

**15.유저 모델**
- `Django`의 `AbstractUser`를 사용하여 모델 생성
- `User` 모델을 생성해서 판매자와 구매자를 구분


## ERD
[**ERD**](https://www.erdcloud.com/d/2WNAohmnrMteJBife) 를 보려면 클릭하세요.

<br>

## 설치 및 실행 방법
**1.저장소 클론**
```
git clone https://github.com/kim-taeseong/desk_item_shop.git
cd desk_item_shop
```

**2.가상환경 설치 및 실행**
```
python -m venv desker
source momento/bin/activate  # mac
source momento\Scripts\activate  # window
```

**3.필요한 패키지 설치**
```
pip install -r requirements.txt
```

**4.데이터베이스 마이그레이션**
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic 
```

**5.서버실행**
```
python manage.py runserver
```

<br>

## 크레딧
이 프로젝트는 다음과 같은 오픈소스패키지를 사용합니다.
- python
- Django
- PostgreSQL
- Bootstrap5

<br>

## GitHub
`@anjiyoo`  ·  `@kim-taeseong`  ·  `@jongyongg`  ·  `@yeojin-0` 