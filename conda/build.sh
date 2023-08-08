echo "Installing AusTrakka."
mkdir -p $PREFIX/bin
echo "$SRC_DIR"
echo "$PREFIX"
ls -la $SRC_DIR
unzip $SRC_DIR/test.zip -d $PREFIX/bin
