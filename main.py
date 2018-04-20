import requests
import sys

from version_helper import VersionHelper


def download_apk(url, output_file=None):
    output = output_file

    if not output:
        output = url[(url.rindex('/') + 1):]

    resp = requests.get(url, stream=True)
    with open(output, 'wb') as apk:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                apk.write(chunk)


def list_available_versions():
    helper = VersionHelper()
    versions = helper.get_all_versions()
    versions.reverse()
    for v in versions:
        print(v)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='WeChat APK Downloader.')
    parser.add_argument('--target-version', type=str,
                        help="Target WeChat version, e.g. '6.6.6'.")
    parser.add_argument('--output', type=str, help="Specify output APK file.")
    parser.add_argument('--list', action='store_true',
                        help="List all available versions.")
    parser.add_argument('--verbose', action='store_true',
                        help="Verbose output.")
    args = parser.parse_args()

    if args.list:
        list_available_versions()
        sys.exit(0)

    helper = VersionHelper()

    target_version = args.target_version
    if not args.target_version:
        target_version = helper.get_newest_version()

    target_url = helper.get_url_for_version(target_version)

    if not target_url:
        print('No download url for version:', target_version)
        sys.exit(1)

    if args.verbose:
        print('Try download target file:', target_url)

    download_apk(target_url, output_file=args.output)
