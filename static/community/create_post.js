// 선택된 상품 목록을 유지하기 위한 배열
var selectedProducts = [];

// CSRF 토큰 가져오기 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// searchButton 버튼이 클릭될 때 searchProduct 함수 호출
document.getElementById('searchButton').addEventListener('click', searchProduct);

// 상품 검색 함수
function searchProduct(event) {
    event.preventDefault(); // 폼의 기본 동작 중지 (페이지 새로고침 없이 AJAX 요청을 통해 검색을 수행)

    // searchInput 입력 필드에서 검색어 가져오기
    const query = document.getElementById('searchInput').value;

    // AJAX 요청
    const xhr = new XMLHttpRequest(); // 새로운 XMLHttpRequest 객체 생성
    const url = '/community/post/search/product/'; // 검색 요청 보내는 URL

    // 폼데이터 객체 생성
    const formData = new FormData(); // 폼데이터 객체 생성
    formData.append('product_name', query); // 검색어를 product_name 필드에 추가 (서버로 전송될 데이터)

    xhr.open('POST', url, true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken); // CSRF 토큰 추가
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            const data = JSON.parse(xhr.responseText);
            renderSearchResults(data);  // 검색 결과를 화면에 표시하는 함수 호출
        } else {
            console.error('요청 실패');
        }
    };
    xhr.send(formData); // 폼데이터 전송
}

// 검색 결과를 화면에 표시하는 함수
function renderSearchResults(data) {
    // 결과를 표시할 DOM 요소 선택
    const resultsContainer = document.getElementById('searchedProductList');

    // 이전 결과 지우기
    resultsContainer.innerHTML = '';

    // 선택된 상품 목록을 사용하여 검색 결과를 필터링
    const filteredProducts = data.products.filter(product => 
        !selectedProducts.some(selectedProduct => 
            selectedProduct.product_name === product.product_name
        )
    );

    // 필터링된 검색 결과를 순회하며 화면에 추가
    filteredProducts.forEach(product => {
        const resultItem = document.createElement('div');
        resultItem.textContent = product.product_name; // 상품의 이름으로 대체

        resultItem.addEventListener('click', () => {
            addProductToSelection(product); // 상품목록에 상품 추가하는 함수
        });

        resultsContainer.appendChild(resultItem);
    });
}

// 선택된 상품목록에 상품 추가하는 함수
function addProductToSelection(product) {
    // 선택된 상품이 표시되는 영역
    const selectionContainer = document.getElementById('selectedProductListContainer');

    // 선택된 상품을 화면에 표시
    const selectedProduct = document.createElement('div');
    selectedProduct.textContent = product.product_name; // 선택된 상품의 이름으로 대체

    // 삭제 버튼 생성
    const deleteButton = document.createElement('button');
    deleteButton.textContent = '삭제';

    // 삭제 버튼에 직접 스타일 적용
    Object.assign(deleteButton.style, {
        backgroundColor: 'transparent',
        border: 'none',
        padding: '0',
        cursor: 'pointer',
        color: 'rgb(165, 165, 165)',
        fontSize: '15px',
        textDecoration: 'underline',
        marginLeft: '10px'
    });

    // 삭제 버튼에 클릭 이벤트 추가
    deleteButton.onclick = () => {
        // 삭제 버튼을 클릭하면 해당 상품을 삭제
        selectionContainer.removeChild(selectedProduct);
        // 선택된 상품 목록에서도 제거
        selectedProducts = selectedProducts.filter(selected => selected.product_name !== product.product_name);

        // 선택된 상품이 모두 제거되면 "선택된 상품이 없습니다" 메시지 표시
        if (selectedProducts.length === 0) {
            document.getElementById('noSelectedProductMessage').style.display = 'block';
        }
        
        // 선택된 상품 목록을 hidden input에 업데이트
        listToHiddenInput();
    };

    // 선택된 상품에 삭제 버튼 추가
    selectedProduct.appendChild(deleteButton);

    // 선택된 상품을 선택된 상품 목록에 추가
    selectionContainer.appendChild(selectedProduct);

    // 선택된 상품 목록에 추가
    selectedProducts.push(product);

    // 선택된 상품이 추가되었으므로 "선택된 상품이 없습니다" 문구를 숨김
    document.getElementById('noSelectedProductMessage').style.display = 'none';

    // 선택된 상품 목록을 hidden input에 업데이트
    listToHiddenInput();
}

// 리스트를 JSON 문자열로 반환하여 hidden input에 저장 (템플릿에서 HTML 폼이 제출될 때, 서버로 자동으로 전송)
function listToHiddenInput() {
    const selectedProductIds = selectedProducts.map(selectedProduct => selectedProduct.product_id);
    console.log('selectedProducts')
    console.log(selectedProducts)

    const hiddenInput = document.getElementById('hiddenInput');
    hiddenInput.value = JSON.stringify(selectedProductIds);
    console.log('hiddenInput')
    console.log(hiddenInput)
}
