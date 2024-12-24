from kafka import KafkaConsumer
import json
import logging

# CONFIGURANDO O KAFKA
KAFKA_TOPIC = "eventos-futebol"
KAFKA_SERVER = "localhost:9092"

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=None,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logging.info("Consumidor iniciado. Aguardando mensagens...")

        for message in consumer:
            logging.info(f"Mensagem recebida: {message.value}")

    except Exception as e:
        logging.error(f"Erro no consumidor Kafka: {e}")

if __name__ == "__main__":
    main()
    
