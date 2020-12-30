VER=""

function checkPIPinstall() {
    PCKG=$1
    if [ -n "$($VER list --disable-pip-version-check | grep -Fw $PCKG)" ]
    then
    echo "$PCKG is installed!"
    else
    echo "Package -$PCKG- is not installed. Do you want to install it? (y/n)"
    read -p "Are you sure? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
    sudo $VER install $PCKG
    else
    echo "This package is required for this to function!"
    exit
    fi
    fi
}

function checkAPTinstall() {
    APTPCKG=$1
    if [ -n "$(apt list --installed | grep -Fw $APTPCKG)" ]
    then
    echo "$APTPCKG is installed!"
    else
    echo "Package -$APTPCKG- is not installed. Do you want to install it? (y/n)"
    read -p "Are you sure? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
    sudo apt-get install $APTPCKG -y
    else
    echo "This package is required for this to function!"
    exit
    fi
    fi
}

if [ -n '$(pip3 --version | grep -Fw "python 3")' ]
then
VER="pip3"
else
if [ -n '$(pip --version | grep -Fw "python 2")' ]
then
VER="pip"
fi
fi
#python is not installed
if [ -z $VER ]
then

echo 'python not found. Do you want to install apt-package "python3" (y/n)'
read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
sudo apt-get install python3
else
exit
fi
fi
checkPIPinstall "pygame"
checkPIPinstall "neat-python"
checkPIPinstall "graphviz"
checkPIPinstall "matplotlib"
checkPIPinstall "numpy"
checkAPTinstall "graphviz"
echo "Drive-Car was successfully installed!"