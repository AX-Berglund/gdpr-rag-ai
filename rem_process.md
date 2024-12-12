# Reminder of what you have done

## Creating venv
mkvirtualenv --python=/usr/local/bin/python3.8 gdpr-env 
workon gdpr-env
pip install ipykernel
(gdpr-env) ➜  gdpr-rag-ai git:(main) ✗ python -m ipykernel install --user --name=gdpr-env --display-name "Python (gdpr-env)"
 - Installed kernelspec gdpr-env in /Users/axhome/Library/Jupyter/kernels/gdpr-env

## Installs
**This is supposed to be simple and fast**
pip install PyPDF2
**This is supposed to be more robust**
pip install pdfminer.six

pip install nltk
