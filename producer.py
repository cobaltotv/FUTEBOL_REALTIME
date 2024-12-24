import requests
from kafka import KafkaProducer
import json
import datetime as dt
import logging
import subprocess
import os
import time

# CONFIGURANDO O KAFKA
KAFKA_TOPIC = "eventos-futebol"
KAFKA_SERVER = "localhost:9092"

# CONFIGURANDO A API
API_URL = "https://api.football-data.org/v4/matches"
API_KEY = "7a4a6bafd8c34afca8266dd197924ccd"

# Caminhos para os scripts do Kafka
KAFKA_DIR = os.path.expanduser('~\\Kafka')
ZOOKEEPER_SCRIPT = os.path.join(KAFKA_DIR, 'bin\\windows\\zookeeper-server-start.bat')
KAFKA_SCRIPT = os.path.join(KAFKA_DIR, 'bin\\windows\\kafka-server-start.bat')
ZOOKEEPER_CONFIG = os.path.join(KAFKA_DIR, 'config\\zookeeper.properties')
KAFKA_CONFIG = os.path.join(KAFKA_DIR, 'config\\server.properties')

def start_zookeeper():
    """Inicia o Zookeeper"""
    print("Iniciando o Zookeeper...")
    subprocess.Popen([ZOOKEEPER_SCRIPT, ZOOKEEPER_CONFIG])
    time.sleep(15)  # Aumentado para garantir que o Zookeeper esteja pronto

def start_kafka():
    """Inicia o Kafka"""
    print("Iniciando o Kafka...")
    subprocess.Popen([KAFKA_SCRIPT, KAFKA_CONFIG])
    time.sleep(15)  # Aumentado para garantir que o Kafka esteja pronto

def get_matches():
    """Consulta a API para obter informações sobre as partidas ao vivo"""
    headers = {"X-Auth-Token": API_KEY}
    
    # Definindo o intervalo de datas
    today = dt.datetime.utcnow().date()
    yesterday = today - dt.timedelta(days=1)
    
    params = {
        "dateFrom": yesterday.strftime("%Y-%m-%d"),
        "dateTo": today.strftime("%Y-%m-%d")
    }
    
    logging.debug(f"Consultando a API com os parâmetros: {params}")
    
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        logging.debug(f"Resposta da API: {response.status_code} - {response.text}")
        if response.status_code == 200:
            matches = response.json().get("matches", [])
            logging.debug(f"Partidas encontradas: {matches}")
            return matches
        else:
            logging.error(f"Erro ao acessar a API: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição da API: {e}")
        return []

def send_to_kafka(producer, matches):
    """Envia dados das partidas ao Kafka com formatação melhorada"""
    for match in matches:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        score = match.get("score", {}).get("fullTime", {"home": None, "away": None})
        home_score = score.get("home", 0)  
        away_score = score.get("away", 0)

        # Formatação do evento
        evento = {
            "timestamp": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "descricao": f"{home_team} {home_score} a {away_score} {away_team}",
            "status": match.get("status", "DESCONHECIDO"),
            "placar": f"{home_score} x {away_score}"
        }

        try:
            producer.send(KAFKA_TOPIC, value=evento)
            logging.info(f"Enviado ao Kafka: {evento}")
        except Exception as e:
            logging.error(f"Erro ao enviar dados ao Kafka: {e}")

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Inicia o Zookeeper e o Kafka
    start_zookeeper()
    start_kafka()

    # Conecta ao Kafka
    producer = None
    while not producer:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            logging.info("Conectado ao Kafka com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao conectar ao Kafka: {e}")
            time.sleep(5)

    try:
        # Envia mensagens ao Kafka
        while True:
            matches = get_matches()
            if matches:
                send_to_kafka(producer, matches)
            else:
                logging.info("Nenhuma partida encontrada.")
            time.sleep(30)

    except KeyboardInterrupt:
        logging.info("Processo interrompido pelo usuário.")
    finally:
        if producer:
            producer.close()
            logging.info("Conexão com o Kafka encerrada.")

if __name__ == "__main__":
    main()
