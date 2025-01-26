from kafka import KafkaProducer
import json
import os

# Kafka 설정
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

# Kafka 프로듀서 생성
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def send_to_kafka(topic: str, message: dict):
    """
    Kafka로 메시지 전송
    :param topic: Kafka 토픽 이름
    :param message: 전송할 메시지
    """
    try:
        producer.send(topic, value=message)
        producer.flush()
    except Exception as e:
        raise
