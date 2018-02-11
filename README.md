# simplemaze
Simple python tkinter based drawing program geared towards level design

Needs tkinter, python.

A simple drawing program that lets you draw circle/oval, rectangles and lines with different colours.

It saves files with an extremely simple text encoding. It is designed to be used as a simple level design where you can draw primitives of differing colours. Then you can load the text file in your game engine and instance different game objects at the location of the primitives. Different primitives can be loaded at the site of different shapes and different colours. That is up to you. 

Resultant file format looks like this:

$W=600
$H600
$BEG
Line::black::298,230,374,342
Line::black::142,400,313,417
Circ::black::61,205,150,335
Rect::black::202,124,354,173
Rect::red::127,330,180,365
Circ::red::247,233,346,408
Rect::green::99,48,161,205
Rect::yellow::33,461,180,530
$END


Have fun.
