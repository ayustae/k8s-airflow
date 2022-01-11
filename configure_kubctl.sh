#!/bin/bash

aws eks update-kubeconfig --region us-east-1 --name spark_k8s_cluster --kubeconfig kubeconfig
