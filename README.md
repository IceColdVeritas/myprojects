# **CSV Processing Application**
This repository contains two applications, the **Publisher** and the **Consumer**, that work together to process CSV files using RabbitMQ as the messaging broker. The Publisher application reads a CSV file and publishes each row as a message to the RabbitMQ server. The Consumer application consumes these messages, parses them, and generates an output CSV file with the processed data.
***
## **Publisher Application**
The Publisher application is responsible for reading a CSV file and publishing each row as a message to the RabbitMQ server. The application establishes a connection to the RabbitMQ server using the AMQP (Advanced Message Queuing Protocol) and publishes messages to the default exchange, using the **`csv_queue`** as the routing key. Each row in the CSV file is sent as a separate message to the RabbitMQ server.

### **Connection to RabbitMQ**
The Publisher application establishes a connection to the RabbitMQ server using the following parameters:

Host: **`rabbitmq`**<br>
Port: **`5672`**<br>
Username: **`guest`**<br>
Password: **`guest`**<br>


The Publisher application will read the CSV file, establish a connection to the RabbitMQ server, and publish each row as a separate message.
***
## **Consumer Application**
The Consumer application is responsible for consuming the messages from the RabbitMQ server, parsing the CSV data, and generating an output CSV file with the processed data. The application establishes a connection to the RabbitMQ server, creates a queue with the name **`csv_queue`**, and starts consuming messages from the queue. Each message is parsed into individual CSV fields, and the data is stored in memory.

### **Connection to RabbitMQ**
The Consumer application establishes a connection to the RabbitMQ server using the same parameters as the Publisher application:

Host: **`rabbitmq`**<br>
Port: **`5672`**<br>
Username: **`guest`**<br>
Password: **`guest`**<br>

The Consumer application will establish a connection to the RabbitMQ server, consume the messages from the **`csv_queue`**, parse the CSV data, and generate an output CSV file with the processed data.

## **Docker Compose**
The Docker Compose file (**`docker-compose.yml`**) defines the services and their configurations for running the Publisher and Consumer applications, as well as the RabbitMQ server.

The Docker Compose setup includes the following services:

- **publisher**: Runs the Publisher application, which reads the CSV file and publishes messages to the RabbitMQ server.
- **consumer**: Runs the Consumer application, which consumes messages from the RabbitMQ server, processes the data, and generates an output CSV file.
- **rabbitmq**: Runs the RabbitMQ server, which acts as the messaging broker for communication between the Publisher and Consumer applications.
<br>
<br>
### **Execution**
To run both the Publisher and Consumer applications using Docker Compose, follow these steps:

1. Ensure that Docker and Docker Compose are installed on your system.

2. Place the CSV file you want to process in the same directory as the docker-compose.yml file.

3. Open a terminal and navigate to the directory containing the docker-compose.yml file.

4. Set the environment variable CSV_FILE_PATH to the path of the CSV file you want to process. For example:

```bash
export CSV_FILE_PATH=/path/to/your/csv_file.csv
```
5. Run the following command to start the Publisher and Consumer applications along with the RabbitMQ server:

```bash
docker-compose up
```
The applications will start processing the CSV file and communicating with the RabbitMQ server.

6. To stop the execution and terminate the Docker containers, use **Ctrl+C** in the terminal.
<br>
<br>

### **Output File**
After running the Publisher and Consumer applications, an output CSV file will be generated in the same directory as the **`docker-compose.yml`** file. The output file will be named **`output.csv`** and will contain the processed data from the input CSV file.

Please note that this documentation assumes you have Docker and Docker Compose installed and configured on your system. It provides an overview of the setup, execution instructions, and details about the RabbitMQ connection and CSV processing.