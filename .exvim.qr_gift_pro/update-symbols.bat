@echo off
set DEST=.\.exvim.qr_gift_pro
set TOOLS=C:\exVim\vimfiles\tools\
set TMP=%DEST%\_symbols
set TARGET=%DEST%\symbols
call %TOOLS%\shell\batch\update-symbols.bat
