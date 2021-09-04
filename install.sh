#! /bin/bash

# create a namespace
kubectl create ns sample

# create a config map
kubectl apply -f cm.yaml

# create a deployment
kubectl apply -f dc.yaml

# create a service
kubectl apply -f svc.yaml