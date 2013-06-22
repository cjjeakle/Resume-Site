## My Personal Website

Build with the help of the Michigan Hackers.
See their awesome tutorial for getting started making websites at: 
https://github.com/michiganhackers/heroku-py-demo.git

----
## Getting Started:

#### Locally Running for the First Time
- Install python 2.7.x and python virtual envrironment
- Run `virtualenv venv --distribute` to start up a virtual environment. 
- Run: `source venv/bin/activate` to start up the virtualenv.
- Install dependancies: `pip install -r requirements.txt`.
- Type `python server.py` to run the app.
- Navigate to `http://localhost:3000/`

#### Next Time You Develop
- `source venv/bin/activate`
- `python server.py` to run locally.
- `git commit -am "commit message"`
- `git push heroku master` Update Heroku, no need to scale.
- `heroku open`

#### Helpful Documentation
- Flask: http://flask.pocoo.org/docs/quickstart/#
- Jade: https://github.com/visionmedia/jade
- Zurb's Foundation Framework: http://foundation.zurb.com/docs/

#### To work with the foundation framework in this project:
- `[sudo] gem install zurb-foundation`
- `[sudo] gem install compass`
- `[sudo] gem install sass`
- `cd path/to/resume-site/public/my-site.css`
- `compass watch` (this watches for changes in the .scss files and updates the css)
- Do your stuff!

## Deploying the app to Heroku:

#### Deploy
1. `heroku login`
2. `heroku create`
3. `git push heroku master`


