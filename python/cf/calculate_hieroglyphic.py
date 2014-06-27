import sys, itertools, re
from pyparsing import *
import operator as op

'''

Author: Zalvie / Cake
Status: Not Done
Description: 
             Grab the JS Hieroglyphic and translate it into numbers and calculate to get the answer
             Damn python makes it hard
             
'''


'''
    [DEBUG] CALC: 30  = [['!+[]+!![]+!![]+[]'], '+', ['+[]']]
    [DEBUG] START: 30   = +((!+[]+!![]+!![]+[])+(+[])) 

    [DEBUG] CALC: 5   = ['!+[]+!![]+!![]+!![]+!![]']
    [DEBUG] CALC: 5   = ['!+[]+!![]+!![]+!![]+!![]']
    [DEBUG] CALC: 8   = ['!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]']
    [DEBUG] CALC: 44  = [['!+[]+!![]+!![]+!![]+[]'], '+', ['!+[]+!![]+!![]+!![]']]
    [DEBUG] CALC: 26  = [['!+[]+!![]+[]'], '+', ['!+[]+!![]+!![]+!![]+!![]+!![]']]
    [DEBUG] CALC: 30  = [['!+[]+!![]+!![]+[]'], '+', ['+[]']]
    [DEBUG] CALC: 25  = [['!+[]+!![]+[]'], '+', ['!+[]+!![]+!![]+!![]+!![]']]
    [DEBUG] CALC: 39  = [['!+[]+!![]+!![]+[]'], '+', ['!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]']]
    [DEBUG] CALC: 29  = [['!+[]+!![]+[]'], '+', ['!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]']]

    [DEBUG] OUTPUT: 62078
'''

parse = '''
       var t,r,a,f, GgydmCQ={"FblpsuEanzgG":+((!+[]+!![]+!![]+[])+(+[]))};
        t = document.createElement('div');
        t.innerHTML="<a href='/'>x</a>";
        t = t.firstChild.href;r = t.match(/https?:\/\//)[0];
        t = t.substr(r.length); t = t.substr(0,t.length-1);
        a = document.getElementById('jschl-answer');
        f = document.getElementById('challenge-form');
        ;GgydmCQ.FblpsuEanzgG+=!+[]+!![]+!![]+!![]+!![];GgydmCQ.FblpsuEanzgG-=!+[]+!![]+!![]+!![]+!![];GgydmCQ.FblpsuEanzgG+=!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![];GgydmCQ.FblpsuEanzgG*=+((!+[]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]));GgydmCQ.FblpsuEanzgG-=+((!+[]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]));GgydmCQ.FblpsuEanzgG-=+((!+[]+!![]+!![]+[])+(+[]));GgydmCQ.FblpsuEanzgG-=+((!+[]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]));GgydmCQ.FblpsuEanzgG*=+((!+[]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));GgydmCQ.FblpsuEanzgG+=+((!+[]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));
'''

cat = ["+[]", '+!![]'] + [''.join(['!+[]'] + ['+!![]' for _ in (range(1, i))]) for i in range(2, 10)]

expr = ZeroOrMore(nestedExpr('(', ')') | quotedString | Word(printables, excludeChars="()") | '+')

def debug(*msg):
  print '[DEBUG]', ' '.join(map(str, msg))

def calc(y, z):
  global output
  return ({'+': op.add, '-': op.sub, '*': op.mul, '/': op.div}[z])(output, y)

def iterFlatten(root):
    if isinstance(root, (list, tuple)):
        for element in root:
            for e in iterFlatten(element):
                yield e
    else:
        yield root

def parse_items(l, out=-1):
  if type(l) is str: 
    if l.find('[') == -1: return 0
    else: l = [l]

  for item in list(iterFlatten(list(l))):
    item = str(item) if type(item) is list else ''.join(list(iterFlatten(item)))

    if item.find('[') == -1: continue

    try:
      answer = 1 if item.replace('[]+[]', '[]') == '!![]' else cat.index(item.replace('[]+[]', '[]'))
    except: # Debug
      print '[DAMN U JS]', '{',l,'}', item, type(item),'\n'
      sys.exit()

    out = str(answer) if item.find('[]+[]') != -1 else answer if out == -1 else out + str(answer) if type(out) is str else out + answer

  debug('CALC:', out, '\t=', l)

  return int(out)

start = re.search(r'\W\w+={"\w+":(.*?)\}', parse).group(1)

output = sum([parse_items(items) for items in list(expr.parseString(start).asList())])

debug('START:', output, '\t=', start, '\n')

for i in re.findall(r'(?:\w+)\.(?:\w+)([\*\+\-])=(?:\+|)(.*?)\;', parse):
  if i[0] not in ['*', '-', '+', '/']: # Debug
    sys.exit(i)

  output = calc(sum([parse_items(items) for items in list(expr.parseString(i[1]).asList())]), i[0])

print 
debug('OUTPUT:', output)
print 


