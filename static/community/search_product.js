// 선택된 상품 목록을 유지하기 위한 배열
var selectedProducts = [];

// 상품 검색
function searchProduct(event) {
    event.preventDefault(); // 폼의 기본 동작 중지
    
    // 검색어 가져오기
    var query = document.getElementById('searchInput').value;

    // AJAX 요청
    var xhr = new XMLHttpRequest();
    var url = '/community/post/search/product/?product_name=' + encodeURIComponent(query);

    xhr.open('GET', url, true);
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            var data = JSON.parse(xhr.responseText);
            SearchResults(data);  // 검색 결과를 화면에 표시하는 함수 호출
        } else {
            console.error('Request failed');
        }
    };
    xhr.send();
}

// 검색 버튼 요소 선택
var searchButton = document.getElementById('searchButton');

// 검색 버튼 클릭 이벤트에 searchProduct 함수 바인딩
searchButton.addEventListener('click', searchProduct);

// 검색 결과를 화면에 표시하는 함수
function SearchResults(data) {
    // 결과를 표시할 DOM 요소 선택
    var resultsContainer = document.getElementById('searchedProductList');

    // 이전 결과 지우기
    resultsContainer.innerHTML = '';
    
    // 선택된 상품 목록을 사용하여 검색 결과를 필터링
    var filteredProducts = data.products.filter(function(product) {
        return !selectedProducts.some(function(selectedProduct) {
            return selectedProduct.product_name === product.product_name;
        });
    });

    // 필터링된 검색 결과를 순회하며 화면에 추가
    filteredProducts.forEach(function(product) {
        // 검색을 클릭할 경우 검색 결과
        var resultItem = document.createElement('div');
        resultItem.textContent = product.product_name; // 상품의 이름으로 대체
        
        // 검색결과(상품명)을 클릭할 경우 하단 상품목록 영역에 선택된 상품 추가
        resultItem.addEventListener('click', function() {
            SearchResultAddProducts(product); // 상품목록에 상품 추가하는 함수
        });
        
        // 결과를 결과 컨테이너에 추가
        resultsContainer.appendChild(resultItem);
    });
}

// 상품목록에 상품 추가하는 함수
function SearchResultAddProducts(product) {
    // 선택된 상품이 표시되는 영역
    var selectionContainer = document.getElementById('selectedProductListContainer');

    // 선택된 상품을 화면에 표시
    var selectedProduct = document.createElement('div');
    selectedProduct.textContent = product.product_name; // 선택된 상품의 이름으로 대체

    // 삭제 버튼 생성
    var deleteButton = document.createElement('button');
    deleteButton.textContent = '삭제';

    // 삭제 버튼에 직접 스타일 적용
    deleteButton.style.backgroundColor = 'transparent'; // 배경색 투명하게 설정
    deleteButton.style.border = 'none'; // 테두리 없음
    deleteButton.style.padding = '0'; // 내부 여백 없음
    deleteButton.style.cursor = 'pointer'; // 커서 모양 변경
    deleteButton.style.color = 'rgb(165, 165, 165)'; // 글자 색상
    deleteButton.style.fontSize = '15px'; // 폰트 크기
    deleteButton.style.textDecoration = 'underline'; // 밑줄 추가
    deleteButton.style.marginLeft = '10px'; // 왼쪽 여백 추가

    // 삭제 버튼에 클릭 이벤트 추가
    deleteButton.onclick = function() {
        // 삭제 버튼을 클릭하면 해당 상품을 삭제
        selectionContainer.removeChild(selectedProduct);
        // 선택된 상품 목록에서도 제거
        selectedProducts = selectedProducts.filter(function(selected) {
            return selected.product_name !== product.product_name;
        });
    };

    // 선택된 상품에 삭제 버튼 추가
    selectedProduct.appendChild(deleteButton);
    
    // 선택된 상품을 선택된 상품 목록에 추가
    selectionContainer.appendChild(selectedProduct);
    
    // 선택된 상품 목록에 추가
    selectedProducts.push(product);
    
    // 선택된 상품이 추가되었으므로 "선택된 상품이 없습니다" 문구를 숨김
    var noSelectedProductMessage = document.getElementById('noSelectedProductMessage');
    noSelectedProductMessage.style.display = 'none';
}

// '작성완료' 버튼에 클릭 이벤트 추가
var completeButton = document.getElementById('completeButton');
completeButton.addEventListener('click', function() {
    sendDataToServer(); // 데이터를 서버로 전송하는 함수 호출
});

// 선택된 상품 데이터 서버로 전송
function sendDataToServer() {
    var xhr = new XMLHttpRequest();
    var url = '/community/post/create/';

    xhr.open('POST', url, true);

    // CSRF 토큰 가져오기
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    // CSRF 토큰을 HTTP 헤더에 포함
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            var response = JSON.parse(xhr.responseText);
            console.log(response.message); // 성공 메시지 출력
            // 데이터 전송 성공 후 선택된 상품 목록 초기화 등의 추가 작업 가능
        } else {
            console.error('데이터 전송에 실패했습니다');
        }
    };

    xhr.onerror = function() {
        console.error('데이터 전송 중 오류가 발생했습니다');
    };

    // 선택된 상품id를 JSON 형식으로 변환하여 전송
    var selectedProductIds = selectedProducts.map(function(product) {
        return product.product_id;
    });

    var dataToSend = JSON.stringify({ 'selected_product_ids': selectedProductIds });
    console.log('dataToSend:', dataToSend);
    xhr.send(dataToSend);
}

// '작성완료' 버튼에 클릭 이벤트 추가
var completeButton = document.getElementById('completeButton');
completeButton.addEventListener('click', function() {
    sendDataToServer(); // 데이터를 서버로 전송하는 함수 호출
});
