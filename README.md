# desk_item_shop

### 24-04-29 지안
#### 구매자, 판매자 회원정보 수정 기능 추가
#### 유저 비밀번호 수정 기능 추가

*****

### 24-04-30 지안
#### 상품등록 : 실제 데이터 등록
#### 스토어ID로 로그인 시, 상품조회/상품등록 링크 추가
#### 각 스토어별로 등록한 상품 보이도록 models/views/템플릿 수정
##### ㄴ> 필요없는 템플릿 삭제 : logistics/add(create), list, detail, update, delete 외 삭제
##### ㄴ> 템플릿명 변경 : logistics/add.html -> logistics/create.html
##### ㄴ> 템플릿 수정 : logistics/list.html, logistics/add.html 해당 스토어 표시, 테이블 내 할인율 상품수정 추가, 상품등록 추가

*****

### 24-05-02 지안
#### 홈페이지 메인페이지 생성 -> logistics/templates/main.html
#### customer 메인 페이지 수정
#### store 메인 페이지/상품 페이지 수정
#### base.html 수정
#### noncategory_base.html -> 사이드바 제외
#### customer_base.html -> 사이드바에 상품 카테고리
#### store_base.html -> 사이드바 제외, 스토어와 다른 nav
#### static/style.css 수정