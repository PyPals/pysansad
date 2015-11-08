from bs4 import BeautifulSoup
import requests
import re

class individual_profile(object):
  """docstring for individual_profile"""
  def __init__(self, url):
    super(individual_profile, self).__init__()
    self.url = url

  def get_value(self):
    req = requests.get(self.url)
    text = req.text
    self.soup = BeautifulSoup(text, 'html5lib')

    #Getting the headings of values
    self.headings = self.soup.find_all(attrs={'class':'views-label'})

    for i in range(len(self.headings)):
      self.headings[i] =   str(self.headings[i].text.split(':')[0])
    #for i in range(len(self.headings)+1, 0, -1):
    #  self.headings[i] = self.headings[i-1]
    #self.headings[0] = 'Name'
    self.headings.append('Image')

    self.all = self.soup.find_all(attrs={'class':'field-content'})
    self.all[0] = self.all[0].find('img')
    self.all.append(self.all.pop(0))
  
  def headings_checker(self, headings):
    for i in self.headings:
      if i not in headings:
        headings.append(i)

  def make_dict(self):
    self.dict = {}
    name = self.soup.find(attrs = {'class':'staticHeading'})
    self.dict['Name'] = name.text

    for i in range(len(self.headings)):
      if self.all[i].text!="":
        self.dict[self.headings[i]] = str(self.all[i].text)
      else:
        self.dict[self.headings[i]] = 'http://india.gov.in' + self.all[i]['src']
    self.headings.append('Name')
    self.get_email()

    #print "done for", self.dict['Name']
    return self.dict

  def extract_email(self, email):
    dot = re.compile('\[dot\]')
    at = re.compile('\[at\]')
    email = dot.sub('.', email)
    email = at.sub('@', email)
    return email

  def get_email(self):
    try:
      email = self.dict['Email Id']
      mails = [] #to save the emails separately before compiling
      dot_nic_in = re.compile('[a-z|-|0\-9]+\[at\]\w+\[dot\]\w+\[dot\]\w+')
      dot_com = re.compile('[a-z|-|0\-9]+\[at\]\w+\[dot\]\w+')

      list_one = re.findall(dot_nic_in, email)
      list_two = re.findall(dot_com, email)
      for i in list_one:
        mails.append(self.extract_email(i))

      for i in list_two:
        if i.find('nic')== -1:
          mails.append(self.extract_email(i))

      email = ', '.join(mails)
      self.dict['Email Id'] = email

    except KeyError:
      self.dict['Email Id'] = 'No email'




if __name__=='__main__':
  url = raw_input('Enter URL: ')
  profile = individual_profile(url)
  profile.get_value()
  #print profile.all[len(profile.all)-1]
  details = profile.make_dict()
  for i in profile.headings:
    print i,details[i]
  print details['Email Id']