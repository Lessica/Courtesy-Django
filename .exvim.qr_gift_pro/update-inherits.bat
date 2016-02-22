@echo off
set DEST=.\.exvim.qr_gift_pro
set TOOLS=C:\exVim\vimfiles\tools\
set TMP=%DEST%\_inherits
set TARGET=%DEST%\inherits
call %TOOLS%\shell\batch\update-inherits.bat
