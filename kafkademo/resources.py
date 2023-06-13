from kafka import KafkaConsumer
from dagster import ConfigurableResource
from typing import List

class KafkaResource(ConfigurableResource):
    bootstrap_servers: List[str]
    topic_name: str

    def get_consumer(self):
       return KafkaConsumer(self.topic_name, group_id='group1', bootstrap_servers=self.bootstrap_servers, fetch_min_bytes=4000)