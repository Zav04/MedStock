document
  .getElementById("occurrenceForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    const nome = document.getElementById("patientName").value;
    const estado = document.getElementById("description").value;
    const user_id = localStorage.getItem("user_id");

    if (nome && estado) {
      // Dados a serem enviados
      const data = {
        user_id_pedido: user_id,
        paciente_nome: nome,
        paciente_estado: estado,
      };

      console.log("Enviando dados para a API:", data); // Log dos dados enviados

      // Envio para a API
      fetch(config.API_URL + config.API_CreateRequerimentoExterno, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          console.log("Status da resposta:", response.status);
          return response.json().then((data) => {
            if (response.ok) {
              alert("Ocorrência enviada com sucesso!");
              console.log("Resposta da API:", data);
            } else {
              throw new Error(
                "Erro ao enviar os dados para a API:" +
                  (data.message || "Erro desconhecido")
              );
            }
          });
        })
        .catch((error) => {
          console.error("Erro:", error);
          alert("Erro ao enviar a ocorrência. Por favor, tente novamente.");
        });
    } else {
      alert("Por favor, preencha todos os campos.");
    }
  });
