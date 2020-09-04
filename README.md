# Shoot

Shoot allows users to take screenshots of code in vim

**Example:**

![](demo.gif)

**Output:**

![](demo.png)

## How to Use

Use the command `:TOpng` to capture a screenshot of the selected lines (or the whole buffer if no lines are selected).

The image will be saved in vim's working directory.

### Options

- `g:shoot_zoom_factor` - Used to zoom image (default: 2)

## How to Install

### Requirements

- Vim compiled with python3 support (check this with `:echo has('python3')`)
- Python 3
- Chrome or Firefox (a browser based on either of these should work too)

### Plugin Install

#### Installation with vim-plug

Add one of the following to your vim-plug plugin list in your .vimrc.

##### For Chromium-based browsers:
```
Plug 'jmckiern/vim-shoot', { 'do': '\"./install.py\" chromedriver' }
```
##### For Firefox-based browsers:
```
Plug 'jmckiern/vim-shoot', { 'do': '\"./install.py\" geckodriver' }
```

Then run `:PlugInstall`

This will install the plugin and run the install.py script. This script does
two things. First, it installs the selenium and requests packages. Second, it
downloads the appropriate binary for the specified webdriver. These are all
isolated to the plugin's local directory.

#### Uninstall

Remove the `Plug 'jmckiern/vim-shoot'` line from your .vimrc and run `:PlugClean`

## How it Works

Vim already has a built in `:TOhtml` command which will generate a html file
that displays the selected lines. Using selenium and a WebDriver, a headless
browser is started to render the output of `:TOhtml`. This is then resized and
a screenshot is taken.
