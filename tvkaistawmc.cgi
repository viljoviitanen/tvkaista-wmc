#!/usr/bin/env /usr/bin/python
# This Python file uses the following encoding: utf-8
#
# Tvkaista windows media center client
#
# Copyright (C) 2011-2013  Viljo Viitanen <viljo.viitanen@iki.fi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import hashlib,random,sys
import urllib, urllib2 , re, os, htmlentitydefs, time, base64, cgi, Cookie, datetime

from xml.dom import minidom
from xml.sax.saxutils import escape

def scriptname():
    return "/tvkaistawmc.cgi/"

def motd():
    return escape("Tämän rivin viestin voit asettaa lähdekoodissa.")

def debugprint(message):
    #comment out to remove stderr spam
    sys.stderr.write(message+"\n")
    pass

def rr():
  return str(random.randint(1,10000000000))

def sr(content):
  print """Content-Type: text/xml; charset=UTF-8
Content-Length: %d
Last-Modified: %s

%s""" % (len(content),datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S GMT"),content)

def bitrate():
  try:
    if os.environ.get('HTTP_COOKIE').find('quality=mp4') != -1:
      return "mp4"
  except:
    pass
  return "h264"

def additem(title,date,url,tim=""):
  if (tim!=""):
    title='%s %s' % (tim,title)
  return simplebutton(date+" "+title,url)
  
def simplebutton(label,path):
  return """<PropertySet>
<Entries>
<cor:String Name="Title" String="%s"/>
<cor:String Name="Path" String="%s"/>
</Entries>
</PropertySet>
""" % (label.encode('utf-8'),escape(path))

def header():
  return """<Mcml xmlns="http://schemas.microsoft.com/2008/mcml"
  xmlns:addin="assembly://Microsoft.MediaCenter/Microsoft.MediaCenter.Hosting"
  xmlns:cor="assembly://MSCorlib/System"
  xmlns:con="/static/Controls2.xml"
  xmlns:me="Me">
  <UI Name="Default">
   <Locals>
      <ArrayListDataSet Name="Data">
        <Source>
"""

def footer(message=""):
  return """
        </Source>
      </ArrayListDataSet>
 
      <ScrollingHandler Name="ScrollingHandler" HandlerStage="Bubbled"/>

      <ScrollingData Name="ScrollingData" PageStep="1"/>
      <Command Name="Go" />
   </Locals>
   <Rules>
      <Binding Source="[ScrollingData.CurrentPage]" Target="[CurrentPage.Content]">
      <Transformer>
      <FormatTransformer Format="{0:F0}"/>
      </Transformer>
      </Binding>
      <Binding Source="[ScrollingData.TotalPages]" Target="[TotalPages.Content]">
      <Transformer>
      <FormatTransformer Format="/ {0:F0}"/>
      </Transformer>
      </Binding>
      <Default Target="[ScrollingHandler.ScrollingData]" Value="[ScrollingData]"/>
      <Default Target="[ScrollingData.Repeater]" Value="[Rep]"/>
      <Changed Source="[Go.Invoked]">
        <Actions>
          <Invoke Target="[Now.NavigateInto]"/>
        </Actions>
      </Changed>
   </Rules>
   <Content>
      <Panel Layout="Form" >
        <Children> 
          
        <Panel Margins="20,20,20,80">
            <LayoutInput>
              <FormLayoutInput Left="Parent,0.15" Top="Parent,0"  />
            </LayoutInput>
            <Layout>
              <FlowLayout Orientation="Vertical" Spacing="15,0"  />
            </Layout>
            <Children>
%s
                  <Scroller Orientation="Vertical" FadeSize="-15" ScrollingData="[ScrollingData]" >
                    <Children>
                      <Repeater Name="Rep" Source="[Data]">
                        <Layout>
                          <FlowLayout Orientation="Vertical" Spacing="10,0"/>
                        </Layout>
                        <Content>
                          <me:SimpleButton3 Label="[RepeatedItem!PropertySet.#Title.ToString]" Path="[RepeatedItem!PropertySet.#Path.ToString]"/>
                        </Content>
                      </Repeater>
                    </Children>
                  </Scroller>
            </Children>
          </Panel>
          <con:Playing Name="Now" >
            <LayoutInput>
              <FormLayoutInput Left="Parent,0" Bottom="Parent,1"/>
            </LayoutInput>
          </con:Playing>
          <con:PlayingButton Command="[Go]">
            <LayoutInput>
              <FormLayoutInput Left="Parent,0,33" Bottom="Parent,1"/>
            </LayoutInput>
          </con:PlayingButton>
          <Text Name="CurrentPage" Content="" Alpha="0.6" Font="Arial,14" Color="White">
            <LayoutInput>
              <FormLayoutInput Right="Parent,1,-50" Bottom="Parent,1,-50"/>
            </LayoutInput>
	  </Text>
          <Text Name="TotalPages" Content="" Alpha="0.6" Font="Arial,14" Color="White">
            <LayoutInput>
              <FormLayoutInput Left="Parent,1,-50" Bottom="Parent,1,-50"/>
            </LayoutInput>
	  </Text>
        </Children>
      </Panel>
   </Content>
  </UI>
 <UI Name="SimpleButton3">
    <Properties>
      <cor:String Name="Label" cor:String="$Required"/>
      <cor:String Name="Path" cor:String="$Required" />
    </Properties>
    <Locals>
      <ClickHandler Name="Clicker" />
      <ShortcutHandler Name="RecordHandler" Shortcut="Record" Handle="true"/>
      <ShortcutHandler Name="PlayPauseHandler" Shortcut="PlayPause" Handle="true"/>
      <ShortcutHandler Name="PlayHandler" Shortcut="Play" Handle="true"/>
    </Locals>
    <Rules>
      <Default Target="[Input.KeyInteractive]" Value="True"/>
      <Default Target="[Input.KeyFocusOnMouseEnter]" Value="true"/>
      <Condition Source="[Input.KeyFocus]" SourceValue="true">
        <Actions>
          <Set Target="[ButtonPanel.Scale]" Value="1.1,1.1,1.1"/>
          <Set Target="[ButtonPanel.Alpha]" Value="1"/>
        </Actions>
      </Condition>
      <Condition Source="[Input.KeyFocus]" SourceValue="false">
        <Actions>
          <Set Target="[ButtonPanel.Scale]" Value="1,1,1"/>
          <Set Target="[ButtonPanel.Alpha]" Value="0.50"/>
        </Actions>
      </Condition>
      <Condition Source="[Clicker.Clicking]" SourceValue="true">
        <Actions>
          <Navigate Source="[Path]" />
        </Actions>
      </Condition>
      <Rule>
        <Conditions>
          <Modified Source="[PlayPauseHandler.Invoked]"/>
        </Conditions>
        <Actions>
          <Navigate Source="[Path]" >
                      <Data>
                           <cor:String Name="RequestMethod" String="GET"/>
                           <cor:String Name="dummy" String="1"/>
                           <cor:String Name="mode2" String="play"/>
                      </Data>
          </Navigate>
        </Actions>
      </Rule>
      <Rule>
        <Conditions>
          <Modified Source="[PlayHandler.Invoked]"/>
        </Conditions>
        <Actions>
          <Navigate Source="[Path]" >
                      <Data>
                           <cor:String Name="RequestMethod" String="GET"/>
                           <cor:String Name="dummy" String="1"/>
                           <cor:String Name="play" String="1"/>
                           <cor:String Name="mode2" String="play"/>
                      </Data>
          </Navigate>
        </Actions>
      </Rule>
      <Rule>
        <Conditions>
          <Modified Source="[RecordHandler.Invoked]"/>
        </Conditions>
        <Actions>
          <Navigate Source="[Path]" >
                      <Data>
                           <cor:String Name="RequestMethod" String="GET"/>
                           <cor:String Name="dummy" String="1"/>
                           <cor:String Name="mode2" String="rec"/>
                      </Data>
          </Navigate>
        </Actions>
      </Rule>
    </Rules>
    <Content>
      <Panel CenterPointPercent="0,0.5,0.5" Name="ButtonPanel">
        <Animations>
          <Animation Animation="animation://con:ScaleAnim"/>
        </Animations>
        <Children>
          <Text Name="MyLabel" Content="[Label]" Alpha="0.75" Font="Arial,25,Bold" Color="White"/>
        </Children>
      </Panel>
    </Content>
  </UI>
</Mcml>

""" % message

def getsetting(x):
  global setting
  ret=setting.get(x)
  if ret==None:
    return ""
  else:
    return ret


# paavalikko
def menu():
  res=header()
  res+=simplebutton("Kanavat",scriptname()+"?url="+urllib.quote_plus('http://www.tvkaista.fi/feed/channels/')+"&mode=1&random="+rr()) 
  res+=simplebutton("Sarjat",scriptname()+"?url="+urllib.quote_plus('http://www.tvkaista.fi/feed/seasonpasses/')+"&mode=1&random="+rr())
  res+=simplebutton("Lista",scriptname()+"?url="+urllib.quote_plus('http://www.tvkaista.fi/feed/playlist')+"&mode=2&random="+rr())
  res+=simplebutton("Elokuvat",scriptname()+"?url="+urllib.quote_plus('http://www.tvkaista.fi/feed/search/title/elokuva')+"&mode=2&random="+rr())
  res+=simplebutton("Haku",scriptname()+"?&mode=4&random="+rr())
  #additem("Suosituimmat","","?url="+urllib.quote_plus('http://www.tvkaista.fi/feedbeta/programs/popular')+"&mode=2")

  vko=['Maanantai','Tiistai','Keskiviikko','Torstai','Perjantai','Lauantai','Sunnuntai']
  t=time.time()
  for i in range(1,29):
    tt=time.localtime(t-86400*i)
    title='%s %s' % (vko[tt[6]], (time.strftime("%d.%m",tt)))
    res+=simplebutton(title,scriptname()+"?url=%d/%d/%d/&mode=5&random=%s" % (tt[0],tt[1],tt[2],rr()))
  res+=simplebutton("Kirjaudu ulos",scriptname()+"logout?random="+rr())
  res+=footer("""<Text Name="MOTD" Color="White" Alpha="0.20" WordWrap="true" Content="%s"/>""" % motd() )
  sr(res);

def fetch(url):
  if (not re.match('^http://www\.tvkaista\.fi/',url)):
    message("Error: invalid url parameter")
    raise Exception
    
  try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    obj = mc.get(hashlib.md5(url+getsetting("username")+"ABCDEFG"+getsetting("password")).hexdigest())
    if obj:
      debugprint("memcache hit")
      return obj
  except ImportError:
    mc=None
    debugprint("memcache not available")
    
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, "http://www.tvkaista.fi", getsetting("username"), \
                         getsetting("password"))
  opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman))
  
  try:
    request = urllib2.Request(url, headers={'User-Agent': "tvkaista-wmc v1 at "+os.environ["HTTP_HOST"]})
    content = opener.open(request).read()

  except urllib2.HTTPError,e:
    if e.code == 401:
      loginform("Tunnus tai salasana oli väärin")
    else:
      message("Pyynto ei onnistunut (%s): %s " % (e.code,url))
    raise Exception
  if mc:
    debugprint("memcache miss")
    mc.set(hashlib.md5(url+getsetting("username")+"ABCDEFG"+getsetting("password")).hexdigest(),content,300)
  return content

