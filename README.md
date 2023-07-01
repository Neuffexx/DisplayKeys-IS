# DisplayKeys-IS

## What is it?
Simply said, a quick workaround tool for splitting images, in a way that lets users customize the spacing between the split image cells, to be used with display key pads.
Dont get me wrong, there are PLENTY of image splitting tools out there hosted on websites even, so you dont have to download anything.
But none of them from what I found actually allow you to adjust anything other than  Rows/Columns.

## Why Make it?
Well I needed a way be able to quickly setup images across different Display Keys.
And although the Mountain Everest addition, the Display Pad, does come with functionallity to make use of the whole screen to display a single image continiously.
It certainly doesnt when you are actually using it, as of the time of writing this (27/6/2023) it only supports this functionality when using a 'lockscreen' image.

## How do you use it?
The only thing anyone probably cares to read on here, so let me make this simple:
- Download / Setup Instructions
	- Download the DisplayKeys-IS_vX.X.X file from the latest of the [Release](https://github.com/Neuffexx/DisplayKeys-IS/releases) page 
	- Extract and Run
		> You may get a warning when first launching it, this is a False Positive, just click 'Run Anyway'.

  		> _If you feel uncomfortable to download the .exe your free to go over the single code file that is the Application to ensure its safe (ProjectFiles/DisplayKeys-IS.py).
    		 Or the action that builds & publishes it (.github/workflows/release.yml)_
- Usage Instructions / Or watch the [Usage Demonstration Video (Placeholder)](http://youtube.com/)
	- Select an Image to split, either by entering the path into the text box or selecing it via the 'Browse' button.
	- Select the Save Location, again, either by entering the path or selecting it
	- (Optionally) Set Image Splitting Options
		- Defaults: Will Split the image in a 2x6 grid, using Spacing horizontally and vertically by 40pixels
		- User Defined: Will let you manually enter the amount of Rows/Columns, and both Horizontal and Vertical Spacing.
	- Click the 'Split Image' button.
	- In the Base Camp software, when assigning images to your DisplayKeys, find wanted images in the provided Save Location

## Whats Next?
Well I plan to add/improve on the following
- Create GIF support
- Clean Up UI
- Improve Image Splitting Logic
- Saving/Loading presets (in case you find combos that work for you)
- Automate Profile Assignment ! Base Camp Only ! (Need to look into how)
- Create UI Representation of how the image will be cut/cropped

## How does it work?
Oh wow someone actually reads this?

Quite simple honestly.
The whole thing is built on Python, making the job quite easy with the plethra of libraries out there that make your life easier.
And that means something since I never really used python before this.

The app can be split into 2 parts:
- The Graphical User Interface (GUI)
- The Image Splitting Logic

### The GUI
By far the hardest part about this project, for me at least, as I had never done anything like this before.
Its completely built using the [TkInter Library](https://wiki.python.org/moin/TkInter).

The interface is composed of three things in the following structure: 
- The Window
  - A Grid (composed of a single column)
    - Widgets (Of custom widget class: EntryWithLabel)

(I might accidentally refere to widget as entries at soem point due to my own lack of knowledge when making this)

When the Window/GUI is first created it takes as a argument an array of widgets, that is then used to populate populate the grid column.
This then continiously runs on a `mainloop()` function that constantly updates the UI allowing for changes as the user interacts with the application.



### Image Splitting Logic
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

So I went about it by seperately setting up the cropping for cells that I seperate into 'Outliers' (Orange) and 'Core' (Purple) cells.
The logic can be summed up to this:
- Determine which image cells are outlier cells or core cells
- If its an outlier cell, check the longest_dimension to determine whether to crop away only at the sides or top/bottom. But only the one that is facing outwards.
- If its a core cell, check the longest_dimension to determine whether to crop away only at the sides or top/bottom. But either 'both sides' or 'both bottom and top'.

(This image is divided by an extra row / column for demonstration purposes)
![Image showing a 3x8 cell division, highlighting both the outlier and core cells](https://i.imgur.com/zcCL5YL.jpg)

- For the Outlier's: I simply make sure to crop from the outside inwards if the Image-Cell proportions allow it (relative to the original image).
  If it doesnt, then it will choose the Single-Outer Side of the larger dimension, to crop from there.
![Image showing a 3x8 cell division, showing the direction of cropping for outlier cells](https://i.imgur.com/lsvQmNl.png)

- For the Core's: on the other hand dont have the benefit of this type of cropping.
  Instead, it crops from both sides of the largest dimension equal amounts of rows of pixels.
![Image showing a 3x8 cell division, showing the direction of cropping for core cells](https://i.imgur.com/yOKNQKl.png)

