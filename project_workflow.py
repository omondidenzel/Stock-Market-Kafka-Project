from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.aws.compute import EC2
from diagrams.aws.analytics import Athena
from diagrams.programming.language import Python
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Glue


with Diagram("Stock Market Data Engineering Workflow", show=False):
    with Cluster("Load Data"):
        load = Python("Python")
        load - Custom("CSV (API Sim)", "Files/csv-file.png")

    with Cluster("Kafka"):
        producer = Server("Producer")
        broker = Kafka("Broker")
        consumer = Server("Consumer")

        producer >> broker >> consumer

    ec2 = EC2("EC2")
    s3 = S3("S3 Bucket")
    athena = Athena("Athena")
    glue = Glue("Glue")

    load >> ec2 >> consumer 
    consumer >> s3 >> glue >> athena