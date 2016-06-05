SPPicture v1
This program allows the user to select an image and display it in a floating box on top of 
	other programs on the computer.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dependencies:	Python3, PIL(Pillow), Tkinter.
Use:
	The viewer allows dragging, and zooming (ctrl+plus/minus or ctrl+scroll) of the image.
	Also there are three buttons, from left to right:
		Full 	-> Shows/Hides the menu buttons and border from the program.
		Img	-> User selection of the image to view.
		Top	-> Switches between having the program always on top or not.
	An image can be selected as a parameter for the program.
	Resizing the window resets the image zoom.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This program has all of the functionality that I wanted, so the project is close to complete.
It needs some major refactoring, considering I expected it to be less than a hundred or two lines,
 I decided to leave it in one file.
If I refactor:
	Split the program into some sort of class based system.
	Throw the global variables into a dictionary, or some system, because this is just silly.
	Clean up event handlers.


For a weekend project, this was a great learning experience.
