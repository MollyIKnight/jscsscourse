fout=open('archive.html','w',encoding='utf-8')
#!doctype has to be put in first to declare this is a html doc
#head is the header
#<title> tag is compulsory
#<meta> tag is self closing
fout.write('''<!doctype html>
<html>
  <head>
    <title>Your Mastodon Archive</title>
    <meta charset='utf-8'>
  </head>
  <body style="background-color:AliceBlue;text-align:left">''')
bodynest = 1

import json
#import codecs
import re

outbox = open("outbox.json",encoding='utf-8')
poststr = outbox.read()
outbox.close()
oball = json.loads(poststr) #all contents of outbox
#the loading from string somehow works a bit faster than load to load from file
#posts = json.load(outbox)
#---following is to prettify the indent for outbox json; it's been done once for manual viewing--
#prettyout = open('pout.json','w', encoding='utf-8')
#prettyout.write(json.dumps(oball, indent=4, ensure_ascii=False))
#prettyout.close()

#'orderedItems' attr is the actual post structure; extract posts as list
posts = oball['orderedItems'] 
#print(len(posts))

#structure of posts: 1st layer: 'published'-publish time; 'to': in reply to; 'object': the main text, Chinese encoding in gbk.
#2nd main layer: object. attributes are:
#id: unique identifier link
#type: Note - normal text; Announce - retoot
#summary: the cw folding
#content: main text that should be shown
#inReplyTo: previous toot this one is linked to
#published: publish time of THIS toot
#rest is not essential
def write_post():
    public = False
    for cc in thisone['cc']:
       if re.search('#Public',cc):
           public = True
           break
    if public:
        fout.write('<p style="background-color:Bisque">')
    else:
        fout.write('<p style="background-color:SeaShell">')
    if thisone['object']['summary']:
        fout.write('<div>Summary: '+thisone['object']['summary']+'</div>')
    if thisone['object']['attachment']:
        fout.write('<div">This toot has attachment. Click on time tag to view in original link</div>')
    fout.write(re.findall('<p>(.*)</p>',thisone['object']['content'])[0])
    fout.write('<div><a href='+thisone['object']['id']+' target="_blank">')
    fout.write(thisone['published'])
    fout.write('</a></div></p>')

def write_retoot():
    fout.write('<p style="background-color:Lavender;color:DarkSlateGray">')
    fout.write('<div">This is a retoot: original link on time tag </div>')
    fout.write(thisone['object'])
    fout.write('<br><a href='+thisone['object']+' target="_blank">')
    fout.write(thisone['published'])
    fout.write('</a></p>')
    
for item in range(len(posts)):
    
    thisone = posts[item]
    
    if thisone['type'] == 'Announce':
        write_retoot()
    if thisone['type'] == 'Create':
        write_post()
    fout.write('<hr>')
 

fout.write('</body>')
fout.close()