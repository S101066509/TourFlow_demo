/**
 * demo_page - 全站 JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {

    // === Auto-dismiss Alerts ===
    // 成功或提示訊息 5 秒後自動關閉
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // === Back to Top Button ===
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
        backToTopBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // === Checkout: 動態計算總價 ===
    const paxInput = document.getElementById('id_pax');
    const priceDisplay = document.getElementById('dynamicTotalPrice');
    const unitPrice = document.getElementById('unitPriceValue');

    if (paxInput && priceDisplay && unitPrice) {
        const price = parseInt(unitPrice.textContent.replace(/[^\d]/g, ''), 10);
        paxInput.addEventListener('input', function () {
            const pax = parseInt(paxInput.value, 10) || 0;
            const total = price * pax;
            priceDisplay.textContent = 'NT$ ' + total.toLocaleString();
        });
    }

});
