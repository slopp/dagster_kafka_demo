# Dagster Stream to Micro-Batch

[Demo video](https://www.loom.com/share/2ede5d6feaf2442cafb83d919ca8b583?sid=7dfc7763-8b78-443a-8bc5-8f0c507f2e2e)

This example project shows how you might use Dagster for a micro-batch streaming use case.

In this example:

- A Kafka producer publishes messages to a topic. See `kafka_producer.py`. You can specify a desired publish rate, `DESIRED_THROUGHPUT_PER_SECOND`.  

- A Dagster sensor is responsible for consuming these messages. On each evaluation tick of the sensor, a consumer is created, adn then the consumer (a) pulls up to `MAX_BATCH_SIZE` messages, and (b) enqueues a run. The sensor passes the batch of messages to the run via `RunConfig`. The (a) pull and (b) submit pattern is repeated up to a fixed amount of time, at which point the sensor tick is marked complete. Dagster then waits a set interval of time before starting a new sensor tick.

- Once the runs are in the run queue, Dagster launches and tracks the micro-batch runs. The number of concurrent runs can be managed by the Dagster queue, see `dagster.yaml`.  

- For each run, the batch of messages is passed to the Dagster asset through configuration and then processed. In this example, the `MyAssetConfig.kafka_msg_batch` accepts a list of decoded `message.values`. You could do any number of interesting things in this processing step, such as bulk uploading to a warehouse or using Dagster's dynamic orchestration to parallel process inputs. 

- The Kafka connection details are stored in a Dagster class, `KafkaResource`.



## Getting started

Install Kafka following [these instructions](https://kafka.apache.org/quickstart); install into this directory. Tested with Kafka 2.13-3.4.0. Update the version info and paths in the Makefile if a different version or install directory is used.

Install the Dagster project and dependencies into a virtual environment of your choice:

```bash
pip install -e ".[dev]"
```

Start Dagster:

```
make dagster_dev
```

Click the link (default: localhost:3000) to open Dagster. 

In a new terminal, start Kafka:

```
make start_kafka
```

In a new terminal, start the Kafka producer:

```bash
make start_producer
```

At this point, you should see the sensor enqueueing runs and asset runs for the various batches. See this [demo video](https://www.loom.com/share/2ede5d6feaf2442cafb83d919ca8b583?sid=7dfc7763-8b78-443a-8bc5-8f0c507f2e2e) for details.

To check the lag (messages that have been published but not consumed by Dagster) run: 

```bash
make check_lag
```

The throughput of the system can be tuned by setting a few options:

Option | Description | Location 
--- | --- | --- 
`DESIRED_THROUGHPUT_PER_SECOND` | Number of messages to publish per second | `kafka_producer.py` 
`MAX_BATCH_SIZE` | Number of messages to batch together into a Dagster run | `kafkademo/sensors.py` 
`MAX_SENSOR_TICK_RUNTIME` | Max time for a sensor tick to run. Longer means fewer consumers but less Dagster visibility. Recommended: 10 seconds. | `kafkademo/sensors.py`
`TIME_BETWEEN_SENSOR_TICKS` | Time between sensor ticks. Longer means increased delay in handling events, but less pressure on Kafka. Recommended: 10 seconds. | `kafkademo/sensors.py`
Max concurrent runs | Dagster will queue runs to prevent overwhelming your run system. Default for local computer: 5 | `dagster.yaml`


## Next steps

This project is straightforward and only contains a single asset. You could create downstream assets, model data partitions, and use declarative scheduling with freshness policies to create downstream data transformations using the latest data that has been loaded.
