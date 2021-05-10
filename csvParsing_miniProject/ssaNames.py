#!/usr/bin/env python
# coding: utf-8

# In[6]:


#https://www.ssa.gov/oact/babynames/limits.htmlhttps://www.ssa.gov/oact/babynames/limits.html

from csv import DictReader



ssnames = {'year':{},'fname':{}, 'gender':{}, 'count':{}}


ftxt='yob'
yob = 1880
ftyp='.txt'

while yob < 2020:
    filename = ftxt + str(yob) + ftyp

    with open (filename) as ssnfile:
        dreader = DictReader(ssnfile, fieldnames=['name','sex', 'number'])
        for record in dreader:
 
            if yob not in ssnames['year']:
                ssnames['year'][yob] = 1
            else:
                ssnames ['year'][yob]+= 1

            if record['name'] not in ssnames['fname']:
                ssnames['fname'][record['name']] = 1
            else:
                ssnames ['fname'][record['name']]+= 1

            if record['sex'] not in ssnames['gender']:
                ssnames['gender'][record['sex']] = 1
            else:
                ssnames ['gender'][record['sex']]+= 1

            if record['number'] not in ssnames['count']:
                ssnames['count'][record['number']] = 1
            else:
                ssnames ['count'][record['number']]+= 1
  
        yob += 1

yrcnt = 0        
print('Year : Names with 5 or more people')           
for y in sorted(ssnames['year']):
    yrcnt += 1     
    print(y,":","{:5d}".format( ssnames['year'][y]))
print('Total Years: ',yrcnt )


# In[ ]:





# In[ ]:




