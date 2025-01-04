# **MedStock - Gestão de Stock para Farmácias Hospitalares**



![Logo_With_BackGround](https://github.com/user-attachments/assets/ecec2fa5-30ec-43c5-a47f-153f2789a703)

O **MedStock** é um sistema desenvolvido para facilitar a gestão de stock em farmácias hospitalares, otimizando processos internos e a comunicação entre diferentes departamentos. Este sistema permite o controlo eficiente de medicamentos, vacinas, materiais cirúrgicos, entre outros consumíveis, além de oferecer funcionalidades para o envio automatizado de pedidos a fornecedores.

## Funcionalidades Principais

- **Gestão de Stock**
  - Controlo detalhado de medicamentos, vacinas, materiais cirúrgicos e outros consumíveis hospitalares.

- **Gestão de Pedidos Internos**
  - Permite o envio e controlo de pedidos realizados pelos diferentes departamentos hospitalares.

- **Redistribuição de Consumíveis**
  - Sistema de redistribuição automática entre requerimentos para atender a requisições urgentes.

- **Simulador de Pedidos Externos**
  - Ferramenta para criação e controlo de pedidos provenientes de serviços de emergência.

- **Gestão de Pedidos a Fornecedores**
  - Mecanismo para envio automático de requisições a fornecedores.

- **Relatórios e Visualização de Dados**
  - Geração de relatórios detalhados sobre níveis de stock, requisições e redistribuições realizadas.

## Arquitetura do Sistema

O MedStock foi desenvolvido com base em uma arquitetura orientada a serviços (SOA), garantindo a interoperabilidade e a escalabilidade do sistema.

- **Interface Gráfica (Desktop)**
  - Desenvolvida em PyQt para oferecer uma experiência de utilizador fluida e intuitiva.

- **Aplicação Móvel**
  - Aplicação em Kotlin para dispositivos Android, focada em validações de stock e gestão de consumíveis.

- **API Backend**
  - Construída com FastAPI para gerir a comunicação entre o Front-End e a base de dados.

- **Simuladores Web**
  - Simuladores específicos para pedidos externos e a fornecedores, desenvolvidos em HTML, CSS e JavaScript.

- **MedSupply**
  - Um simulador adicional para pedidos a fornecedores, desenvolvido em React, com uma API em Flask para facilitar a simulação dos processos de reabastecimento de stock.

- **Base de Dados**
  - Gerida em PostgreSQL, assegurando a integridade e eficiência na gestão de grandes volumes de dados.

## Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada no desenvolvimento do projeto.
- **PyQt**: Framework para a interface gráfica desktop.
- **FastAPI**: Framework para a criação da API REST.
- **PostgreSQL**: Sistema de base de dados relacional robusto e escalável.
- **Kotlin**: Utilizado no desenvolvimento da aplicação móvel **MedReader**.
- **HTML, CSS, JavaScript**: Utilizado no desenvolvimento da plantaforma  **MedOcorrencias**.
- **React**: Utilizado no simulador de pedidos a fornecedores, **MedSupply**.
- **Flask**: Framework para a API do simulador **MedSupply**.

    


