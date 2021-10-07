$OUTPUT_PATH="./tmp"
$EXIST=Test-Path $OUTPUT_PATH
$FILES=Get-ChildItem -Path "src/" -Filter *.py -r | % { $_.FullName }
echo $FILES
if ($EXIST -eq "True"){
  rm -r -Force ./tmp
}
mkdir tmp
cd tmp
pyinstaller -Fw $FILES  -n KnightReport
cd ..
