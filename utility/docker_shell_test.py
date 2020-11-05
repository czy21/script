import json
import subprocess


def inspect_network(inspect_command):
    proc = subprocess.Popen(inspect_command, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    connected_containers = json.loads("".join([x.strip() for x in proc.stdout.readlines() if x.strip()]))
    print([v["Name"] for v in connected_containers[0]["Containers"].values()])
    proc.stdout.close()
    proc.wait()
    return connected_containers, proc


if __name__ == '__main__':
    inspect_network('sudo docker network inspect erp_play_default')
