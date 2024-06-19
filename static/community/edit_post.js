document.addEventListener('DOMContentLoaded', function() {
    // 초기 선택된 상품을 전역 배열에 저장
    window.selectedProducts = [...(initialSelectedProducts || [])];
    console.log('초기 선택된 상품 initialSelectedProducts', initialSelectedProducts);

    // 페이지 로드 시 초기 선택된 상품 목록 렌더링
    window.selectedProducts.forEach(product => {
        addProductToSelection(product, false); // 두 번째 인자로 렌더링 여부 전달
    });

    // 폼 제출 시 선택된 상품 목록 업데이트
    document.querySelector('form').addEventListener('submit', function() {
        listToHiddenInput();
    });
});

// CSRF 토큰 가져오기 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// 검색 버튼 클릭 시 상품 검색 함수 호출
document.getElementById('searchButton').addEventListener('click', searchProduct);

// 상품 검색 함수
function searchProduct(event) {
    event.preventDefault();  // 기본 폼 제출 동작 방지

    const query = document.getElementById('searchInput').value;
    const xhr = new XMLHttpRequest();
    const url = '/community/post/search/product/';

    const formData = new FormData();
    formData.append('product_name', query);

    xhr.open('POST', url, true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            const data = JSON.parse(xhr.responseText);
            renderSearchResults(data);
        } else {
            console.error('요청 실패');
        }
    };
    xhr.send(formData);
}

// 검색 결과 렌더링 함수
function renderSearchResults(data) {
    const resultsContainer = document.getElementById('searchedProductList');
    resultsContainer.innerHTML = ''; // 이전 결과 초기화

    const filteredProducts = data.products.filter(product => 
        !selectedProducts.some(selectedProduct => 
            selectedProduct.product_id === product.product_id
        )
    );

    filteredProducts.forEach(product => {
        const resultItem = document.createElement('div');
        resultItem.textContent = product.product_name;
        resultItem.addEventListener('click', () => {
            addProductToSelection(product);
        });
        resultsContainer.appendChild(resultItem);
    });
}

// 선택된 상품 목록 렌더링 함수
function renderSelectedProducts() {
    const selectedProductList = document.getElementById('selectedProductList');
    selectedProductList.innerHTML = ''; // 기존 목록 초기화

    selectedProducts.forEach(product => {
        const selectedProduct = document.createElement('div');
        selectedProduct.textContent = product.product_name;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '삭제';
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

        deleteButton.onclick = function() {
            selectedProducts = selectedProducts.filter(selectedProduct => selectedProduct.product_id !== product.product_id);
            renderSelectedProducts();
            listToHiddenInput();
            console.log('삭제버튼 클릭 시 selectedProducts', selectedProducts);
        };

        selectedProduct.appendChild(deleteButton);
        selectedProductList.appendChild(selectedProduct);
    });
}

// 상품 선택 함수
function addProductToSelection(product, shouldRender = true) {
    if (!product || !product.product_name || !product.product_id) return;
    if (selectedProducts.some(selectedProduct => selectedProduct.product_id === product.product_id)) return;

    selectedProducts.push(product);
    if (shouldRender) renderSelectedProducts();
    listToHiddenInput();
}

// 선택된 상품 목록을 hidden input에 저장하는 함수
function listToHiddenInput() {
    const selectedProductIds = selectedProducts.map(selectedProduct => selectedProduct.product_id);
    const hiddenInput = document.getElementById('hiddenInput');
    hiddenInput.value = JSON.stringify(selectedProductIds);
    console.log('json 문자열 형태로 서버에 전송 selectedProductIds', selectedProductIds);
}

// 초기 선택된 상품 목록에서 상품 삭제 함수
function deleteProduct(productName) {
    const selectedProductList = document.getElementById('selectedProductList');
    const selectedProductItems = selectedProductList.children;

    for (let item of selectedProductItems) {
        if (item.textContent.includes(productName)) {
            selectedProductList.removeChild(item);
            break;
        }
    }

    selectedProducts = selectedProducts.filter(product => product.product_name !== productName);

    const messageElement = document.getElementById('noSelectedProductMessage');
    messageElement.style.display = selectedProducts.length === 0 ? 'block' : 'none';

    listToHiddenInput();
}
