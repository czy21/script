```shell
mkdir -p $HOME/.kube && sudo cp --force /etc/rancher/k3s/k3s.yaml $HOME/.kube/config && sudo chown $USER:$USER $HOME/.kube/config
sudo curl -SL "https://dl.k8s.io/release/v1.28.3/bin/linux/amd64/kubectl" -o /usr/local/bin/kubectl
sudo chmod +x /usr/local/bin/kubectl 
# sudo ln -sf /usr/local/bin/kubectl /usr/bin/kubectl
kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
helm completion bash | sudo tee /etc/bash_completion.d/helm > /dev/null
```