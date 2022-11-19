Steps to setup dependencies: 
1. Start Zookeeper: bin/zookeeper-server-start.sh config/zookeeper.properties
2. Start Kafka: bin/kafka-server-start.sh config/server.properties
3. Create Topics: bin/kafka-topics.sh --create --topic tweet_sentiments --bootstrap-server localhost:9092 and bin/kafka-topics.sh --create --topic tweet_sentiments_result --bootstrap-server localhost:9092
4. Start Elasticsearch: ./bin/elasticsearch
5. Start Kibana: ./bin/kibana
6. Start Logstash: ./bin/logstash 

Steps to run code:
1. Run the producer to get tweets and analyze: python producer.py
2. run spark: .spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 kafkaStreaming.py localhost:9092 subscribe tweet_sentiments 