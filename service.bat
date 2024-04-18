@echo off 
if "%1"=="h" goto begin 
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",1)(window.close)&&exit 
:begin 
::
start /b cmd /k "python.exe %~dp0/web.py"