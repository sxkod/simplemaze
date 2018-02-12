#! /usr/bin/env python

import Tkinter as tk
from tkFileDialog import askopenfilename as askop
from tkFileDialog import asksaveasfilename as asksv
import math

ditem={
	'x1':None,
	'y1':None,
	'x2':None,
	'y2':None,
	'mode': None,
	'col': None
}

lastpos=[None,None]
lines=[]
dlines=[]
ditems=[]
dobjects=[]

cnvw=600
cnvh=600
gridsize=20
snapsize=5.0
modes={1:"Line",2:"Circ",3:"Rect"}
colors={1:"white",2:"black",3:"red",4:"blue",5:"green",6:"yellow"}

root=tk.Tk()
modeval=tk.IntVar(root)
colval=tk.IntVar(root)
modeval.set(1)
colval.set(2)
root.title("Maze Drawing Tool")


def redraw(event):
	global ditems,dobjects,cnv
	if len(ditems)<1:return
	ditemsloc=[]
	for n in ditems:
		ditemsloc.append(n)
	clear(1)
	for n in ditemsloc:
		if n['mode']=='Line':
			dobj=cnv.create_line(n['x1'],n['y1'],n['x2'],n['y2'],width=3,fill=n['col'])
		elif n['mode']=='Circ':
			dobj=cnv.create_oval(n['x1'],n['y1'],n['x2'],n['y2'],width=3,fill=n['col'])
		elif n['mode']=='Rect':
			dobj=cnv.create_rectangle(n['x1'],n['y1'],n['x2'],n['y2'],width=3,fill=n['col'])
		dobjects.append(dobj)
		ditems.append(n)

def clear(event):
	global cnv,ditems,dobjects
	if len(dobjects)<1:return
	for n in dobjects:
		cnv.delete(n)
	dobjects=[]
	ditems=[]

def drawgrid():
	global cnv,cnvh,cnvw
	segw=cnvw/gridsize
	segh=cnvh/gridsize
	for n in range(segh):
		cnv.create_line(0,n*gridsize,cnvw,n*gridsize,fill='blue')
	for n in range(segw):
		cnv.create_line(n*gridsize,0,n*gridsize,cnvh,fill='blue')

def doundo(event):
	global cnv,dobjects,ditems
	if len(dobjects)<=0:return
	last=dobjects[-1]
	dobjects=dobjects[0:-1]
	ditems=ditems[0:-1]
	cnv.delete(last)

	
def clicked(event):
	global lastpos,ditems,colval,modeval,colors,modes,ditem,dobjects
	xnow=event.x
	ynow=event.y
	if lastpos[0]==None:
		lastpos=[xnow,ynow]
	else:
		ditmp=ditem.copy()
		ditmp['x1'],ditmp['y1'],ditmp['x2'],ditmp['y2'],ditmp['mode'],ditmp['col']=lastpos[0],lastpos[1],xnow,ynow,modes[modeval.get()],colors[colval.get()]
		ditems.append(ditmp)
		ditmp=None
		if modes[modeval.get()]=='Line':
			dobj=cnv.create_line(lastpos[0],lastpos[1],xnow,ynow,width=3,fill=colors[colval.get()])
		elif modes[modeval.get()]=='Circ':
			dobj=cnv.create_oval(lastpos[0],lastpos[1],xnow,ynow,width=3,fill=colors[colval.get()])
		elif modes[modeval.get()]=='Rect':
			dobj=cnv.create_rectangle(lastpos[0],lastpos[1],xnow,ynow,width=3,fill=colors[colval.get()])
		lastpos=[None,None]
		dobjects.append(dobj)

def quitit(event):
	raise SystemExit

def roundup(x):
	global snapsize
	return int(math.ceil(x / snapsize))*int(snapsize)
    
def saveit(event):
	global dobjects,ditems,cnvw,cnvh
	fname=asksv()
	txt='$W=='+str(cnvw)+'\n'+'$H=='+str(cnvh)+'\n$BEG\n'
	for n in ditems:
		txt+=n['mode']+'::'+n['col']+'::'+str(n['x1'])+','+str(n['y1'])+','+str(n['x2'])+','+str(n['y2'])+'\n'
	txt+='$END'
	fx=open(fname,'w')
	fx.write(txt)
	fx.close()

def loadit(event):
	global dobjects,ditems,cnvw,cnvh,ditem
	fname=askop()
	if not fname:return
	if len(fname.strip())<1:return
	f=open(fname)
	txt=f.read()
	if txt.find('$BEG')<=0 or txt.find('$END')<=0:return
	f.close()
	txt=txt.replace('$END','')
	txt=txt.split('$BEG')	
	if len(txt)<2:
		print("Not enough data!",len(txt))
		return
	txt=txt[1]
	#now finally we have one object per line TYPE:COLOR:2 x/y coords
	for n in txt.split('\n'):
		if len(n.strip())<=0:continue
		tmpmod,tmpcol,coords=n.split('::')
		tx=coords.split(',')
		ditmp=ditem.copy()
		ditmp['x1'],ditmp['y1'],ditmp['x2'],ditmp['y2'],ditmp['mode'],ditmp['col']=tx[0],tx[1],tx[2],tx[3],tmpmod,tmpcol
		ditems.append(ditmp)
		ditmp=None
	redraw(1)

cnv=tk.Canvas(root,width=cnvw,height=cnvh,relief="raised")

bsave=tk.Button(root,text="Save",fg="green")
bquit=tk.Button(root,text="Quit",fg="red")
bundo=tk.Button(root,text="Undo",fg="blue")
bredr=tk.Button(root,text="Redraw",fg="blue")
bclr=tk.Button(root,text="Clear",fg="red")
bload=tk.Button(root,text="Load",fg="blue")

rframe=tk.Frame(root,relief='sunken')

tmp=modes.keys()
tmp.sort()
for n in tmp:
	tk.Radiobutton(rframe,text=modes[n],variable=modeval,value=n,indicatoron=0).pack()

tk.Frame(rframe,height=10,relief='groove').pack()

tmp=colors.keys()
tmp.sort()
for n in tmp:
	tk.Radiobutton(rframe,text=colors[n],variable=colval,value=n,indicatoron=0).pack()
	

rframe.grid(row=0,column=0,sticky="W")
cnv.grid(row=0,column=1,columnspan=6,sticky="NW")
bsave.grid(row=1,column=0,sticky="S")
bundo.grid(row=1,column=1,sticky="S")
bredr.grid(row=1,column=2,sticky="S")
bclr.grid(row=1,column=3,sticky="S")
bload.grid(row=1,column=4,sticky="S")
bquit.grid(row=1,column=5,sticky="S")

cnv.bind('<Button-1>',clicked)
bundo.bind('<Button-1>',doundo)
bredr.bind('<Button-1>',redraw)
bclr.bind('<Button-1>',clear)
bsave.bind('<Button-1>',saveit)
bload.bind('<Button-1>',loadit)
bquit.bind('<Button-1>',quitit)

drawgrid()
root.mainloop()
