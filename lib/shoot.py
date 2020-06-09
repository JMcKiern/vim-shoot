import re
import tempfile
import datetime
import driver_mgr


def GenFilename():
    return ('shoot_' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') +
            '.png')

def HtmlFile2Png(filename: str):
    with open(filename, 'r') as f:
        htmlString = f.read()
    Html2Png(htmlString)

def Html2Png(htmlString: str):
    re.compile("pre {.*?}")

    # Fit content to image
    p = re.compile("pre {.*?}")
    m = p.search(htmlString)
    if m is None:
        raise ValueError("Could not find pre css selector")
    htmlString = (htmlString[:m.end()-1] + "display:inline-block; padding: 3px; " +
            htmlString[m.end()-1:])

    with tempfile.NamedTemporaryFile('w+', suffix='.html') as f:
        f.write(htmlString)
        f.seek(0)

        driver = driver_mgr.GetDriver()
        driver.get('file://' + f.name)
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)

        filename = GenFilename()
        driver.find_element_by_tag_name('pre').screenshot(filename)
        print('Saved screenshot as ' + filename)
        driver.quit()
