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
    <style>
     body {
         background-color:AliceBlue;
         font-family: arial, Helvetica, sans-serif;
        }
     .publicstatus{
         background-color:Bisque;
         border: 2px solid black;
         text-align:left;
         margin: auto;
         padding:20px;
         width: 80%;

        }
        .privatestatus{
         background-color:Seashell;
         border: 2px solid black;
         text-align:left;
         margin:auto;
         padding:20px;
         width: 80%;

        }
        .retoot{
         background-color:Lavender;
         color:DarkSlateGray;
         border: 2px solid black;
         text-align:left;
         margin:auto;
         padding:20px;
         width: 80%;

        }

         .retoot_self{
         background-color:LightCyan;
         color:DarkSlateGray;
         border: 2px solid black;
         text-align:left;
         margin:auto;
         padding:20px;
         width: 80%;

        }
        .attachment_declare{
        text-align:center;
        }
        .retoot_declare{
        text-align:center;
        }
        .summary_content{
        text-align:center;
        font: bold 30px}
        
        .original_link{
        text-align:center;
        }
    </style>
  </head>
  <body>\n''')
bodynest = 1

import json
import re
import datetime as dt

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
def writecontent(str,fout):
    lines=re.findall('<p>(.*?)</p>',str)
    for i in lines:
       fout.write(i+'<br>')

def date_time_format(tsstr):
    #2020-05-19T11:50:58Z
    ts = dt.datetime.strptime(tsstr, '%Y-%m-%dT%H:%M:%SZ')
    tsfs = ts.strftime('%H:%M:%S, on %a, %d %B %Y') #timstamp format string
    return 'Published at ' + tsfs

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
    if thisone['object']['summary']:
        fout.write('<p class="summary_content">Summary: '+thisone['object']['summary']+'</p> \n')
    if public:
        fout.write('<p class="publicstatus"> \n') #style="background-color:Bisque">')
    else:
        fout.write('<p class="privatestatus"> \n')# style="background-color:SeaShell">')
    writecontent((thisone['object']['content']),fout)
    if thisone['object']['attachment']:
        fout.write('<div class="attachment_declare">This toot has attachment. Click on time tag to view in original link</div> \n')
    fout.write('<div class="original_link"><a href='+thisone['object']['id']+' target="_blank">')
    fout.write(date_time_format(thisone['published']))
    fout.write('</a></div>\n</p>\n')

def write_retoot():
    if isinstance(thisone['object'],dict):
        fout.write('<p class="retoot_self">\n')
        fout.write(thisone['object']['url'])
        fout.write('<div class="retoot_declare">This is a retoot of your own previous toot: original link on time tag </div> \n')
        fout.write('<div class="original_link"> <a href='+thisone['object']['url']+' target="_blank">')
        fout.write(date_time_format(thisone['published']))
        fout.write('</a></div>\n</p>\n')
    else:
        fout.write('<p class="retoot">\n')
        fout.write(thisone['object'])
        fout.write('<div class="retoot_declare">This is a retoot: original link on time tag </div> \n')
        fout.write('<div class="original_link"> <a href='+thisone['object']+' target="_blank">')
        fout.write(date_time_format(thisone['published']))
        fout.write('</a></div>\n</p>\n')
    
for item in range(len(posts)):
    
    thisone = posts[item]
    
    if thisone['type'] == 'Announce':
        write_retoot()
    if thisone['type'] == 'Create':
        write_post()
    
 

fout.write('</body>\n')
fout.close()
