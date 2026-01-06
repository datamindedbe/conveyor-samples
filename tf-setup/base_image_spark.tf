resource "conveyor_ide_base_image" "my_image" {
  name         = "pyspark"
  description  = "My custom pyspark base image"
  config = {
    build_steps = [
      {
        name = "install openjdk"
        cmd  = <<EOF
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
sudo apt-get update && sudo apt-get install -y --no-install-recommends gcc g++ software-properties-common openjdk-11-jre unzip curl
JAVA_PATH=$(sudo update-alternatives --list java | sed -e "s/\/bin\/java//")
echo "export JAVA_HOME=$JAVA_PATH" >> ~/.bashrc
EOF
      },
      {
        name = "add spark libraries with conveyor specific patches and add them to the python environment"
        cmd = <<EOF
curl -X GET https://static.conveyordata.com/spark/spark-3.5.1-hadoop-3.3.6-v1.zip -o spark.zip \
  && sudo unzip ./spark.zip -d /opt \
  && rm ./spark.zip && sudo chmod -R 777 /opt/spark
echo 'source /opt/spark/sbin/spark-config.sh' >> ~/.bashrc
EOF
      },
      {
        name = "set default spark configuration for aws"
        cmd = <<EOF
mkdir -p /opt/spark/conf
cat <<-EOT > /opt/spark/conf/spark-defaults.conf
spark.hadoop.fs.s3.impl                             org.apache.hadoop.fs.s3a.S3AFileSystem
spark.hadoop.fs.s3a.aws.credentials.provider        com.amazonaws.auth.DefaultAWSCredentialsProviderChain
spark.kubernetes.pyspark.pythonVersion              3
spark.hadoop.hive.metastore.client.factory.class    com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory
spark.hadoop.hive.imetastoreclient.factory.class    com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory
spark.eventLog.enabled                              false
EOT
EOF
      }
    ]
  }
}
