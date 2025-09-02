#!/usr/bin/env python3
import itertools
import json
import subprocess
from itertools import chain
from typing import TypeVar, Generic, Callable, List, Optional
from urllib.parse import urlparse

import requests

T = TypeVar('T')


class PageIterator(Generic[T]):
    def __init__(self, page_index: int, page_size: int, load_func: Callable[[int, int], List[T]]):
        self.page_index = page_index
        self.page_size = page_size
        self.load_func = load_func

        self.current_index = 0
        self.has_more = True
        self.list: Optional[List[T]] = None

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if not self.has_next():
            raise StopIteration

        item = self.list[self.current_index]
        self.current_index += 1
        return item

    def has_next(self) -> bool:
        if self.list is not None and self.current_index < len(self.list):
            return True

        if not self.has_more:
            return False

        self.list = self.load_func(self.page_index, self.page_size)

        if self.list is None or len(self.list) == 0:
            self.has_more = False
            return False

        if len(self.list) < self.page_size:
            self.has_more = False

        self.current_index = 0
        self.page_index += 1
        return True


def flatmap(func, iterable):
    return chain.from_iterable(map(func, iterable))


def get_adoptium_jdks():
    filelist_cmd = 'rsync -r --list-only --include=*/ --include="OpenJDK*-jdk*" --exclude=* rsync://mirror.nju.edu.cn/adoptium/ | awk \'$NF ~ /OpenJDK/\' | awk \'{print $NF}\''
    result = subprocess.run(filelist_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    file_list = result.stdout.strip().splitlines()
    file_text = requests.get('https://archives.jenkins.io/updates/updates/io.jenkins.plugins.adoptopenjdk.AdoptOpenJDKInstaller.json')
    file_text = file_text.text.replace("downloadService.post('io.jenkins.plugins.adoptopenjdk.AdoptOpenJDKInstaller',", '').rstrip(')')
    openjdk_list = json.loads(file_text).get('data')
    for j in openjdk_list:
        for r in j['releases']:
            for b in r['binaries']:
                source_file = urlparse(b['binary_link']).path.split('/')[-1]
                target_file = next(filter(lambda f: f.split('/')[-1] == source_file, file_list), None)
                if target_file is not None:
                    b['binary_link'] = f'https://mirrors.nju.edu.cn/adoptium/{target_file}'
    return openjdk_list


def get_graalvm_jdks():
    def get_ext(asset, release):
        name_split = asset['name'].split('_')
        os_split = name_split[1].split('-')
        return {
            'tag_name': release['tag_name'],
            'major': release['tag_name'].replace('jdk-', '').split('.')[0],
            'os': os_split[0],
            'arch': os_split[1],
        }

    page_iterator = PageIterator(1, 100, lambda i, s: requests.get(f'https://api.github.com/repos/graalvm/graalvm-ce-builds/releases?page={i}&per_page={s}').json())
    releases = [t for t in page_iterator]
    releases = list(filter(lambda r: r['tag_name'].startswith('jdk-'), releases))
    releases = list(flatmap(lambda r: [
        {
            **a,
            **get_ext(a, r)
        }
        for a in filter(lambda r: 'sha256' not in r['name'], r['assets'])], releases))
    releases = [
        {
            'name': f'OpenJDK {k} - GraalVM',
            'releases': list(sorted([
                {
                    'release_name': rk,
                    'openjdk_impl': 'graalvm',
                    'binaries': [
                        {
                            'architecture': b['arch'],
                            'binary_link': b['browser_download_url'],
                            'openjdk_impl': 'graalvm',
                            'os': b['os'],
                        }
                        for b in rv
                    ]
                }
                for rk, rv in itertools.groupby(sorted(v, key=lambda a: a['tag_name']), key=lambda a: a['tag_name'])
            ], key=lambda r: r['release_name'], reverse=True)),
        }
        for k, v in itertools.groupby(sorted(releases, key=lambda r: r['major']), key=lambda r: r['major'])
    ]
    return releases


jdks = []
jdks.extend(get_adoptium_jdks())
jdks.extend(get_graalvm_jdks())

html_template = f'''<!DOCTYPE html><html><head><meta http-equiv='Content-Type' content='text/html;charset=UTF-8' /></head><body><script>window.onload = function () {{ window.parent.postMessage(JSON.stringify(
{json.dumps({'data': jdks}, indent=2)}
),'*'); }};</script></body></html>)'''
print(html_template)
