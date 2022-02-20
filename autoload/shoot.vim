let s:save_cpo = &cpo
set cpo&vim

let s:plugin_path = expand('<sfile>:p:h')

if !exists('g:shoot_install_driver')
	let g:shoot_install_driver = v:false
endif
if !exists('g:shoot_zoom_factor')
	" zoom factor of 1 is generally too low
	let g:shoot_zoom_factor = 2
endif
if !exists('g:shoot_save_path')
	" save path
	let g:shoot_save_path = getcwd()
endif

function! shoot#Shoot(line1, line2)
    silent call tohtml#Convert2HTML(a:line1, a:line2)
    let l:bufnr = bufnr()
    let s:bufAsStr = join(getbufline(l:bufnr, 1, '$'), "\n")
    execute l:bufnr.'bd!'
python3 << ENDPYTHON

import os
import sys
import vim

plugin_path = vim.eval("s:plugin_path")
sys.path.append(os.path.abspath(plugin_path + '/../lib'))
sys.path.append(os.path.abspath(plugin_path + '/../3rdparty'))

import shoot
htmlString = vim.eval("s:bufAsStr")
zoomFactor = int(vim.eval("g:shoot_zoom_factor"))
save_path = vim.eval("g:shoot_save_path")
browser_binary = vim.eval('g:shoot_browser_binary') if bool(int(vim.eval('exists("g:shoot_browser_binary")'))) else None
shoot.Html2Png(htmlString, zoomFactor, save_path, browser_binary)

ENDPYTHON
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
