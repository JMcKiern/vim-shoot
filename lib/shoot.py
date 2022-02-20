import re
import os
import os.path
import tempfile
import datetime
import driver_mgr

def GenFilename():
    if os.name == 'nt':
        datetime_format = '%Y-%m-%d_%H%M%S'
    else:
        datetime_format = '%Y-%m-%d_%H:%M:%S'
    return ('shoot_' + datetime.datetime.now().strftime(datetime_format) +
            '.png')

def AddToCss(htmlString, pattern, toAdd):
    p = re.compile(pattern)
    m = p.search(htmlString)
    if m is None:
        raise ValueError("Could not find css with " + pattern)
    return htmlString[:m.end()-1] + toAdd + htmlString[m.end()-1:]

def Html2Png(htmlString: str, zoomFactor, save_path: str, browser_binary: str):
    htmlString = AddToCss(htmlString, "pre {.*?}", "margin: 0; ")
    bodyCss = "margin: 0; padding: 3px; transform: scale(" + str(zoomFactor) + "); transform-origin: top left; display: inline-block; "
    htmlString = AddToCss(htmlString, "body {.*?}", bodyCss)

    f = tempfile.NamedTemporaryFile('w+', suffix='.html', delete=False)
    try:
        f.write(htmlString)
        f.seek(0)
        f.close()

        driver = driver_mgr.GetDriver(browser_binary)
        driver.get('file://' + f.name)
        requiredWidth = driver.execute_script('return document.body.scrollWidth')
        requiredHeight = driver.execute_script('return document.body.scrollHeight')

        paddingWidth = driver.execute_script('return (window.outerWidth - window.innerWidth)')
        paddingHeight = driver.execute_script('return (window.outerHeight - window.innerHeight)')

        driver.set_window_size(requiredWidth * zoomFactor + paddingWidth + 1,
                               requiredHeight * zoomFactor + paddingHeight + 1)

        filename = GenFilename()
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        path = os.path.join(save_path, filename)
        driver.save_screenshot(path)
        print('Saved screenshot at ' + path)
        driver.quit()
    finally:
        os.remove(f.name)
