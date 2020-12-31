VER=""

function checkPIPinstall() {
    PCKG=$1
    if [ -n "$($VER list --disable-pip-version-check | grep -Fw $PCKG)" ]
    then
    echo "$PCKG is installed!"
    else
    read -p "Package -$PCKG- is not installed. Do you want to install it? (y/n)" -n 1 -r
    # read -p "Are you sure? " -n 1 -r
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
    if [ $(dpkg-query -W -f='${Status}' $APTPCKG 2>/dev/null | grep -c "ok installed") -eq 1 ];
    then
    echo "$APTPCKG is installed!"
    else
    read -p "Package -$APTPCKG- is not installed. Do you want to install it? (y/n)" -n 1 -r
    # read -p "Are you sure? " -n 1 -r
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

if [ $(dpkg-query -W -f='${Status}' python3 2>/dev/null | grep -c "ok installed") -eq 1 ] || [ $(dpkg-query -W -f='${Status}' python-is-python3 2>/dev/null | grep -c "ok installed") -eq 1 ];
then
if [ $(dpkg-query -W -f='${Status}' python3-pip 2>/dev/null | grep -c "ok installed") -eq 1 ];
then
if [ -n '$(pip3 --version | grep -Fw "python 3")' ]
then
VER="pip3"
else
if [ $(dpkg-query -W -f='${Status}' python-pip 2>/dev/null | grep -c "ok installed") -eq 1 ];
then
if [ -n '$(pip --version | grep -Fw "python 3")' ]
then
VER="pip"
fi
fi
fi
fi
fi
#python is not installed
if [ -z $VER ]
then

read -p 'python not found. Do you want to install apt-package "python3" & "python3-pip" (y/n)' -n 1 -r
# read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
sudo apt-get install python3 python3-pip -y
VER="pip3"
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
