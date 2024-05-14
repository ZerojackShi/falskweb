@echo off 
if "%1"=="h" goto begin 
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",1)(window.close)&&exit 
:begin 
::
rem 获取当前文件夹路径
set "current_dir=%~dp0"
rem 执行 Python 脚本
start /b cmd /k "python.exe %current_dir%web.py"