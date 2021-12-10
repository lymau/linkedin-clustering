# Text Clustering User Description LinkedIn 

Simple implementation of short text clustering algorithm in Flask web app.

### Development

1. Clone this repository.  
2. Make a new environtment.  

<b>Linux</b>
```shell
$ python3 -m venv venv
```

<b>Windows</b>  
```cmd
py -3 -m venv venv
```

3. Install the dependencies. 
```shell
$ pip install -r requirements.txt
```
4. Set the variable.  

<b>Linux</b>
```shell
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

<b>Windows</b>  
CMD
```cmd
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```
PowerShell
```powershell
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
> flask run
```
5. Start developing!