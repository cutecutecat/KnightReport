OUTPUT_PATH="tmp"
FILES=$(cd src && find ~+ -type f -name "*.py")
echo $FILES
[ -d $OUTPUT_PATH ] && rm -rf tmp
mkdir tmp
cd tmp
# pyinstaller issue 4341-> can only use onedir mode
pyinstaller -Dw $FILES -c -n KnightReport --upx-dir $1
cd dist
hdiutil create ./KnightReport.dmg -srcfolder KnightReport -ov
cd ..
