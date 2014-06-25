# Cute new protection using how js loves to do true false math <.<

url = require 'url', jsdom = require 'jsdom', request = require 'request'

jsdom.defaultDocumentFeatures = ProcessExternalResources: false
j = request.jar()

request = request.defaults({jar: j})

host = url.parse "http://vpsfrom.us"

console.log '    [URL]', host.href

request.get host.resolve('/'), (error, response, body) ->
  if (error || response.statusCode != 503)
    return console.log 'No CF?'

  document = jsdom.jsdom(body).parentWindow.window.document
  
  token = document.getElementsByName("jschl_vc")[0].value

  script = document.getElementsByTagName("script")[0].innerHTML
  script = (/setTimeout\(function\(\)\{([^]*?)f\.submit\(\)\;/m.exec(script)[1]).replace(/(^\s+[fat].*?$)/gm, '').replace(/[\n|\r|\s]/g, "").replace(/var([\w]+,)+/, "t=\"" + host.host + "\";").replace(/a\.value/, "answer")
  eval script # Totally "safe" yo

  console.log ' [ANSWER]', answer
  console.log '  [TOKEN]', token

  request.get host.resolve('/cdn-cgi/l/chk_jschl?jschl_vc=' + token + '&jschl_answer=' + answer), (error, response, body) ->
    if (error || response.statusCode != 200)
      return console.log 'Welp, we tried at least'

    console.log '[COOKIES]', j.getCookieString(host.href)
