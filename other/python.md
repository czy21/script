# windows python c++ build tool install
## install vs2022
## selected windows sdk and 

# ubuntu 20.0.4 install python
```shell
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 python3.10-dev python3.10-distutils -y
ls -l /usr/bin/python*
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2
sudo update-alternatives --config python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.10 get-pip.py

sudo apt remove python3-apt
sudo apt autoremove
sudo apt autoclean
sudo apt install python3-apt
```