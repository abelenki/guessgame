import cgi
import datetime , Cookie , random , os, sha,time

import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class ScoreBoard(db.Model):
  name = db.StringProperty()
  attempts = db.IntegerProperty()
  answer = db.IntegerProperty()
  start_time = db.StringProperty()
  end_time = db.StringProperty()
  finish = db.BooleanProperty()
  delay = db.StringProperty()


class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))


class Start(webapp.RequestHandler):
  def post(self):
    ke = sha.new(repr(datetime.datetime.now())).hexdigest()
    score = ScoreBoard(key_name=ke)
    name = score.name = self.request.get('name')
    answer = score.answer = random.randint(1,999)
    start_time = datetime.datetime.now()
    score.key_name = 'siddhartha'
    score.start_time = str(start_time)
    score.attempts = 0
    score.put()
    template_values = {
            'start_time': start_time,
            'name': name,
            'key': ke
        }
    path = os.path.join(os.path.dirname(__file__), 'start.html')
    self.response.out.write(template.render(path,template_values))

  def get(self):
    self.redirect('/')
    
class Play(webapp.RequestHandler):
  def post(self):
    start_date = self.request.get('start_time')
    ke = self.request.get('key')
    name =  self.request.get('name')
    sb = ScoreBoard()
    use = db.GqlQuery("SELECT * FROM ScoreBoard WHERE name = :1 AND start_time = :2", name,start_date)
    try:
      record = db.Key.from_path('ScoreBoard', ke)
      rec = db.get(record)
      rec.attempts = rec.attempts + 1
      atm = rec.attempts
    except:
      s = 1


    for us in use:
      name = us.name
      answer = us.answer
      #us.attempts = us.attempts + 1
    
    et = None
    dt = 0
    #self.response.out.write('%s <br />' % answer)
    value = int(self.request.get('value'))
    #self.response.out.write('%s <br />' % value)
    if answer == value:
      flag = 0
      et = datetime.datetime.now()
      sd = start_date[:-7]
      st = datetime.datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")
      dt = et - st
      rec.finish = True
      rec.delay = str(dt)
      #self.response.out.write('You have completed in :: %s'% dt)
      rec.end_time = str(et)
    elif answer < value:
      flag = 1
      #self.response.out.write('You have entereda too large number... ')
    else:
      flag = -1
      #self.response.out.write('You have entered a too small number... ')

    rec.put()

    template_values = {
            'start_time': start_date,
            'name': name,
            'key': ke,
            'flag' : flag,
            'attempts' : atm,
            'endtime' : et,
            'delay' : dt,
            'c1' : random.randint(0,256),
            'c2' : random.randint(0,256),
            'c3' : random.randint(0,256),
            'prev' : value
        }
    path = os.path.join(os.path.dirname(__file__), 'play.html')
    self.response.out.write(template.render(path,template_values))

  def get(self):
    self.redirect('/')
    
class Scores(webapp.RequestHandler):
  def get(self):
    use = db.GqlQuery("SELECT * FROM ScoreBoard WHERE finish = True ORDER BY attempts,delay ASC")
    template_values ={
      'board' : use
    }
    path = os.path.join(os.path.dirname(__file__), 'scores.html')
    self.response.out.write(template.render(path,template_values))


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/start', Start),
  ('/play',Play),
  ('/score',Scores)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
