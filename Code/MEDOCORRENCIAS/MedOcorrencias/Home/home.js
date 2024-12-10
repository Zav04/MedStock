// home.js
document.getElementById('occurrenceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    const description = document.getElementById('description').value;

    if (description) {
        alert('Ocorrência enviada: ' + description);
        // Aqui você pode adicionar o código para enviar a ocorrência ao servidor
    } else {
        alert('Por favor, descreva a ocorrência.');
    }
});
