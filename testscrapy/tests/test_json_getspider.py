import requests

session1=requests.session()
# response1=session1.request(method='get',url='http://localhost:6800/listspiders.json',params={'project':'default'})
# http://localhost:6800/schedule.json -d project=myproject -d spider=somespider

response1=session1.request(method='post',url='http://localhost:6800/schedule.json',params={'project':'default','spider':'spider1'})

print(response1.text)
session1.close()