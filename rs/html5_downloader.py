import requests, random, os, re, sys, datetime

os.chdir('/rs')

class lang:
  WORLD                = random.choice([5, 24, 134])
  URL                  = 'http://world%d.runescape.com/html5/client/Bootstrap.js' % WORLD
  HTML_URL             = 'http://secure.runescape.com/m=world%d/html5/client/html5game.ws' % WORLD
  FOUND                = 'Found'
  X_FOUND              = FOUND + ': %s'
  NOT_FOUND            = 'Not ' + FOUND

  APP                  = '[   APP   ]'

  COULD_NOT_FETCH_FILE = (APP, 'Could not fetch the file')
  BOOTSTRAP_NOT_FOUND  = ('[BOOTSTRAP]', NOT_FOUND)
  CLIENT_VERSION_EMPTY = ('[  CV-RE  ]', NOT_FOUND)

  ALREADY_HAS          = ('[   DIR   ]', 'Version is already saved')
  MK_DIR               = '[   DIR   ] Making directory:'

  SAVED                = APP + ' Saved: %s'

  SAVE_PATH            = 'saves/%s'

def err(con, msg, el = lang.FOUND):
  if not con: print ' '.join(msg); print '-' * 64, '\n'; sys.exit()
  elif el:    print msg[0], el

def fetch(URL):
  print lang.APP, 'Downloading:', URL

  r = requests.get(URL)

  err(r.status_code == 200, lang.COULD_NOT_FETCH_FILE, 'File Fetched')

  return r.content

print '-' * 64
print lang.APP, 'Started:', datetime.datetime.now()

data = fetch(lang.URL)

bootstrap = data[data.find('Bootstrap'):]

err(bootstrap.find('client') > 1, lang.BOOTSTRAP_NOT_FOUND, lang.X_FOUND % bootstrap)

version = ''.join(re.findall(r'\((\d+),1', bootstrap))

err(version, lang.CLIENT_VERSION_EMPTY, lang.X_FOUND % version)

lang.SAVE_PATH = os.path.realpath(lang.SAVE_PATH % version)

bootstrap = os.path.join(lang.SAVE_PATH, 'bootstrap.js')

err(not os.path.isdir(lang.SAVE_PATH), lang.ALREADY_HAS, lang.SAVE_PATH)

os.makedirs(lang.SAVE_PATH)

with open(bootstrap, 'w+') as f: f.write(data)

print lang.SAVED % bootstrap

data = fetch(lang.HTML_URL)

with open(bootstrap[:-3] + '.html', 'w+') as f: f.write(data)

print lang.SAVED % bootstrap[:-3] + '.html'
