// Evento para mostrar a página de login ao clicar no botão
document.getElementById('loginButton').addEventListener('click', function() {
    // Esconde a página inicial
    document.getElementById('introPage').style.display = 'none';
    
    
});

// Redireciona para a página de login
document.getElementById('loginButton').addEventListener('click', function() {
    // Caminho relativo: saindo da pasta "Intro Page" e indo para "Login/login.html"
    window.location.href = '../Login/login.html';  
});



