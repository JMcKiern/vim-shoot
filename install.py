#!/usr/bin/env python3
import subprocess
import os
import sys
import io
import tarfile
import zipfile

def DownloadAndExtract(url: str):
    import requests
    print("Downloading from " + url)
    resp = requests.get(url, stream=True)

    if resp.status_code != requests.codes.ok:
        raise RuntimeError("Could not reach " + resp.url)

    if ".zip" in resp.url:
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        z.extractall(GetLocalDriverDir())
    elif ".tar.gz" in resp.url:
        t = tarfile.open(fileobj=io.BytesIO(resp.content), mode='r:gz')
        t.extractall(GetLocalDriverDir())
    else:
        raise ValueError("Unknown filetype: " + url.split('/')[-1])

def GetPlatform(driver_name: str):
    if driver_name == 'chromedriver':
        if sys.platform.startswith('linux'):
            return 'linux64'
        elif sys.platform.startswith('win32'):
            return 'win32'
        elif sys.platform.startswith('darwin'):
            return 'mac64'
    elif driver_name == 'geckodriver':
        if sys.platform.startswith('linux'):
            return 'linux64'
        elif sys.platform.startswith('win32'):
            return 'win32'
        elif sys.platform.startswith('darwin'):
            return 'macos'
    else:
        raise RuntimeError("Unknown driver: " + driver_name)
    raise RuntimeError("Unknown platform: " + sys.platform)

def GetSupportedDriverNames():
    return ['chromedriver', 'geckodriver']

def GetLocalDriverDir():
    return os.path.abspath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), './bin'))

def InstallGeckodriver():
    import requests
    latest_url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    resp = requests.get(latest_url)
    if resp.status_code != requests.codes.ok:
        raise RuntimeError("Could not reach " + resp.url)
    verNum = resp.json()['tag_name']

    assets_url = resp.json()['assets_url']
    resp = requests.get(assets_url)
    if resp.status_code != requests.codes.ok:
        raise RuntimeError("Could not reach " + resp.url)

    plt = GetPlatform('geckodriver')

    for asset in resp.json():
        if plt in asset['name']:
            dl_url = asset['browser_download_url']
            break

    DownloadAndExtract(dl_url)

def InstallChromedriver():
    import requests
    lr_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    resp = requests.get(lr_url)

    if resp.status_code != requests.codes.ok:
        raise RuntimeError("Could not reach " + resp.url)
    rel = resp.text


    plt = GetPlatform('chromedriver')

    dl_url = ('https://chromedriver.storage.googleapis.com/' + rel +
            '/chromedriver_' + plt + '.zip')

    DownloadAndExtract(dl_url)

def InstallDriver(driver_name: str):
    if driver_name not in GetSupportedDriverNames():
        raise ValueError("Preferred driver must be one of " + driver_names)

    print("Installing " + driver_name)
    if driver_name == "chromedriver":
        return InstallChromedriver()
    elif driver_name == "geckodriver":
        return InstallGeckodriver()
    else:
        raise RuntimeError("Cannot install " + preferred_driver)

def main():
    repolink_str = 'See https://github.com/JMcKiern/vim-shoot for details'
    if len(sys.argv) != 2:
        print('You must specify the WebDriver to use.\n' + repolink_str)
        return
    chosen_webdriver = sys.argv[1]

    supported_webdrivers = GetSupportedDriverNames()
    if chosen_webdriver not in supported_webdrivers:
        print('Only ' + str(supported_webdrivers) + ' are supported.\n' +
                repolink_str)

    dependencies = ['selenium', 'requests']
    install_dir = './3rdparty/'
    print('Installing dependencies (' + ', '.join(dependencies) + ') into ' +
            install_dir)
    subprocess.check_call([sys.executable, *(' '.join(['-m pip install',
        *dependencies, '--ignore-installed -t', install_dir]).split(' '))])

    sys.path.append(os.path.abspath('./3rdparty'))

    import requests
    InstallDriver(chosen_webdriver)

if __name__ == '__main__':
    main()
