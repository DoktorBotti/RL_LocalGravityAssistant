@echo off


:start


If not "%1" == "activated" Goto notActivated 

pip install cycler
pip install kiwisolver
pip install matplotlib
pip install numpy
pip install Pillow
pip install pynput
pip install pyparsing
pip install pyperclip
pip install PyRect
pip install PyScreeze
pip install pytesseract
pip install python-dateutil
pip install PyTweening
pip install scipy
pip install six
Goto end


:notActivated
python -m venv ./venv
cmd /k ".\venv\Scripts\activate & .\InstallDepencencies.bat activated"

:end


exit