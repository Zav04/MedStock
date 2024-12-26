document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', handleLogin);
});

function handleLogin(event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Dados a serem enviados
    const data = {
        email: email,
        password: password
    };

    console.log('Enviando dados para a API:', data); // Log dos dados enviados

    // Envio para a API
    fetch((config.API_URL) + (config.API_LOGIN), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        return response.json().then(data => {
            if (response.ok) {
                if (data.response) { // Verifica se response é true
                    const userId = data.data.utilizador_id;
                    if (userId != null) {
                        localStorage.setItem('user_id', userId);
                    }
                    window.location.href = '../Home/home.html';
                } else {
                    alert(data.error || 'Erro ao realizar login.');
                }
            } else {
                alert('Erro: ' + (data.error || response.statusText));
            }
        });
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao fazer login. Por favor, tente novamente.');
    });
}
