@echo off
echo Setup
echo.
echo Adding virtualenv to python via pip
pip install virtualenv
echo.
echo Creating virtualenv named ENV for project
virtualenv ENV
echo.
echo Activating environment with activate script in Scripts
cd Env/Scripts
call activate
echo.
echo Installing beautifulsoup4
pip install beautifulsoup4
echo.
echo Installing requests
pip install requests
echo.
echo Installing lxml
pip install lxml
echo.
echo Deactivating ENV
call deactivate
echo.
echo Creating runfile.bat using python script
cd ..
cd ..
python Runfile_Writer.py
echo.
echo Setup complete
pause