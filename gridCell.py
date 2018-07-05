#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#
# Author: Peter Schüller (2014)
# Adapted from a script posted by Adam Marshall Smith on the potassco mailing list (2014)
#

import sys
import re
import json
import subprocess
import collections
import traceback

def extractExtensions(answerset):
  #print(repr(answer_set))
  field_pattern = re.compile(r'(\w+)\((\d+)\)') #for row and column atoms 
  tuple_pattern = re.compile(r'(\w+)\((.*,.*)\)') #the other atoms
  extensions = collections.defaultdict(lambda: set())
  for l in answerset:
    try:
      args = field_pattern.match(l).groups()
      #print "for {} got field pattern match {}".format(l, repr(args))
      # first arg = predicate
      # second/third arg = coordinates
      # rest is taken as string if not None but " are stripped
      head = args[0]
      rest = int(args[1])
      extensions[head].add(rest)
      if args[3]:
        rest.append(str(args[3]).strip('"'))
      #sys.stderr.write(
      #  "got head {} and rest {}\n".format(repr(head), repr(rest))
    except:
      #sys.stderr.write("exception ignored: "+traceback.format_exc())
      pass
  for l in answerset:
      try:
        args = tuple_pattern.match(l).groups()
        #print "for {} got field pattern match {}".format(l, repr(args))
        # first arg = predicate
        # second/third arg = coordinates
        # rest is taken as string if not None but " are stripped
        head = args[0]
        rest = args[1]
        extensions[head].add(rest)
        if args[3]:
          rest.append(str(args[3]).strip('"'))
        #sys.stderr.write(
        #  "got head {} and rest {}\n".format(repr(head), repr(rest))
      except:
        #sys.stderr.write("exception ignored: "+traceback.format_exc())
        pass
  #print(extensions)
  return extensions

import tkinter as tk