#onko gmt-aikaleima kesaajassa
def isdst(tt):
  dates = {
    2011 : [27,30],
    2012 : [25,28],
    2013 : [31,27],
    2014 : [30,26],
    2015 : [29,25],
    2016 : [27,30],
    2017 : [26,29],
    2018 : [25,28],
    2019 : [31,27],
  }
  t=time.gmtime(tt)
  if t[1] > 3 and t[1]<10:
    return True
  if t[1] < 3 or t[1]>10:
    return False
  if t[1] == 3:
    if t[2] < dates[t[0]][0]:
      return False
    if t[2] == dates[t[0]][0]:
      if t[3] == 0:
        return False
    return True
  if t[1] == 10:
    if t[2] < dates[t[0]][1]:
      return True
    if t[2] == dates[t[0]][1]:
      if t[3] == 0:
        return True
    return False

def listprograms(url):
  try:
    dom = minidom.parseString(fetch(url+'/'+bitrate()+'.rss'))
  except Exception:
    return
  res=header()
  items = dom.getElementsByTagName('item')
  if len(items)==0:
     message("ei ohjelmia")
     return
  #kaanteinen jarjestys kaikkeen paitsi edellisten paivien listauksiin
  if url.count("/feed/archives/")==0:
    items.reverse()
  ret = []
  lyh=['Ma','Ti','Ke','To','Pe','La','Su']
  count=0
  for i in items:
    count=count+1
    if count > 25 and "xelokuva" in url:
      break
    ptit=i.getElementsByTagName('title')[0].childNodes[0].nodeValue
    try:
      pdes=i.getElementsByTagName('description')[0].childNodes[0].nodeValue.replace('"',"'")
    except:
      pdes=""
    pdat=i.getElementsByTagName('pubDate')[0].childNodes[0].nodeValue
    pcha=i.getElementsByTagName('source')[0].childNodes[0].nodeValue
    try:
      purl=i.getElementsByTagName('enclosure')[0].attributes['url'].value
    except:
      purl="PUUTTUU"
      ptit="*"+ptit+"* TALLENNE PUUTTUU *"
    if len(pdes)>140:
      shortdes=pdes[:140]+'...'
    else:
      shortdes=pdes
    tt=time.mktime(time.strptime(pdat,"%a, %d %b %Y %H:%M:%S +0000"))
    if (isdst(tt)):
      timediff=10800
    else:
      timediff=7200
    t=time.gmtime(tt+timediff)
    kuvaus = "%s\n%s %s - %s (%s)" % (ptit,lyh[t[6]],time.strftime("%d.%m.",t),pdes,pcha)

    res+=additem(escape(ptit),time.strftime("%d.%m.",t),scriptname()+"?url="+urllib.quote_plus(purl)+"&mode=0&desc="+urllib.quote_plus(kuvaus.encode('utf-8'))+"&random="+rr(),time.strftime("%H:%M",t))
  
  dom.unlink()
  res+=footer()
  sr(res)

