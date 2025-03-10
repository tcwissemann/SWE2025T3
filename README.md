Created using Python 13.3.1 - requirement
Using https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack on vscode - nice to have

clone the git repo

create a virtual environment
CMD + SHIFT + P    ---- > python: create environment ---> venv ---> 13.3.1 ---> select requirements.txt

activate virtual environment
source .venv/bin/activate

if you edit or update the requirements
then run pip install -r requirements.txt 

then cd source and run python manage.py runserver

click the link in console and head to the about/

you can find your pages inside source/about/templates
