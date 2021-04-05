import random
import time

def eight_ball():
  random.seed(time.time())
  answers = random.randint(1,7)
  if answers == 1:
      return "It is certain"
    
  elif answers == 2:
      return "Outlook good"
    
  elif answers == 3:
      return "You may rely on it"
    
  elif answers == 4:
      return "Ask again later"
    
  elif answers == 5:
      return "Reply hazy, try again"
    
  elif answers == 6:
      return "I don't think so"
    
  elif answers == 7:
      return "My sources say no"

def why_ball():
  random.seed(time.time())
  answers = random.randint(1,8)
  if answers == 1:
      return "Who knows"
    
  elif answers == 2:
      return "Maybe you can ask them"
    
  elif answers == 3:
      return "Because they are special"
    
  elif answers == 4:
      return "Because you are a boulder, and I am a mountain"
    
  elif answers == 5:
      return "Because the ting goes skrraaa"
    
  elif answers == 6:
      return "Because they are amazing"
    
  elif answers == 7:
      return "Because of you"
    
  elif answers == 8:
      return "My sources say I disagree"

def who_ball():
  random.seed(time.time())
  answers = random.randint(1,8)
  if answers == 1:
      return "A good friend of mine"
    
  elif answers == 2:
      return "A person"
    
  elif answers == 3:
      return "Not you"
    
  elif answers == 4:
      return "A very special individual who has a lot to see in their future"
    
  elif answers == 5:
      return "Food--uhImean a very loving person I will chew--ish.. cherish I mean"
    
  elif answers == 6:
      return "Amazing"
    
  elif answers == 7:
      return "The best person I cannot calculate to be any better"
    
  elif answers == 8:
      return "Not bad, but not good either... Average"

def what_ball():
  random.seed(time.time())
  answers = random.randint(1,3)
  if answers == 1:
      return "Who knows"
    
  elif answers == 2:
      return "Maybe you can ask them"

  elif answers == 2:
      return "Is it a good thing?"