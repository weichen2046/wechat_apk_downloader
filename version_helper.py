import bisect
from distutils.version import StrictVersion
import re

from bs4 import BeautifulSoup
import demjson
import requests


class VersionHelper(object):

    version_list_url = 'https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_faq_list'

    def __init__(self, platform='Android'):
        self.db_dict = {}
        self.db_list = []
        self.db_loaded = False
        self.all_versions = []
        self.all_versions_loaded = False
        self.platform = platform

    def get_newest_version(self):
        resp = requests.get(self.version_list_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        def is_android_version(tag):
            return True if re.match(r'.* ((\d+\.)+\d+) for Android', str(tag.string)) is not None else False

        tag_a = soup.find(is_android_version)
        return re.match(r'.* ((\d+\.)+\d+)', str(tag_a)).groups()[0]

    def get_all_versions(self):
        if self.all_versions_loaded:
            return self.all_versions

        resp = requests.get(self.version_list_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        def is_android_version(tag):
            return True if re.match(r'.* ((\d+\.)+\d+) for Android', str(tag.string)) is not None else False

        tags_a = soup.find_all(is_android_version)
        tags_a.reverse()
        self.all_versions = [re.match(r'.* ((\d+\.)+\d+)', str(tag_a)
                                      ).groups()[0] for tag_a in tags_a]
        self.all_versions_loaded = True
        return self.all_versions

    def get_url_for_version(self, version):
        '''
        E.g. http://dldir1.qq.com/weixin/android/weixin666android1300.apk

        Side effect: will change local database.
        '''

        if not self.all_versions_loaded:
            self.get_all_versions()

        if version not in self.all_versions:
            return None

        target_url_fmt = 'http://dldir1.qq.com/weixin/android/weixin{}android{}.apk'

        if not self.db_loaded:
            self.load_db('./database.json')

        if version in self.db_dict:
            return target_url_fmt.format(version.replace('.', ''), self.db_dict[version])

        index = bisect.bisect_right(self.db_list, StrictVersion(version))

        if index < len(self.db_list):
            up_ver = str(self.db_list[index])
            up_code = self.db_dict[up_ver]

            up_code -= 20
            while up_code > 0:
                target_url = target_url_fmt.format(
                    version.replace('.', ''), up_code)
                resp = requests.head(target_url)
                if resp.status_code == requests.codes.not_found:
                    up_code -= 20
                    continue
                self.__update_local_db(version, up_code)
                return target_url
        else:
            server_newest_ver = StrictVersion(self.all_versions[-1])
            if StrictVersion(version) > server_newest_ver:
                return None

            local_largest_ver = str(self.db_list[-1])
            local_largest_ver_index = self.all_versions.index(
                local_largest_ver)
            target_ver_index = self.all_versions.index(version)
            target_ver_code = (
                target_ver_index - local_largest_ver_index) * 20 + self.db_dict[local_largest_ver]
            target_url = target_url_fmt.format(
                version.replace('.', ''), target_ver_code)

            resp = requests.head(target_url)
            if resp.status_code == requests.codes.ok:
                self.__update_local_db(version, target_ver_code)
                return target_url
            return None

    def is_version_exist(self, version):
        if not self.all_versions_loaded:
            self.get_all_versions()
        return version in self.all_versions

    def load_db(self, db_file):
        db = demjson.decode_file(db_file)
        for ver_code in db:
            self.db_list.append(StrictVersion(ver_code['version']))
            self.db_dict[ver_code['version']] = ver_code['code']

        self.db_list.sort()
        self.db_loaded = True

    def __update_local_db(self, version, code):
        self.db_dict[version] = code
        ver_array = []
        for k, v in self.db_dict.items():
            ver_array.append({
                'version': k,
                'code': v,
            })
        demjson.encode_to_file('database.json', ver_array, overwrite=True)
