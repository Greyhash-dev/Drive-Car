VER=""

if [ -n '$(pip3 --version | grep -Fw "python 3")' ]
then
echo "python3"
elif [ '$(pip --version | grep -Fw "python 2")' ]
then
echo "python2"
fi