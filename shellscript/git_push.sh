#!/bin/sh

echo "pushing automatically."

git pull origin master
git add .

if [ $# -gt 0 ]
then 
    git commit -m "$*"
    git push origin master
else
    echo ""
    echo "No arguments"
    echo "Comment of commiting will be \"updated resume program shellscript.\""
    echo "Do you continue? (y/n)"
    read ANSWER
    if [ "$ANSWER" == "y" ]
    then
        git commit -m "updated program using shellscript."
        git push origin master
        open -a "/Applications/Google Chrome.app" https://github.com/chikurin66/graduation-thesis.git
    else
        echo "Please enter the message to commit"
    fi
fi

