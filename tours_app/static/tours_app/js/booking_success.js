// 複製訂單編號，讓使用者可以複製保存與查詢。
function copyOrderNumber() {
    const orderNum = document.getElementById('orderNumber').innerText;
    navigator.clipboard.writeText(orderNum).then(() => {
        alert('訂單編號已複製！');
    });
}
