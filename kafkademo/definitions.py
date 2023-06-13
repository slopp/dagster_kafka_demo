from dagster import asset, sensor, Definitions, RunRequest, RunConfig, Config, OpExecutionContext, define_asset_job, AssetSelection, DefaultSensorStatus

from kafkademo.resources import KafkaResource
from kafkademo.sensors import sensor_factory
from kafkademo.assets import loaded_from_kafka, downstream_of_kafka

SENSOR_REPLICAS=4

defs = Definitions(
    assets=[loaded_from_kafka],
    jobs=[downstream_of_kafka],
    sensors=[sensor_factory(i) for i in range(SENSOR_REPLICAS)],
    resources={
        'kafka': KafkaResource(bootstrap_servers=['localhost:9092'], topic_name='First_Topic')
    }
)