import sys
import os
from selenium import webdriver
import stat
import shutil

def GetSupportedDriverNames():
    return ['chromedriver', 'geckodriver']

def GetLocalDriverDir():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) +
            '/../bin')

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
        options.accept_insecure_certs = False
        log_dir = os.path.abspath(os.path.dirname(__file__) + '/../log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_path = log_dir + '/geckodriver.log'
        driver = webdriver.Firefox(executable_path=path,
                log_path=log_path, options=options)
    else:
        raise RuntimeError(driver_name + " is not supported")

    return driver

def GetDriverLocal():
    driver_names = GetSupportedDriverNames()

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
    driver_names = GetSupportedDriverNames()

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

    raise RuntimeError("Could not find a supported webdriver. See https://github.com/jmckiern/vim-shoot for details.")
