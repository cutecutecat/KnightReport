OUTPUT_PATH="tmp"
FILES=$(cd src && find ~+ -type f -name "*.py")
echo $FILES
[ -d $OUTPUT_PATH ] && rm -rf tmp
mkdir tmp
cd tmp
pyinstaller -Fw $FILES -c -n KnightReport-mac --upx-dir $1
mkdir -p KnightReport
cp KnightReport-mac ./KnightReport/KnightReport-mac
hdiutil create ./KnightReport-mac.dmg -srcfolder KnightReport -ov