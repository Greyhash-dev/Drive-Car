VER=""

if [ -n '$(pip3 --version | grep -Fw "python 3")' ]
then
VER="python3"
else
if [ -n '$(pip --version | grep -Fw "python 2")' ]
then
VER="python2"
fi
fi
echo $VER