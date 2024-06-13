// 상품 검색
function searchProduct(event) {
    event.preventDefault(); // 폼의 기본 동작 중지
    
    // 검색어 가져오기
    var query = document.getElementById('searchInput').value;
    console.log('query')
    console.log(query)

    // AJAX 요청
    var xhr = new XMLHttpRequest();
    var url = '/community/post/search/product/?product_name=' + encodeURIComponent(query);

    console.log('url')
    console.log(url)

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
    
    // 검색 결과를 순회하며 화면에 추가
    data.products.forEach(function(product) {
        // 검색을 클릭할 경우 검색 결과
        var resultItem = document.createElement('div');
        resultItem.textContent = product.product_name; // 상품의 이름으로 대체
        
        // 검색결과(상품명)을 클릭할 경우 하단 상품목록 영역에 선택된 상품 추가
        resultItem.addEventListener('click', function() {
            SearchResultAddProducts(product); // 상품목록에 상품을 1개 이상 추가하는 함수 호출
        });
        
        // 결과를 결과 컨테이너에 추가
        resultsContainer.appendChild(resultItem);
    });
}

// 상품목록에 상품을 1개 이상 추가하는 함수
function SearchResultAddProducts(product) {
    // 선택된 상품 목록의 DOM 요소 선택
    var selectionContainer = document.getElementById('selectedProductListContainer');
    
    // 선택된 상품을 나타내는 새로운 DOM 요소 생성
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

    // 삭제 버튼에 마우스를 올렸을 때의 스타일
    deleteButton.onmouseover = function() {
        deleteButton.style.backgroundColor = 'transparent'; // 배경색 투명하게 설정
        deleteButton.style.border = 'none'; // 테두리 없음
        deleteButton.style.padding = '0'; // 내부 여백 없음
        deleteButton.style.cursor = 'pointer'; // 커서 모양 변경
        deleteButton.style.backgroundColor = 'rgb(255, 0, 0)'; // 배경색 변경
        deleteButton.style.color = '#fff'; // 글자 색상 변경
        deleteButton.style.fontSize = '15px'; // 폰트 크기
        deleteButton.style.textDecoration = 'underline'; // 밑줄 추가
        deleteButton.style.marginLeft = '10px'; // 왼쪽 여백 추가
    };

    // 삭제 버튼에 마우스를 벗어났을 때의 스타일
    deleteButton.onmouseout = function() {
        deleteButton.style.backgroundColor = 'transparent'; // 배경색 투명하게 설정
        deleteButton.style.border = 'none'; // 테두리 없음
        deleteButton.style.padding = '0'; // 내부 여백 없음
        deleteButton.style.cursor = 'pointer'; // 커서 모양 변경
        deleteButton.style.color = 'rgb(165, 165, 165)'; // 글자 색상
        deleteButton.style.fontSize = '15px'; // 폰트 크기
        deleteButton.style.textDecoration = 'underline'; // 밑줄 추가
        deleteButton.style.marginLeft = '10px'; // 왼쪽 여백 추가
    };

    // 삭제 버튼에 클릭 이벤트 추가
    deleteButton.onclick = function() {
        // 삭제 버튼을 클릭하면 해당 상품을 삭제
        selectionContainer.removeChild(selectedProduct);
        UpdateSelectedProducts(); // 선택된 상품 목록 업데이트
    };

    // 선택된 상품에 삭제 버튼 추가
    selectedProduct.appendChild(deleteButton);
    
    // 선택된 상품을 선택된 상품 목록에 추가
    selectionContainer.appendChild(selectedProduct);
    
    // 선택된 상품이 추가되었으므로 "선택된 상품이 없습니다" 문구를 숨김
    var noSelectedProductMessage = document.getElementById('noSelectedProductMessage');
    noSelectedProductMessage.style.display = 'none';

    UpdateSelectedProducts(); // 선택된 상품 목록 업데이트
}


function getCookie(cookieName) {
    let name = cookieName + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


// 선택된 상품 목록을 서버로 보내는 함수
function UpdateSelectedProducts() {
    let cookieValue = getCookie("getCookie");
    var selectionContainer = document.getElementById('selectedProductListContainer');
    var selectedProducts = selectionContainer.querySelectorAll('div');
    var selectedProductIds = [];

    selectedProducts.forEach(function(product) {
        selectedProductIds.push(product.textContent.replace(' 삭제', ''));
    });

    var xhr = new XMLHttpRequest();
    var url = '/community/post/selected/product/';
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // CSRF 토큰 설정

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            var data = JSON.parse(xhr.responseText);
            console.log(data.message); // 서버로부터의 응답 메시지
        } else {
            console.error('요청이 실패했습니다');
        }
    };
}
