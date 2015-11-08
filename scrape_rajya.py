import requests
import csv
from bs4 import BeautifulSoup
from individual_profile import individual_profile
from time import sleep

url ='http://india.gov.in/my-government/indian-parliament/rajya-sabha?page='
headings = ['Name']
data = []

for i in range(10):
  print len(data)
  curr_url = url + str(i)
  req = requests.get(curr_url)

  if req.status_code == 200:
    body = req.text
    if body.find("No record found") == -1:
      soup = BeautifulSoup(body, "html5lib")
      all_url = soup.find_all(attrs = {'class':'field-content'})
      remove = [] #Contains tags to be removed

      for i in all_url:
        if i.find('a') is None:
          remove.append(i)
        else:
          anchor = i.find('a')
          parliament = '/my-government/indian-parliament/'
          if anchor['href'].find(parliament) == -1:
            remove.append(i)

      #Removing unnecessary tags
      for i in remove:
        all_url.pop(all_url.index(i))

      #Saving all URLs
      for i in range(len(all_url)):
        all_url[i] = 'http://india.gov.in' + all_url[i].find('a')['href']

      for i in all_url:
        profile = individual_profile(i)
        profile.get_value()
        profile.headings_checker(headings)
        data.append(profile.make_dict())
        sleep(1)

print len(data)
with open('rajya_sabha.csv', 'a') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames = headings)
  writer.writeheader()
  for i in data:
    writer.writerow(i)