# Sistema de gestão de Casa de Sementes

Este projeto apresenta um sistema de gestão para uma Casa de Sementes, integrado a um Sistema de Monitoramento de Umidade e Temperatura. O sistema de monitoramento foi desenvolvido em conjunto com este projeto, utilizando Arduíno e sensores de temperatura e umidade DHT22. Para acessar o projeto de monitoramento, você pode visitar o seguinte link: https://github.com/pedrohs21/monitor-casa-de-sementes. 

O objetivo deste projeto é fornecer uma plataforma para o gerenciamento e monitoramento de uma casa de sementes, permitindo um controle mais eficiente e moderno, permitindo que os usuários visualizem dados em tempo real e recebam alertas quando os níveis de umidade ou temperatura estiverem fora dos valores adequados.

## Funcionalidades

- Cadastro de sementes: permite cadastrar as sementes que estão armazenadas na Casa de Sementes, incluindo informações como variedade, espécie, data de validade, quantidade, etc.
- Monitoramento de umidade e temperatura: o sistema se conecta ao Sistema de Monitoramento que através de sensores de umidade e temperatura instalados na Casa de Sementes fornecem dados em tempo real. Os dados são exibidos em gráficos para facilitar a visualização.
- Alertas: quando os níveis de umidade ou temperatura estiverem fora dos valores adequados, o sistema enviará alertas para os usuários cadastrados.
- Relatórios: o sistema gera relatórios periódicos com informações sobre o estado das sementes armazenadas na casa de sementes, permitindo que os usuários avaliem a qualidade das sementes e identifiquem possíveis problemas.
- Histórico: o sistema armazena um histórico de dados de umidade e temperatura para permitir que os usuários analisem tendências ao longo do tempo e identifiquem padrões, além de também armazenar um histórico dos diferentes tipos de testes realizados nas sementes, como por exemplo, testes de germinação.

## Tecnologias utilizadas

- Linguagem de programação: Python
- Framework: Django
- Banco de dados: PostgreSQL
- Front-end: HTML, CSS, JavaScript e Bootstrap

## Instalação

Para instalar o sistema, siga os passos abaixo:

1. Clone este repositório em sua máquina local.
2. Crie um ambiente virtual python e ative-o.
3. Instale as dependências executando o comando `pip install -r requirements.txt`.
4. Execute o script `server-dev.sh`.
5. Acesse o sistema em `http://localhost:8000`.
