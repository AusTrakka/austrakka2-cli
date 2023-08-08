pipenv-setup sync
pyoxidizer build --verbose
cd build/$1/debug/install
zip austrakka-cli-$2-$3.zip austrakka -r austrakka-lib
mv austrakka-cli-$2-$3.zip ../../../../