
cat = ['+[]', '+!![]'] + [''.join(['!+[]'] + ['+!![]' for _ in (range(1, i))]) for i in range(2, 10)]

def calc(s):
  output = None

  for o in ''.join(['\n' if e in list('()') else e for e in list(s)]).split('\n'):
    if '[' not in o: continue

    answer = 1 if o.replace('[]+[]', '[]') == '!![]' else cat.index(o.replace('[]+[]', '[]'))

    if isinstance(output, basestring) or '[]+[]' in o:
        answer = str(answer)
    
    if output == None:
      output = answer 
    else: 
      output += answer

  return output


for l in ['+((!+[]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]))','+((!+[]+!![]+[])+(+!![]))','+((+!![]+[])+(!+[]+!![]+!![]+!![]))','+((!+[]+!![]+[])+(!+[]+!![]+!![]))','!+[]+!![]']:
    print calc(l)
