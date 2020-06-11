import re
import tempfile
import datetime
import driver_mgr


def GenFilename():
    return ('shoot_' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') +
            '.png')

def AddToCss(htmlString, pattern, toAdd):
    p = re.compile(pattern)
    m = p.search(htmlString)
    if m is None:
        raise ValueError("Could not find css with " + pattern)
    return htmlString[:m.end()-1] + toAdd + htmlString[m.end()-1:]

def Html2Png(htmlString: str, zoomFactor):
    htmlString = AddToCss(htmlString, "pre {.*?}", "margin: 0; ")
    bodyCss = "margin: 0; padding: 3px; transform: scale(" + str(zoomFactor) + "); transform-origin: top left; display: inline-block; "
    htmlString = AddToCss(htmlString, "body {.*?}", bodyCss)

    with tempfile.NamedTemporaryFile('w+', suffix='.html') as f:
        f.write(htmlString)
        f.seek(0)

        driver = driver_mgr.GetDriver()
        driver.get('file://' + f.name)
        requiredWidth = driver.execute_script('return document.body.scrollWidth')
        requiredHeight = driver.execute_script('return document.body.scrollHeight')

        paddingWidth = driver.execute_script('return (window.outerWidth - window.innerWidth)')
        paddingHeight = driver.execute_script('return (window.outerHeight - window.innerHeight)')

        driver.set_window_size(requiredWidth * zoomFactor + paddingWidth + 1,
                               requiredHeight * zoomFactor + paddingHeight + 1)

        filename = GenFilename()
        driver.save_screenshot(filename)
        print('Saved screenshot as ' + filename)
        driver.quit()
