# Flask app

```sh
git clone 
cd app
virtualenv env
env\Scripts\activate.bat
pip install -r requirements.txt
export FLASK_APP="entrypoint"
export FLASK_ENV="development"
export FLASK_DEBUG=1
echo $FLASK_DEBUG
python -m flask run
```