import requests
import sys
import io
import os
from selenium import webdriver
import stat
import vim
import shutil
import tarfile
import zipfile

def DownloadAndExtract(url: str):
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


def GetSupportedDriverNamesOrdered():
    driver_names = ['chromedriver', 'geckodriver']

    if bool(int(vim.eval('exists("g:shoot_preferred_driver")'))):
        preferred_driver = vim.eval('g:shoot_preferred_driver')
        if preferred_driver not in driver_names:
            raise ValueError("Preferred driver must be one of " + driver_names)
        if (bool(int(vim.eval('exists("g:shoot_force_preferred_driver")'))) and
                bool(int(vim.eval('g:shoot_force_preferred_driver')))):
            driver_names = [preferred_driver]
        else:
            # Move to front
            driver_names.insert(0,
                driver_names.pop(driver_names.index(preferred_driver)))

    return driver_names

def GetLocalDriverDir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) +
            '/../bin')

def InstallGeckodriver():
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

    return GetDriverLocal()

def InstallChromedriver():
    lr_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    resp = requests.get(lr_url)

    if resp.status_code != requests.codes.ok:
        raise RuntimeError("Could not reach " + resp.url)
    rel = resp.text


    plt = GetPlatform('chromedriver')

    dl_url = ('https://chromedriver.storage.googleapis.com/' + rel +
            '/chromedriver_' + plt + '.zip')

    DownloadAndExtract(dl_url)

    return GetDriverLocal()

def InstallDriver():
    if not bool(int(vim.eval('exists("g:shoot_preferred_driver")'))):
        raise ValueError("g:shoot_preferred_driver must be defined to install a driver")

    driver_name = vim.eval('g:shoot_preferred_driver')
    if driver_name not in GetSupportedDriverNamesOrdered():
        raise ValueError("Preferred driver must be one of " + driver_names)

    print("Installing " + driver_name)
    if driver_name == "chromedriver":
        return InstallChromedriver()
    elif driver_name == "geckodriver":
        return InstallGeckodriver()
    else:
        raise RuntimeError("Cannot install " + preferred_driver)

def CreateDriver(path: str):
    if not os.path.exists(path):
        return None

    driver_name = os.path.basename(path)
    if driver_name.endswith('.exe'):
        driver_name = '.'.join(driver_name.split('.')[:-1])

    if driver_name == "chromedriver":
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(executable_path=path, options=options)
    elif driver_name == "geckodriver":
        options = webdriver.FirefoxOptions()
        options.headless = True
        log_dir = os.path.abspath(os.path.dirname(path) + '/../log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_path = log_dir + '/geckodriver.log'
        driver = webdriver.Firefox(executable_path=path,
                log_path=log_path, options=options)
    else:
        raise RuntimeError(driver_name + " is not supported")

    return driver

def GetDriverLocal():
    driver_names = GetSupportedDriverNamesOrdered()

    for driver_name in driver_names:
        path = GetLocalDriverDir() + '/' + driver_name
        if sys.platform == 'win32':
            path += '.exe'
        if os.path.exists(path):
            break
    else:
        return None
    os.chmod(path, stat.S_IXUSR)

    return CreateDriver(path)

def GetDriverOnPath():
    driver_names = GetSupportedDriverNamesOrdered()

    for driver_name in driver_names:
        path = shutil.which(driver_name)
        if path is not None:
            break
    else:
        return None

    return CreateDriver(path)

def GetDriver():

    driver = GetDriverLocal()
    if driver is not None:
        return driver

    driver = GetDriverOnPath()
    if driver is not None:
        return driver

    if vim.eval("g:shoot_install_driver"):
        driver = InstallDriver()
        if driver is not None:
            return driver

    raise RuntimeError("Could not find a supported webdriver. See https://github.com/jmckiern/vim-shoot for details.")
