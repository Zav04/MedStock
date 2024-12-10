document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', handleLogin);
});

function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simulando uma verificação de login
    if (username === 'admin' && password === '1234') {
        // Redireciona para a página HOME
        window.location.href = '../Home/home.html';
    } else {
        alert('Nome de utilizador ou senha incorretos!');
    }
}
