/opt/spark/bin/spark-submit \
    --master k8s://https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT} \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=3 \
    --conf spark.kubernetes.container.image="datamechanics/spark:3.1-latest" \
    --conf spark.kubernetes.namespace=spark \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.jars.ivy=/tmp/.ivy \
    --conf spark.kubernetes.authenticate.caCertFile=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
    --conf spark.kubernetes.authenticate.oauthTokenFile=/var/run/secrets/kubernetes.io/serviceaccount/token \
    --conf spark.kubernetes.file.upload.path="s3a://sdg-tht-spark/executables" \
    local:///opt/spark/examples/src/main/python/pi.py
