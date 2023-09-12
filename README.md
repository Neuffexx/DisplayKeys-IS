# DisplayKeys-IS

## What is it?
Simply said, a quick workaround tool for splitting images, in a way that lets users customize the spacing between the split image cells, to be used with display key pads.  
_Should work for any Display Pad, as it currently doesnt interface with any of them directly._

## Why Make it?
Well I needed a way be able to quickly setup images across different Display Keys.  
Dont get me wrong, there are PLENTY of image splitting tools out there hosted on websites even, so you dont have to download anything.  
But none of them from what I found actually allow you to adjust anything other than  Rows/Columns.  

And although the Mountain Everest addition, the Display Pad, does come with functionallity to make use of the whole screen to display a single image continiously.  
It certainly doesnt when you are actually using it, as of the time of writing this (27/6/2023) it only supports this functionality when using a 'lockscreen' image.

## How do you use it?
The only thing anyone probably cares to read on here, so let me make this simple:
- Download / Setup Instructions
	- Download the DisplayKeys-IS_vX.X.X file, from the latest of the [Release](https://github.com/Neuffexx/DisplayKeys-IS/releases) page 
	- Run
		> You may get a warning when first launching it, just click 'Run Anyway'.

  		> _If you feel uncomfortable to download the .exe your free to go over the single code file that is the Application to ensure its safe (ProjectFiles/DisplayKeys-IS.py).  
  		  Or the action that builds & publishes it (.github/workflows/release.yml)_
- Usage Instructions (Or watch the [Usage Demonstration Video](https://youtu.be/D6juk_5pe5Q))
	- Select an Image to split, by selecting it via a 'Browse' button or Drag and Drop it onto the Text Field.
	- Select the Save Location, in either of the same two methods. (Default save location if none is entered: _Desktop_)
	- (Optionally) Set Image Splitting Parameters
		- `Presets:` Will Split the image in a pre-saved combo of variables
          - There you will find a Dropdown with the currently existing Presets to select from
            - Initially will automatically select a 'Default' profile, with a 2x6 grid, using Spacing of **_40 (pixels)_**.
            - Can `add` / `edit` / `delete` presets with the buttons found beneath the Dropdown
            - To Import/Export Presets, go to `(Menu Bar) File>Presets`
		- `User Defined:` Will let you manually enter the amount of Rows/Columns, and the Spacing between Image-Cells.
	- Click the `Split Image` button.
  		- Settings will use defaults for any input not given.
	- Just assign them in your Display Keypad's Provided software.  
	  And you're done :D

## Whats Next?
Well I plan to add/improve on the following (in no particular order):
- Clean Up UI
  - +Make Preview more accurate to final result
- Improve Image Splitting Logic
- Automate Image Assignment to Profiles ! BaseCamp Software ! (Need to look into how)
- Add GIF support, for the Previewer  
  (Splitting functionality already supports it)

<pre>






	

</pre>

# Extra Stuff
## Examples
All Example Images that I used for testing can be found [here(placeholder)]().
> (Includes the original's used along with the split version I found work best for me, for demonstration/experimentation purposes)
## Documentation
Check out the [Documentation](https://github.com/Neuffexx/DisplayKeys-IS/blob/Development/DOCUMENTATION.md) if you want to contribute or simply want to know how stuff works!
