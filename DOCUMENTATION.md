# Welcome to the DisplayKeys-IS Documentation!
> Here I will simply be documenting, for myself and others how the I have made this little tool, so that its a bit easier to work with in case something is unclear.  
> Trust me I made this, but even I come back after a 2 days break and already forgot what I did, so I also constantly check this page all the time.

<pre>



                            This page is currently a WIP as a lot is being remade!

  
  
</pre>

## How does the Application work?


Quite simple honestly.
The whole thing is built on Python, making the job quite easy with the plethra of libraries out there that make your life easier.
And that means something since I never really used python before this.

The app can be split into 2 parts:
- The Graphical User Interface (GUI)
- The Image Splitting Logic

## The GUI (`SECTION NEEDS UPDATING`)
By far the hardest part about this project, for me at least, as I had never done anything like this before.
Its completely built using the [TkInter Library](https://wiki.python.org/moin/TkInter).

The interface is composed of three things in the following structure: 
- The Window
  - Frame A
    - List of Widgets (Custom widget class: DisplayKeys_Widget)
  - Frame B
    - Preview Widget (Custom widget Class: DisplayKeys_Previewer)

When the Window/GUI is first created it takes as a argument an array of widgets, that is then used to populate populate the grid column.
This then continiously runs on a `mainloop()` function that constantly updates the UI allowing for changes as the user interacts with the application.



## Image Splitting Logic (`SECTION NEEDS UPDATING`)
This took some playing around with. But was also relatively easy to implement, as it was completely built on the functionality of the [PIL - Image Library](https://wiki.python.org/moin/PythonImagingLibrary).

Although you think its pretty straight forward (as did I), you simply get the  rows and colums to slice the image(s) by and factor in the gap value for where to make the split.
However, unfortunately I noticed an issue with this approach. Whenever I used an image that was for example an image was non-square in format it will cause squishing.
This is really incosistent, but it happened to me a lot, so I decided to do something about it since software 'should' crop it anyways if the image is not in a square format.

So I had to essentially make sure that whatever the image gets split to, will need to be cropped to be in a square format. 
Otherwise it just makes life misserable for anyone using it.

The base rule for any sort of cropping is comparing the split cells X/Y dimensions and seeing which one is greater.
This is because if you split an image by lets say 2 rows and 6 columns (as is the Mountain DisplayPad layout), you will inevitably get image cells that are taller than they are wide.
So by checking which dimension is the largest in length, I can determine the sides of the image to cut.
![Image showing the default cell division of a user provided image](https://i.imgur.com/6SoscLS.png)


But I cant just cut away at any and all sides of each image cell that I want to, even if its in the right dimension, I need to somehow determine whether to crop for example the top or bottom of a tall image.
Otherwise it will defeat the point of making it square since it will simply ruin the images.

And although I could statically say, if at Top row then crop at top of image, and if at Bottom row crop at bottom of image.
This approach falls appart the moment more than 2 rows are used. *Of course also if less than 2 rows, but the inital implementation of this tool was `not` made with handeling such situations in mind.
As for example, someone may need to add a third row in the splitting process, due to the subject of the image that the user wants to see potentionally only being in the top or bottom 2/3rds of the image.

So I went about it by seperately setting up the cropping for cells that I seperate into `Outliers` (Orange) and `Core` (Purple) cells.
The logic can be summed up to this:
- Determine which image cells are outlier cells or core cells
- If its an outlier cell, check the longest_dimension to determine whether to crop away only at the sides or top/bottom. But only the one that is facing outwards.
- If its a core cell, check the longest_dimension to determine whether to crop away only at the sides or top/bottom. But either 'both sides' or 'both bottom and top'.

(This image is divided by an extra row / column for demonstration purposes)
![Image showing a 3x8 cell division, highlighting both the outlier and core cells](https://i.imgur.com/zcCL5YL.jpg)  
`Orange = Outlier Cells  |  Purple = Core Cells`

- For the Outlier's: I simply make sure to crop from the outside inwards if the Image-Cell proportions allow it (relative to the original image).
![Image showing a 3x8 cell division, showing the direction of cropping for outlier cells](https://i.imgur.com/lsvQmNl.png)

- The Core's: on the other hand dont have the benefit of this type of cropping.
  Instead, it crops from both sides of the largest dimension equal amounts of rows of pixels.
![Image showing a 3x8 cell division, showing the direction of cropping for core cells](https://i.imgur.com/yOKNQKl.png)

## How to make an actual Application out of the Code?
Short answer: I dont know.  
The best and easiest way for me was to use [PyInstaller](https://pyinstaller.org/en/stable/#), that takes my code file along with anything I want packaged based on some parameters and creates an `.exe` file for me.  
As someone once said:   
> _You dont have to know how a tool works to use it._

Dont remember who said it, but im sure someone did...


On GitHub at the very least I use `GitHub Actions` to simplify the process of packaging the code into an application.  
It can run it in a fresh new and clean environment without any of my dumb interfierance, run the PyInstaller command and upload the successful result to the repository.  
And hey, if something doesnt work it has a detailed console of log text of pretty much every step it takes making it quite easy to debug, even shows you errors causes by your own code.
Although learning `Actions` was a bit annoying at the beginning, I would say its worthwhile.
