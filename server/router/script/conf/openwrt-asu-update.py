from requests import Session

session = Session()

asu_url = "http://openwrt-asu.czy21.com"

def reload_all():
    versions_json = session.get("http://openwrt-download.czy21.com/.versions.json").json()
    versions = []
    upcoming_version = versions_json["upcoming_version"]
    if upcoming_version:
        versions.append(upcoming_version)
    versions.extend(versions_json["versions_list"])
    for version in versions:
        print(f"Reloading {version}")
        targets = session.get(
            f"http://openwrt-download.czy21.com/releases/{version}/.targets.json"
        )
        if targets.status_code == 404:
            print(f"Targets not found for {version}")
            continue
        targets = targets.json()
        for target in targets:
            print(f"Reloading {version}/{target}")
            session.get(
                f"{asu_url}/api/v1/update/{version}/{target}",
                headers={"X-Update-Token": "{{ param_asu_update_token }}"},
            )

    targets = session.get(
        "http://openwrt-download.czy21.com/snapshots/.targets.json"
    ).json()
    for target in targets:
        print(f"Reloading SNAPSHOT/{target}")
        session.get(
            f"{asu_url}/api/v1/update/SNAPSHOT/{target}",
            headers={"X-Update-Token": "{{ param_asu_update_token }}"},
        )

reload_all()