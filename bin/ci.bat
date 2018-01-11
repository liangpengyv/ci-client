@echo off

if "%1"=="" goto no_parameter
if "%1"=="-y" goto yaml
if "%1"=="--yaml" goto yaml
if "%1"=="-h" goto help
if "%1"=="--help" goto help

goto error

:no_parameter
python %CI_HOME%\tools\client.py
goto end

:yaml
python %CI_HOME%\tools\client.py -y %CI_HOME%\conf\%2"
goto end

:help
python %CI_HOME%\tools\client.py -h
goto end

:error
python %CI_HOME%\tools\client.py %1

:end
