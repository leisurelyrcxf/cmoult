#!/bin/bash

#Builds CherryPy and Django form sources

cherrymd5=542b96b2cd825e8120e8cd822bc18f4b
djangomd5=3f5d2f7b94350832094084acbb3a9de4
python=python-dsu3

function dlpatch {
    #fetch CherryPy
    echo "Fetching CherryPy 3.8.0"
    wget --quiet https://pypi.python.org/packages/source/C/CherryPy/CherryPy-3.8.0.tar.gz

    #Check md5sum 
    md5=$(md5sum CherryPy-3.8.0.tar.gz | cut -d' ' -f1)
    if [ "$md5" == "$cherrymd5" ]
    then
        echo "md5sum of CherryPy OK"
        tar -xzf CherryPy-3.8.0.tar.gz
        #Apply patch
        echo "Patching ..."
        pushd CherryPy-3.8.0
        patch -p1 < ../cherrypy.diff
        popd
        echo "complete"
        echo "Downloading Django 1.8"
        wget --quiet https://github.com/django/django/archive/1.8.tar.gz
        md5=$(md5sum 1.8.tar.gz | cut -d' ' -f1)
        if [ "$md5" == "$djangomd5" ]
        then
            echo "md5sum of Django 1.8 OK"
            tar -xzf 1.8.tar.gz
        else
            echo "wrong md5sum on Django 1.8.tar.gz, could not continue"
            exit 1
        fi
    else
        echo "wrong md5sum on CherryPy-3.8.0.tar.gz, could not continue"
        exit 1
    fi
}

function clean {
    echo "Cleaning"
    rm -rf CherryPy-3.8.0
    rm -rf django-1.8
    rm CherryPy-3.8.0.tar.gz
    rm 1.8.tar.gz
}

function install {
    echo "Installing CherryPy"
    echo $@
    pushd CherryPy-3.8.0
    $python setup.py install $@
    popd
    echo "Installing Django"
    pushd django-1.8
    $python setup.py install $@
    popd
}


#Parse the command line
while [[ $# > 0 ]]
do
    key="$1"
    case $key in
        -p|--python)
            python=$2
            shift
            ;;
        -f|--prefix)
            pref=$2
            shift
            ;;
        -i|--install)
            ins="yes"
            ;;
        -c|--clean)
            cl="yes"
            ;;
        -h|--help)
            echo "Downloads and installs libraries for Django example"
            echo "Usage : ./build.sh [option1 [value1]] [option2 [value2]]"
            echo "-p (--python) <interpreter> sets python interpreter (python-dsu3 by default)"
            echo "-f (--prefix) <prefix> sets specific install prefix"
            echo "-i (--install) asks for installations of libraries"
            echo "-c (--clean) cleans before downloading"
            echo "-h (--help) shows this help"
            exit 0
            ;;
        *)
            ;;
    esac
    shift
done

if [ -v cl ]
then

    clean
fi

dlpatch

if [ -v ins ]
then
    if [ -v pref ]
    then
        echo "lama"
        install --pref $pref
    else
        install
    fi
fi
exit 0
