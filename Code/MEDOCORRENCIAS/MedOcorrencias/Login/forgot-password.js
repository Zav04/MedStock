// Script de recuperação de senha
document.getElementById('forgotPasswordForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Simulação de envio de e-mail
    var email = document.getElementById('email').value;
    if (email) {
        alert('Instruções para recuperação de senha enviadas para ' + email);
        window.location.href = 'index.html'; // Redireciona de volta ao login
    } else {
        alert('Por favor, insira um e-mail válido.');
    }
});
