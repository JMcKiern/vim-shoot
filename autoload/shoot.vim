let s:save_cpo = &cpo
set cpo&vim

let s:plugin_path = expand('<sfile>:p:h')

if !exists('g:shoot_install_driver')
	let g:shoot_install_driver = v:false
endif

function! shoot#Shoot(line1, line2)
    silent call tohtml#Convert2HTML(a:line1, a:line2)
    let l:bufnr = bufnr()
    let s:bufAsStr = join(getbufline(l:bufnr, 1, '$'), "\n")
    execute l:bufnr.'bd!'
python3 << endpython

import os
import sys
import vim

plugin_path = vim.eval("s:plugin_path")
python_module_path = os.path.abspath(plugin_path + '/../lib')
sys.path.append(python_module_path)

import shoot
htmlString = vim.eval("s:bufAsStr")
shoot.Html2Png(htmlString)

endpython
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
