

## cjjeake's Resume Site

Build with the help of the Michigan Hackers.
See their awesome tutorial for getting started making websites at: 
https://github.com/michiganhackers/heroku-py-demo.git

----
## Below are reminders for myself and other on how to build and use the actual project:

### Locally Running
- Run `virtualenv venv --distribute` to start up a virtual environment. 
- Run: `source venv/bin/activate` to start up the virtualenv.
- Install Flask: `pip install -r requirements.txt`.
- Type `python server.py` to run the app.
- Navigate to `http://localhost:3000/`

### Deploy

1. `heroku login`
2. `heroku create [yourappname]` Make up a great app name.
3. `git push heroku master` (If you dont have an ssh key on Heroku see below.)

##### Heroku will install dependences and launch your app here. Magic!

- `heroku ps:scale web=1` This gives your app one `web worker`.
- `heroku open` This will go to yourappname.herokuapp.com
