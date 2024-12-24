# FLUXO DE DADOS EM TEMPO REAL PARA EVENTOS DE FUTEBOL

## VISÃO GERAL

Este projeto é um sistema de fluxo de dados em tempo real desenvolvido para capturar, processar e consumir eventos relacionados a partidas de futebol, como gols, substituições, cartões e resultados. Utilizando Apache Kafka como backbone do fluxo de dados, o sistema garante baixa latência, escalabilidade e alta disponibilidade para aplicações que necessitam de informações atualizadas em tempo real.

## TECNOLOGIAS UTILIZADAS

### LINGUAGEM E FERRAMENTAS

- **Python**: Para implementação dos produtores e consumidores de dados.
- **Apache Kafka**: Para o gerenciamento de mensagens em tempo real.

### BIBLIOTECAS PYTHON

- **kafka-python**: Integração entre Python e Apache Kafka.
- **logging**: Para monitoramento e depuração do sistema.
- **json**: Para serialização e deserialização de mensagens.

## ESTRUTURA DO PROJETO

### ARQUIVOS PRINCIPAIS

- **producer.py**: Envia eventos simulados de partidas de futebol para um tópico Kafka.
- **consumer.py**: Consome mensagens do tópico Kafka e processa os eventos recebidos.
- **docker-compose.yml**: Configura o ambiente do Kafka, incluindo o broker e o zookeeper.

### TÓPICO KAFKA

- **Nome**: eventos-futebol
- **Descrição**: Centraliza os eventos de futebol para consumo em tempo real.

## CONFIGURAÇÃO E EXECUÇÃO

### REQUISITOS

- Docker e Docker Compose instalados.
- Python 3.8 ou superior.
- Apache Kafka configurado localmente ou via Docker.

### PASSOS PARA CONFIGURAÇÃO

1. Clone o repositório:
    ```sh
    git clone https://github.com/cobaltotv/FUTEBOL_REALTIME.git
    cd seu-repositorio
    ```

2. Inicie o ambiente Kafka com Docker Compose:
    ```sh
    docker-compose up -d
    ```

3. Instale as dependências Python:
    ```sh
    pip install -r requirements.txt
    ```

4. Execute o produtor de dados:
    ```sh
    python producer.py
    ```

5. Em outra janela do terminal, execute o consumidor:
    ```sh
    python consumer.py
    ```

## FUNCIONAMENTO

### PRODUCER (PRODUTOR)

- O `producer.py` gera eventos simulados de partidas de futebol.
- Envia mensagens JSON para o tópico Kafka `eventos-futebol`.

### CONSUMER (CONSUMIDOR)

- O `consumer.py` consome as mensagens do tópico Kafka.
- Processa e exibe os eventos recebidos em tempo real no terminal.

## LOGS E MONITORAMENTO

O sistema utiliza o módulo `logging` para registrar eventos e diagnósticos.

- **Producer**: Registra eventos enviados ao Kafka.
- **Consumer**: Registra eventos consumidos do Kafka.

### EXEMPLOS DE LOGS

- **Producer**: `2024-12-23 22:00:00 - producer - INFO - Evento enviado: {"jogo": "Time A vs Time B", "evento": "gol"}`
- **Consumer**: `2024-12-23 22:01:00 - consumer - INFO - Recebido do Kafka: {"jogo": "Time A vs Time B", "evento": "gol"}`

## POSSÍVEIS MELHORIAS

- Integração com um banco de dados para armazenar os eventos.
- Desenvolvimento de um dashboard em tempo real para visualização dos eventos.
- Implementação de mecanismos de alertas automáticos para eventos importantes.

## CONTRIBUIÇÃO

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias, correções ou novas funcionalidades.

## LICENÇA

Este projeto está licenciado sob a Licença MIT.

Desenvolvido por [Guilherme]⚽. Obrigado!
