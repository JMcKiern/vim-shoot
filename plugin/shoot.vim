let s:save_cpo = &cpo
set cpo&vim

if exists('g:loaded_shoot')
    finish
endif
let g:loaded_shoot = 1

if !exists(":TOpng")
    command -range=% -bar TOpng :call shoot#Shoot(<line1>, <line2>)
endif

let &cpo = s:save_cpo
unlet s:save_cpo
