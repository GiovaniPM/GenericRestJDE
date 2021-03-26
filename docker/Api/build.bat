7z a files.zip ../../api/*.*
docker build --tag=gapimg .
del files.zip