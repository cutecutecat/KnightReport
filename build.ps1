rm -r -Force ./tmp
mkdir tmp
cd tmp
pyinstaller -Fw ../src/main.py ../src/ctrl.py ../src/constants.py ../src/utils.py -n KnightReport
cd ..