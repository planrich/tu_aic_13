# -*- coding: latin-1 -*-

# import the MobileWorks library
import mobileworks as mw
import settings


# set username and pw
mw.username = settings.mobileWorks_Username
mw.password = settings.mobileWorks_Password
# use sandbox
mw.sandbox()

# create the project object 
p = mw.Project(instructions="Is Apple mentioned in this paragraph positiv, neutral or negative") 
# we can also add more parameters 
p.set_params(resourcetype="t", redundancy="3")
# this will add a field called 'Name' of type 't' (text) 
p.add_field('Rating', 'm', choices="positive, neutral, negative")
# add task to projekt 
p.add_task(mw.Task(resource="Yet, as today’s rollout of a new set of iPads demonstrates, that may just be Apple’s core problem. It’s the HBO of tech companies. It’s a highly profitable, premium brand that got started in the 1970s, and that industry peers envy and love. But while highly profitable, it always has to cope with cheaper, aggressive competitors. (Netflix announced Monday that it had surpassed the premium cable network in subscribers)."))
p.add_task(mw.Task(resource="Well, Apple is now a purveyor of expensive, high-end products in a market where consumers are turning to cheaper alternatives."))
p.add_task(mw.Task(resource="In the past year, Apple’s dominance in the tablet market has crumbled. As Henry Blodget noted at Business Insider, in a market that’s exploding, iPad’s sales dropped 14 percent in the last quarter compared to the year prior. Apple has gone from controlling 71 percent of the tablet market in the beginning of 2012, to holding down just 28 percent by the end of the most recent quarter. In that time frame, more competitively priced competitors like Samsung and Microsoft have made significant gains."))
#p.set_params(webhooks="www.google.at")
#post projekt to mobile works
p.post()

# create a task object 
#t = mw.Task(instructions="What is the name on this business card?") 
# set some parameters 
#t.set_params(resource="http://www.mobileworks.com/images/samplecard.jpg") 
# add the required fields 
#t.add_field("Name", "t") 
# finally, post it and get the url of the newly created task 
#task_url = t.post()
#print(task_url)

print("..projekt posted..")
