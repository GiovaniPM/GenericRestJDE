zip -D files ..\api\*.*
docker build --tag=gapimg .
del files.zip