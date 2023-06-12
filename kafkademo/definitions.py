from dagster import asset, sensor, Definitions, RunRequest, RunConfig, Config, OpExecutionContext, define_asset_job, AssetSelection, DefaultSensorStatus

from kafkademo.resources import KafkaResource
from kafkademo.sensors import watch_kafka
from kafkademo.assets import loaded_from_kafka, downstream_of_kafka

defs = Definitions(
    assets=[loaded_from_kafka],
    jobs=[downstream_of_kafka],
    sensors=[watch_kafka],
    resources={
        'kafka': KafkaResource(bootstrap_servers=['localhost:9092'], topic_name='First_Topic')
    }
)