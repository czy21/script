## Cluster Install
```shell
# instann operator
kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/download/v2.11.0/cluster-operator.yml"

# get default username
kubectl -n db get secret rabbitmq-default-user -o jsonpath="{.data.username}" | base64 --decode
# get default password
kubectl -n db get secret rabbitmq-default-user -o jsonpath="{.data.password}" | base64 --decode

#
kubectl run perf-test --image=pivotalrabbitmq/perf-test -- --uri "amqp://${username}:${password}@${service}"

# delete instance
kubectl delete rabbitmqcluster rabbitmq
```