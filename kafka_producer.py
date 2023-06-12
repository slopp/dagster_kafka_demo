from kafka import KafkaProducer
from datetime import datetime 
import time

# Inputs
DESIRED_THROUGHPUT_PER_SECOND = 10
bootstrap_servers = ['localhost:9092']
topicName = 'First_Topic'

def _print_throughput(i, tstart, DESIRED_THROUGHPUT_PER_SECOND):
    """ Prints the throughput of events pushed to kafka"""
    if i % DESIRED_THROUGHPUT_PER_SECOND == 0:
        print(f"Posted {DESIRED_THROUGHPUT_PER_SECOND} messages in {(datetime.now() - tstart).seconds} seconds")
        tstart = datetime.now()
    return tstart
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

tstart = datetime.now()
for i in range(0,1000):
    producer.send(topicName, bytes(f'Message {i}', 'utf-8'))    
    time.sleep(1/DESIRED_THROUGHPUT_PER_SECOND)
    tstart = _print_throughput(i, tstart, DESIRED_THROUGHPUT_PER_SECOND)




