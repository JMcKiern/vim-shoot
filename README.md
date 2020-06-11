# Shoot

Shoot allows users to take screenshots of code in vim

## How to Install

### Requirements

- Vim compiled with python3 support (check this with `:echo has('python3')`
- Chrome or Firefox installed

### Plugin Install

If using vim-plug, add this line to your .vimrc

```
Plug 'jmckiern/vim-shoot'
```

Additionally, you **must** install a WebDriver for Shoot to work.

### WebDriver

Shoot relies on a Selenium WebDriver to render the html. Specifically, either
`chromedriver` or `geckodriver` is needed.

Shoot is capable of installing the appropriate binary into the plugin directory.

This can be done by specifying the following in your .vimrc:

```
g:shoot_preferred_driver = 'chromedriver'
g:shoot_install_driver = v:true
```

#### Which WebDriver to use

Use `'geckodriver'` if you use Firefox  
Use `'chromedriver'` if you Chrome/Chromium

## How to Use

Use the command `:TOpng` to capture a screenshot of the whole buffer

You can also call it with a range on lines to specify which lines to include

The image will be saved in vim's current working directory.

## Options

- `g:shoot_preferred_driver` can be set to either `'geckodriver'` or `'chromedriver'`.
- `g:shoot_force_preferred_driver` only use the driver specified in `g:shoot_preferred_driver`
- `g:shoot_install_driver`, if set to `v:true`, Shoot will install the selected driver if none is found

## How Shoot Finds a WebDriver

1. Check the plugin directory for a driver
2. If no driver found, check for a driver in $PATH
3. If no driver found and `g:shoot_install_driver` is set, download the driver specified by `g:shoot_preferred_driver`
