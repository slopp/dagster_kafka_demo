
from datetime import datetime
import time
from dagster import asset, sensor, Definitions, RunRequest, RunConfig, Config, OpExecutionContext, define_asset_job, AssetSelection, DefaultSensorStatus
from kafkademo.resources import KafkaResource
from kafkademo.assets import MyAssetConfig

MAX_BATCH_SIZE=50
MAX_SENSOR_TICK_RUNTIME=30
TIME_BETWEEN_SENSOR_TICKS=40

def sensor_factory(replica_id: int):

    @sensor(
        minimum_interval_seconds=TIME_BETWEEN_SENSOR_TICKS,
        job_name='downstream_of_kafka',
        default_status=DefaultSensorStatus.RUNNING,
        name=f"watch_kafka_{replica_id}"
    )
    def watch_kafka(kafka: KafkaResource):
        """ A sensor that consumes events from kafka and launches enqueues runs for them """
        
        # for each sensor loop, create a consumer and read up to MAX records
        consumer = kafka.get_consumer()
        tstart = datetime.now()
        

        while (datetime.now() - tstart).seconds < MAX_SENSOR_TICK_RUNTIME:

            msgs = consumer.poll(max_records=MAX_BATCH_SIZE,timeout_ms=2000)

            batch = []

            for tp, messages in msgs.items():
                for message in messages:
                    batch.append(message.value.decode('utf-8'))
                    
            if len(batch) > 0:
                yield RunRequest(
                    run_key=message.key,
                    run_config=RunConfig(ops={"loaded_from_kafka": MyAssetConfig(batch=batch)})
                )
                

            consumer.commit()
   
    return watch_kafka
        

