
clean: 
	rm -rf ~/.dagster_home; mkdir ~/.dagster_home; cp dagster.yaml ~/.dagster_home/dagster.yaml

dagster_dev: clean
	export DAGSTER_HOME="~/.dagster_home"; dagster dev -m kafkademo

check_lag: 
	kafka_2.13-3.4.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group group1              

start_kafka: start_zookeeper
	kafka_2.13-3.4.0/bin/kafka-server-start.sh kafka_2.13-3.4.0/config/server.properties & 

start_zookeeper:
	kafka_2.13-3.4.0/bin/zookeeper-server-start.sh kafka_2.13-3.4.0/config/zookeeper.properties &

start_producer:
	python ./kafka_producer.py