# desk_item_shop

### 24-04-26 준호
### 구매자,판매자 로그인 및 회원가입 기능
### 이메일을 통해 아이디 찾기 기능
### 회원가입 시, 아이디,비밀번호 유효성검사 및 안내메시지, 플레이스 홀더
### 구매자 및 판매자 홈페이지 일단 제거
### requirements.txt 최신화

### 24-04-27 준호
#### 비밀번호 초기화 기능 - 진행중
#### 회원 정보 수정 기능 - 진행중(지안님 담당?)
#### 회원 탈퇴 기능 - 진행중
#### 지안님 확인을 위한 임시 기능 구현 판매자 로그인 > 상품 등록 > 등록 완료 후 상품 리스트 페이지(주석 풀고 확인하시면 됩니다)
#### LOGIN_URL 주석처리, users/urls.py 수정으로 http://127.0.0.1:8000/ 진입하면 로그인 페이지 나오게 수정
#### 회원가입 완료(signup_done.html) 페이지 생성
#### 고객 회원가입 페이지에서 생년월일 선택을 DateInput 위젯을 사용하도록 수정
#### 회원가입 페이지에서 가입일 > 연락처, 사용자이름 > 아이디 및 자잘한 버그,오타 수정

### 24-04-29 지안
#### 구매자, 판매자 회원정보 수정 기능 추가
#### 유저 비밀번호 수정 기능 추가 

### 24-04-30 지안
#### 상품등록 : 실제 데이터 등록
#### 스토어ID로 로그인 시, 상품조회/상품등록 링크 추가
#### 각 스토어별로 등록한 상품 보이도록 models/views/템플릿 수정
##### ㄴ> 필요없는 템플릿 삭제 : logistics/add(create), list, detail, update, delete 외 삭제
##### ㄴ> 템플릿명 변경 : logistics/add.html -> logistics/create.html
##### ㄴ> 템플릿 수정 : logistics/list.html, logistics/add.html 해당 스토어 표시, 테이블 내 할인율 상품수정 추가, 상품등록 추가