def listfeeds(u,archive=False):
  if archive:
    url='http://www.tvkaista.fi/feed/channels/'
  else:
    url=u
  try:
    dom = minidom.parseString(fetch(url))
  except Exception:
    raise
  items = dom.getElementsByTagName('item')
  res=header()
  dat=''
  if "/feed/seasonpasses" in url:
    items.sort(key=lambda i: i.getElementsByTagName('title')[0].childNodes[0].nodeValue)
  for i in items:
    ptit=i.getElementsByTagName('title')[0].childNodes[0].nodeValue
    plin=i.getElementsByTagName('link')[0].childNodes[0].nodeValue
    if archive:
      plin=re.sub(r'/feed/','/feed/archives/'+u,plin)
      dat=u'virheellinen pvm'
      #paivamaara urlista
      match=re.search('(\d+)/(\d+)/(\d+)/',u)
      try:
        dat="%02d.%02d" % (int(match.group(3)),int(match.group(2)))
      except AttributeError:
        pass
    res+=simplebutton(dat+" "+escape(ptit),scriptname()+"?url="+urllib.quote_plus(plin)+"&mode=2"+"&random="+rr())
  dom.unlink()
  res+=footer()
  sr(res)

  # hakutulokset
def search(param):
  if None==param:
    message("Hakuparametri oli tyhjä")
    return
  if param in " " "  " "   ":
    message("Hakuparametri oli pelkkä välilyönti")
    return
  url = 'http://www.tvkaista.fi/feed/search/title/%s' % urllib.quote_plus(param)
  try:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    sc = cookie["search"].value
  except (Cookie.CookieError, KeyError):
    sc = ""
  list = []
  if sc != "":
    try:
      list = base64.b64decode(sc).splitlines()
    except IndexError:
      pass
  try:
    list.remove(param)
  except ValueError:
    pass
  if len(list)>8: list.pop()
  list.insert(0,param)
  expiration = datetime.datetime.now() + datetime.timedelta(days=1000)
  cookie = Cookie.SimpleCookie()
  cookie["search"] = base64.b64encode("\n".join(list)) 
  cookie["search"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
  print cookie.output()
  listprograms(url)

def play(url,desc,mode2):
  if url=="PUUTTUU":
    message("Tallenne puuttuu.")
    return
  
  try:
    number=url.split('/')[5].split('.')[0]
    link2=scriptname()+"?url="+urllib.quote_plus('http://www.tvkaista.fi/feedbeta/programs/'+number+'/suggestions')+"&mode=2&random="+rr()
  except:
    link2=''
  try:
    nimi=desc.splitlines()[0]
    nimi=nimi.split(':')[0]
    link1=scriptname()+"?url="+urllib.quote_plus(nimi)+"&mode=3&random="+rr()
  except:
    link1=''

  ruletoplay=""
  if mode2=="play":
    ruletoplay="""
      <Rule>
        <Actions>
          <Invoke Target="[AddInHost.MediaCenterEnvironment.PlayMedia]" 
                  mediaType="Video" media="[MediaPath]" addToQueue="false"/>
          <Invoke Target="[AddInHost.MediaCenterEnvironment.MediaExperience.GoToFullScreen]"/>
        </Actions>
      </Rule>"""

  sr("""<Mcml xmlns="http://schemas.microsoft.com/2008/mcml"
  xmlns:addin="assembly://Microsoft.MediaCenter/Microsoft.MediaCenter.Hosting"
  xmlns:cor="assembly://MSCorlib/System" 
      xmlns:con="/static/Controls2.xml"
      xmlns:me="Me">

  <UI Name="play">
    <Locals>
      <addin:AddInHost Name="AddInHost"/>
      <cor:String Name="MediaPath" String="%s"/>
      <Command Name="Go" />
      <Command Name="Play" />
      <Command Name="Add" />
      <Command Name="Search" />
      <Command Name="Suggest" />
      <Command Name="Menu" />
    </Locals>
    <Rules>
%s
      <Rule>
        <Conditions>
          <Modified Source="[Play.Invoked]"/>
        </Conditions>
        <Actions>
          <Invoke Target="[AddInHost.MediaCenterEnvironment.PlayMedia]" 
                  mediaType="Video" media="[MediaPath]" addToQueue="false"/>
          <Invoke Target="[AddInHost.MediaCenterEnvironment.MediaExperience.GoToFullScreen]"/>
        </Actions>
      </Rule> 
      <Rule> 
        <Conditions>
          <Modified Source="[Go.Invoked]"/>
        </Conditions>
        <Actions>
          <Invoke Target="[Now.NavigateInto]"/>
        </Actions>
      </Rule> 
      <Rule> 
        <Conditions>
          <Modified Source="[Menu.Invoked]"/>
        </Conditions>
        <Actions>
           <Navigate Source="%s" />
        </Actions>
      </Rule> 
      <Rule> 
        <Conditions>
          <Modified Source="[Search.Invoked]"/>
        </Conditions>
        <Actions>
           <Navigate Source="%s" />
        </Actions>
      </Rule> 
      <Rule> 
        <Conditions>
          <Modified Source="[Suggest.Invoked]"/>
        </Conditions>
        <Actions>
           <Navigate Source="%s" />
        </Actions>
      </Rule> 
    </Rules>
  <Content>
     <Panel Layout="Form"> 
     <Children>
      <Panel Margins="20,20,20,20">
           <LayoutInput>
              <FormLayoutInput Left="Parent,.15"  />
            </LayoutInput>

            <Layout>
              <FlowLayout Orientation="Vertical" Spacing="10,0"  />
            </Layout>
          <Children>
            <Text Name="Message" Color="White" Alpha="0.50" WordWrap="true" Content="%s"/>
            
            <con:SimpleButton Label="Toista" Command="[Play]" />
<!--
            <con:SimpleButton Label="Lisää katselulistalle" Command="[Add]" />
-->
            <con:SimpleButton Label="Hae samannimisiä" Command="[Search]" />
            <con:SimpleButton Label="Ohjelmaehdotukset" Command="[Suggest]" />
            <con:SimpleButton Label="Takaisin päävalikkoon" Command="[Menu]" />
         </Children>
      </Panel>
          <con:Playing Name="Now" >
            <LayoutInput>
              <FormLayoutInput Left="Parent,0" Bottom="Parent,1"/>
            </LayoutInput>
          </con:Playing>
          <con:PlayingButton Command="[Go]">
            <LayoutInput>
              <FormLayoutInput Left="Parent,0,33" Bottom="Parent,1"/>
            </LayoutInput>
          </con:PlayingButton>
     </Children>
    </Panel>     
  </Content>
  </UI>
</Mcml>""" % (
 escape(url+"?username="+urllib.quote_plus(getsetting("username"))+"&password="+urllib.quote_plus((getsetting("password")))),
 ruletoplay,
 scriptname()+"?random="+rr(),
 escape(link1),
 escape(link2),
 escape(desc),
))



def searchform():
  ps="""<Text Name="Aiemmat" Color="White" Alpha="0.20" WordWrap="true" Content="Aiemmat haut:"/>"""
  try:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    sc = cookie["search"].value
  except (Cookie.CookieError, KeyError):
    sc = ""
  if sc != "":
    try:
      searches = base64.b64decode(sc).splitlines()
    except IndexError:
      searches = ()
    for i in searches:
      ps+="""<con:SimpleButton2 Label="%s" Path="%s"/>""" % ( escape(i),scriptname()+"?mode=3&amp;url="+urllib.quote_plus(i)+"&amp;random="+rr() )
  sr("""<Mcml xmlns="http://schemas.microsoft.com/2008/mcml"
  xmlns:addin="assembly://Microsoft.MediaCenter/Microsoft.MediaCenter.Hosting"
  xmlns:cor="assembly://MSCorlib/System"
  xmlns:con="/static/Controls2.xml"
>
 <UI Name="search">
      <Locals>
        <addin:AddInHost Name="AddInHost"/>
        <EditableText Name="search" Value="" />
        <TypingHandler Name="texth" PasswordMasked="false" MaxLength="50" />
        <Command Name="Go" />
      </Locals>

      <Rules>
        <Binding Source="[search.Value]" Target="[DisplaySearch.Content]" />
        <Binding Source="[search]" Target="[texth.EditableText]" />
        <Changed Source="[Go.Invoked]">
          <Actions>
            <Invoke Target="[Now.NavigateInto]"/>
          </Actions>
        </Changed>
      </Rules>

  <Content>
     <Panel Layout="Form">
     <Children>
      <Panel Margins="20,20,20,50">
           <LayoutInput>
              <FormLayoutInput Left="Parent,.15"  />
            </LayoutInput>

            <Layout>
              <FlowLayout Orientation="Vertical" Spacing="10,0"  />
            </Layout>
          <Children>
            <Panel>
            <Layout>
              <FlowLayout Orientation="Horizontal" Spacing="40,0"  />
            </Layout>
            <Children>
               <con:SimpleButton Label="Hakusana">
               <Command>
                <InvokeCommand Description="Open the Onscreen Keyboard"
                               Target="[AddInHost.MediaCenterEnvironment.ShowOnscreenKeyboard]"
                               editableText="[texth.EditableText]"
                               passwordMasked="[texth.PasswordMasked]"
                               maxLength="[texth.MaxLength]"/>
              </Command>
              </con:SimpleButton>
              <Text Name="DisplaySearch" Color="White" Alpha="0.50" />
              </Children>
            </Panel>
            <con:SimpleButton Label="Hae" >
                <Command>
                  <NavigateCommand Source="%s">
                      <Data>
                           <cor:String Name="RequestMethod" String="%s"/>
                           <ObjectPath Name="dummy" ObjectPath="[search.Value]"/>
                           <ObjectPath Name="url" ObjectPath="[search.Value]"/>

                      </Data>
                  </NavigateCommand>
                </Command>
            </con:SimpleButton>
%s
         </Children>
      </Panel>
      <con:Playing Name="Now" >
            <LayoutInput>
              <FormLayoutInput Left="Parent,0" Bottom="Parent,1"/>
            </LayoutInput>
      </con:Playing>
      <con:PlayingButton Command="[Go]">
            <LayoutInput>
              <FormLayoutInput Left="Parent,0,33" Bottom="Parent,1"/>
            </LayoutInput>
      </con:PlayingButton>
     </Children>
    </Panel>     
  </Content>
 </UI>
</Mcml>""" % (scriptname()+"?mode=3&amp;random="+rr(),getmethod(),ps))


def loginform(text=""):
  sr("""<Mcml xmlns="http://schemas.microsoft.com/2008/mcml"
  xmlns:addin="assembly://Microsoft.MediaCenter/Microsoft.MediaCenter.Hosting"
  xmlns:cor="assembly://MSCorlib/System"
  xmlns:con="/static/Controls2.xml"
>
 <UI Name="login">
      <Locals>
        <addin:AddInHost Name="AddInHost"/>
        <EditableText Name="user" Value="%s" />
        <EditableText Name="pass" Value="" />
        <TypingHandler Name="texth" PasswordMasked="false" MaxLength="50" />
        <TypingHandler Name="passh" PasswordMasked="true" MaxLength="50" />
      </Locals>

      <Rules>
        <Binding Source="[user.Value]" Target="[DisplayUser.Content]" />
        <Binding Source="[user]" Target="[texth.EditableText]" />
        <Binding Source="[pass.Value]" Target="[DisplayPass.Content]" />
        <Binding Source="[pass]" Target="[passh.EditableText]" />
      </Rules>

  <Content>
     <Panel Layout="Form">
     <Children>
      <Panel Margins="20,20,20,20">
           <LayoutInput>
              <FormLayoutInput Left="Parent,.15"  />
            </LayoutInput>

            <Layout>
              <FlowLayout Orientation="Vertical" Spacing="10,0"  />
            </Layout>
          <Children>
            <Text Name="Welcome" Color="White" Alpha="0.50" Content="TVkaista Windows Media Center"/>
            <Text Name="Message" Color="White" Alpha="0.50" Content="%s"/>
            <Panel>
            <Layout>
              <FlowLayout Orientation="Horizontal" Spacing="40,0"  />
            </Layout>
            <Children>
               <con:SimpleButton Label="Käyttäjätunnus">
               <Command>
                <InvokeCommand Description="Open the Onscreen Keyboard"
                               Target="[AddInHost.MediaCenterEnvironment.ShowOnscreenKeyboard]"
                               editableText="[texth.EditableText]"
                               passwordMasked="[texth.PasswordMasked]"
                               maxLength="[texth.MaxLength]"/>
              </Command>
              </con:SimpleButton>
              <Text Name="DisplayUser" Color="White" Alpha="0.50" />
              </Children>
            </Panel>
            <Text Name="DisplayPass" Color="White" Visible="false"/>
          <con:SimpleButton Label="Salasana">
              <Command>
                <InvokeCommand Description="Open the Onscreen Keyboard"
                               Target="[AddInHost.MediaCenterEnvironment.ShowOnscreenKeyboard]"
                               editableText="[passh.EditableText]"
                               passwordMasked="[passh.PasswordMasked]"
                               maxLength="[passh.MaxLength]"/>
              </Command>
            </con:SimpleButton>
            <con:SimpleButton Label="Kirjaudu sisään" >
                <Command>
                  <NavigateCommand Source="%s">
                      <Data>
                           <cor:String Name="RequestMethod" String="%s"/>
                           <ObjectPath Name="dummy" ObjectPath="[user.Value]"/>
                           <ObjectPath Name="user" ObjectPath="[user.Value]"/>
                           <ObjectPath Name="pass" ObjectPath="[pass.Value]"/>

                      </Data>
                  </NavigateCommand>
                </Command>
            </con:SimpleButton>
            <Text Name="Author" Color="White" Alpha="0.20" Content="Sovelluksen on tehnyt Viljo Viitanen"/>
            <Text Name="Motd" Color="White" Alpha="0.20" WordWrap="true" Content="%s"/>
         </Children>
      </Panel>
     </Children>
    </Panel>     
  </Content>
 </UI>
</Mcml>""" % (escape(getsetting("username")),text,scriptname()+"login?random="+rr(),getmethod(),motd()))
  

def message(text="[virhe]",path=""):
  if path=="":
    path=scriptname()+"?random="+rr() 
  res=header()
  res+=simplebutton("Jatka",path)
  msg="""<Text Name="Message" Color="White" Alpha="0.50" Content="%s"/>""" % (text)
  res+=footer(msg)
  sr(res)


#handle login form post, set auth cookie
def login():
  form = cgi.FieldStorage()
  username=form.getfirst("user","")
  password=form.getfirst("pass","")
  expiration = datetime.datetime.now() + datetime.timedelta(days=1000)
  cookie = Cookie.SimpleCookie()
  cookie["auth"] = base64.b64encode(username+':'+password) 
  cookie["auth"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
  print cookie.output()
  message("ok")

#delete auth cookie
def logout():
  cookie = Cookie.SimpleCookie()
  cookie["auth"] = ""
  cookie["auth"]["expires"] = "Sat, 29-Jan-2011 00:00:00 GMT"
  print cookie.output()
  message("Olet kirjautunut ulos.")


def getmethod():
  if os.environ['SERVER_PORT'] == "8080":
    return "GET"
  else:
    return "GET"

def main():
  global setting
  setting=dict()
  
  path=os.environ.get('REQUEST_URI')
  if "/login" in path:
    login()
    return
  if "/logout" in path:
    logout()
    return
  if "/link" in path:
    print "Content-Type: text/html\n\n<a href=\"windowsmediacenterweb://"+os.environ["HTTP_HOST"]+scriptname()+"\">windows media center link</a>"
    return
  
  url=None
  mode=None
  random=None
  desc=""
  mode2=None
  try:
    params=cgi.parse_qs(os.environ.get('QUERY_STRING'))
    random=params["random"][0]
    mode=int(params["mode"][0])
    url=cgi.escape(params["url"][0],True)
    desc=params["desc"][0]
    mode2=params["mode2"][0]
  except(KeyError):
    pass
  if (random == None):
    print "Location: http://"+os.environ["HTTP_HOST"]+scriptname()+'?random='+rr()

  try:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    auth = cookie["auth"].value
  except (Cookie.CookieError, KeyError):
    debugprint("cookie or keyerror")
    loginform()
    return
  try:
    user_pass_parts = base64.b64decode(auth).split(':')
    setting['username'] = user_pass_parts[0]
    setting['password'] = user_pass_parts[1]
  except IndexError:
    debugprint("indexerror")
    loginform()
    return

  if mode==0:
          play(url,desc,mode2)
  elif mode==1:
          listfeeds(url)
  elif mode==2:
          listprograms(url)
  elif mode==3:
          search(url)
  elif mode==4:
          searchform()
  elif mode==5:
          listfeeds(url,True)
  else:
          menu()

if __name__ == "__main__":
    main()
