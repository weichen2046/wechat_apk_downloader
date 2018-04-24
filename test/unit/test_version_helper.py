import os
import unittest

from distutils.version import StrictVersion

from version_helper import VersionHelper

TEST_BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class VersionHelperTestCase(unittest.TestCase):

    def test_load_db(self):
        db_file = os.path.join(TEST_BASE_DIR, 'database.json')
        helper = VersionHelper()
        helper.load_db(db_file)

        self.assertEqual(3, len(helper.db_list))
        self.assertEqual(3, len(helper.db_dict))

        expected_list = [
            StrictVersion('6.6.2'),
            StrictVersion('6.6.3'),
            StrictVersion('6.6.5'),
        ]
        self.assertListEqual(helper.db_list, expected_list)

        expected_dict = {
            '6.6.5': 1280,
            '6.6.3': 1260,
            '6.6.2': 1240,
        }
        self.assertDictEqual(helper.db_dict, expected_dict)

    def test_is_version_exist(self):
        helper = VersionHelper()
        version = '6.6.6'
        actual = helper.is_version_exist(version)
        self.assertEqual(
            True, actual, 'Version {} should be exist'.format(version))

        version = '6.6.4'
        actual = helper.is_version_exist(version)
        self.assertEqual(
            False, actual, 'Version {} should not be exist'.format(version))

    def test_get_newest_version(self):
        helper = VersionHelper()
        import os
        actual = helper.get_newest_version()
        self.assertEqual(os.environ.get('WECHAT_NEWEST_VER'), actual)

    def test_get_all_versions(self):
        helper = VersionHelper()
        versions = helper.get_all_versions()
        self.assertGreater(len(versions), 0)

        self.assertIn(StrictVersion('1.0.0'), versions)
        self.assertIn(StrictVersion('1.1.0'), versions)

    def test_get_url_for_version(self):
        helper = VersionHelper()

        # Test don't exist version.
        url = helper.get_url_for_version('6.6.4')
        self.assertEqual(url, None)

        # Test version in local database file.
        url = helper.get_url_for_version('6.6.5')
        self.assertEqual(
            url, 'http://dldir1.qq.com/weixin/android/weixin665android1280.apk')

        # Test future version.
        url = helper.get_url_for_version(os.environ.get('WECHAT_FUTURE_VER'))
        self.assertEqual(url, None)

        # Test version beyond largest version in local database.
        url = helper.get_url_for_version('6.6.6')
        self.assertEqual(
            url, 'http://dldir1.qq.com/weixin/android/weixin666android1300.apk')

        # Test version below least version in local database.
        url = helper.get_url_for_version('6.6.1')
        self.assertEqual(
            url, 'http://dldir1.qq.com/weixin/android/weixin661android1220.apk')
