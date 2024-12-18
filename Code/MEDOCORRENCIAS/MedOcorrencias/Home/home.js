document.getElementById('occurrenceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    const paciente_nome = document.getElementById('patientName').value;
    const paciente_estado = document.getElementById('description').value;

    if (patientName && description) {
        // Dados a serem enviados
        const data = {
            user_id_pedido: 12,
            paciente_nome: paciente_nome,
            paciente_estado: paciente_estado
        };

        console.log('Enviando dados para a API:', data); // Log dos dados enviados

        // Envio para a API
        fetch('https://medstock-api-ce98.onrender.com/MedStock_CreateRequerimentoExterno/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            console.log('Status da resposta:', response.status);
            return response.json().then(data => {
                if (response.ok) {
                    alert('Ocorrência enviada com sucesso!');
                    console.log('Resposta da API:', data);
                } else {
                    throw new Error(`Erro ao enviar os dados para a API: ${data.message || 'Erro desconhecido'}`);
                }
            });
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao enviar a ocorrência. Por favor, tente novamente.');
        });
    } else {
        alert('Por favor, preencha todos os campos.');
    }
});
