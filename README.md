# Shoot

Shoot allows users to take screenshots of code in vim

## How to Install

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

TODO: Explain how to install

## How to Use

Use the command `:TOpng` to capture a screenshot of the whole buffer

You can also call it with a range on lines to specify which lines to include

The image will be saved in vim's current working directory.

## Options

`g:shoot_preferred_driver` can be set to either `geckodriver` or `chromedriver`.
`g:shoot_install_driver`, if set to `v:true`, Shoot will install the selected driver if none is found

## How Shoot Finds a WebDriver

1. Check the plugin directory for a driver
2. Check for a driver in $PATH
3. If `g:shoot_install_driver` is set, download the driver specified by `g:shoot_preferred_driver`
