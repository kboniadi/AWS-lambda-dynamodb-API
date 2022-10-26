FROM amazon/dynamodb-local
WORKDIR /home/dynamodblocal
RUN mkdir ./data && chown -R 1000 ./data
CMD ["-jar", "DynamoDBLocal.jar", "-dbPath", "./data", "-sharedDb"]
VOLUME ["./data"]