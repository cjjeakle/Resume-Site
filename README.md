## My Personal Website

This is an old version of my personal website. 
The current version can be found at: 
https://github.com/cjjeakle/cjjeakle.github.io

Built with the help of the Michigan Hackers.
See their awesome tutorial for getting started making websites at: 
https://github.com/michiganhackers/heroku-py-demo.git

----
## Some Reminders From the Tutorial:

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
- `git commit -m "commit message"`
- `git push heroku master` Update Heroku, no need to scale.
- `heroku open`

## Other Helpful Information:

#### Documentation
- Flask: http://flask.pocoo.org/docs/quickstart/#
- Jade: https://github.com/visionmedia/jade
- Zurb's Foundation Framework: http://foundation.zurb.com/docs/

#### To work with the foundation framework in this project:
- `[sudo] gem install zurb-foundation`
- `[sudo] gem install compass`
- `[sudo] gem install sass`
- `cd path/to/personal-site/static/my-site.css`
- `compass watch` (this watches for changes in the .scss files and updates the css)
- Do your stuff!