class Window:

  def __init__(self,answersets,selected):
    self.answersets = answersets
    self.selections = list(range(0,len(self.answersets)))
    self.selected = selected
    #print(self.selected)
    self.root = tk.Tk()
    self.main = tk.Frame(self.root,width=5000,height=1000)
    self.main.pack(fill=tk.BOTH, expand=False)
    

    self.canvas1 = tk.Canvas(self.main, bg="white",width=1000,height=100,border=1, relief="sunken", scrollregion=(0,0,3000,3000))
   
    self.hbar=tk.Scrollbar(self.main,orient=tk.HORIZONTAL)
    self.hbar.pack(side=tk.BOTTOM,fill=tk.X)
    self.hbar.config(command=self.canvas1.xview)
    

    self.canvas1.config(width=300,height=300)
    self.canvas1.config(xscrollcommand=self.hbar.set)
    self.canvas1.pack(side=tk.LEFT,fill=tk.BOTH)
    self.canvas1.pack(expand=False, side=tk.TOP)
  
    self.selector = tk.Scale(self.main, orient=tk.HORIZONTAL, showvalue=0, command=self.select)
    self.selector.pack(side=tk.BOTTOM,fill=tk.X)
    self.root.bind("<Right>", lambda x:self.go(+1))
    self.root.bind("<Left>", lambda x:self.go(-1))
    self.root.bind("q", exit) # TODO more graceful quitting
    self.items = []
    self.updateView()

  def select(self,which):
    self.selected = int(which)
    self.updateView()

  def go(self,direction):
    self.selected = (self.selected + direction) % len(self.answersets)
    self.updateView()

  def updateView(self):
    self.selector.config(from_=0, to=len(self.answersets)-1)

    SIZE=30
    FIELD_FILL='#b7b7b7'
    WALL_FILL='#444'
    MARK_FILL='#A77'
    TEXT_FILL='#000'
    ROBOT_FILL='#ffc0cb'
    TARGET_FILL='#ccccff'

    def fieldRect(x,y,offset=SIZE):
      x, y = int(x)+1, int(y)+1
      return (x*SIZE-offset/2, y*SIZE-offset/2, x*SIZE+offset/2, y*SIZE+offset/2)

    # delete old items
    for i in self.items:
      self.canvas1.delete(i)
    # create new items
    self.items = []

    ext = extractExtensions(self.answersets[self.selected])
    #print repr(ext)
    maxx = max([x for x in ext['row']])
    maxy = max([y for y in ext['column']])

    self.root.geometry("{}x{}+0+0".format((maxx+7)*SIZE, (maxy+6)*SIZE)) #the window size, increasing 7 will make larger window

    count=0
    for i in range(0,int(maxT)+1):
      for x in ext['row']:
          for y in ext['column']:
              self.items.append( self.canvas1.create_rectangle( * fieldRect(y+count,x), fill=FIELD_FILL))   
      count+=5          

    #sorting obstacles
    tmp1=sorted(list(ext['obstacleAt']), key=lambda x: int(x[-1]))
    count=-5
    prev=None 
    for a in tmp1:
      x=a.split(',')
      if x[2]!=prev:
	      count=count+5
	      self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+count,int(x[0])), fill=WALL_FILL))   
      else:
        self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+count,int(x[0])), fill=WALL_FILL)) 
      prev=x[2]


    #sorting target 
    tmp2=sorted(list(ext['target']), key=lambda x: int(x[-1]))
    count=0
    print(tmp2)
    for a in tmp2:
      #print (a)
      x=a.split(',')
      

      if x[-2]=='east':
      	visits=count
      	for i in range(0,len(tmp2)-int(count/5)):
          for j in range(1,int(x[3])-int(x[1])):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+j+visits,int(x[0])), fill='#FFF'))
          if ((visits+5)/5!=int(maxT)+1):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+visits+5,int(x[0])), fill='#FFF'))
          visits=visits+5

      if x[-2]=='west': 
        visits=count
        for i in range(0,len(tmp2)-int(count/5)):
          for j in range(1,int(x[1])-int(x[3])):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])-j+visits,int(x[0])), fill='#FFF'))
          if ((visits+5)/5!=int(maxT)+1):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+visits+5,int(x[0])), fill='#FFF'))
          visits=visits+5
      if x[-2]=='south':
        visits=count
        for i in range(0,len(tmp2)-int(count/5)):
          for j in range(1,int(x[2])-int(x[0])):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+visits,int(x[0])+j), fill='#FFF'))
          if ((visits+5)/5!=int(maxT)+1):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+visits+5,int(x[0])), fill='#FFF'))
          visits=visits+5
      if x[-2]=='north':
        visits=count
        for i in range(0,len(tmp2)-int(count/5)):
          for j in range(1,int(x[0])-int(x[2])):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+visits,int(x[0])-j), fill='#FFF'))
          if ((visits+5)/5!=int(maxT)+1):
            self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+visits+5,int(x[0])), fill='#FFF'))
          visits=visits+5
      self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[3])+count,int(x[2])), fill='#FFF'))
      self.items.append( self.canvas1.create_oval( * fieldRect(int(x[3])+count,int(x[2]),20), fill=TARGET_FILL))

      count=count+5

    #sorting robot 
    tmp=sorted(list(ext['robotAt']), key=lambda x: int(x[-1]))
    count=0
    for a in tmp:
      x=a.split(',')
      self.items.append( self.canvas1.create_rectangle( * fieldRect(int(x[1])+count,int(x[0])), fill=ROBOT_FILL))
      count=count+5   

    arr=[]

    i=0
    for x in tmp:
      arr.insert(i,"RobotAt: "+ x)  
      i+=1
    #print (arr)
    #print (tmp1)
    

    flag=False
    for y in tmp1:
      flag=False
      for i in range(0,len(arr)):
        if arr[i][-1]==y[-1]:
          arr[i]+="\nObstacleAt: "+y
          flag=True
      if flag==False:
        arr.append("ObstacleAt: "+ y)
    #print(len(arr))   

    #flag=False
    #print(tmp2)
    count=0
    for z in tmp2:
      flag=False
      for i in range(0,len(arr)):
        if arr[i][-1]==z[-1]:
          arr[i]+="\nTargetAt: "+z
          count=i
          flag=True
      if flag==False:
        arr.append("TargetAt: "+z)
    #print(arr)

    x_cor=90
    y_cor=200
    for j in range(0,len(arr)):
      self.canvas1.create_text((x_cor,y_cor),font=("Purisa", 12), text=arr[j])
      x_cor+=145
      
def display_tk(answersets,selected):
  w = Window(answersets,selected)

maxT=None
if len(sys.argv)>3:
  maxT=sys.argv[-1]
else:
  maxT=2
#print (maxT) 

MAXANS=100
clingo = subprocess.Popen(
  "clingo --outf=2 -c time={} {} 0".format(maxT,' '.join(sys.argv[1:3])),
  shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
clingoout, clingoerr = clingo.communicate()
del clingo
#print (clingoout)
clingoout = json.loads(clingoout.decode('utf-8'))
#print(repr(clingoout))
#print(repr(clingoout['Call'][0]['Witnesses']))
#print(repr(clingoout['Call'][0]['Witnesses'][0]['Value']))
#print(repr(clingoout['Call'][0]['Witnesses'][1]['Value']))
witnesses = clingoout['Call'][0]['Witnesses']
#print (witnesses)
#print(len(witnesses))
#import random
#render_svg(random.choice(witn)['Value'])
for i in range(0,len(witnesses)):
  display_tk([witness['Value'] for witness in witnesses],i)
#print ([witness['Value'] for witness in witnesses])
#display_tk([witness['Value'] for witness in witnesses],0)
tk.mainloop()
