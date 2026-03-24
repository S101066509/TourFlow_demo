// 密碼顯示切換
document.querySelector('#togglePassword').addEventListener('click', function (e) {
    const password = document.querySelector('#id_password');
    const icon = this.querySelector('i');
    if (password.type === 'password') {
        password.type = 'text';
        icon.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        password.type = 'password';
        icon.classList.replace('bi-eye-slash', 'bi-eye');
    }
});
