# DisplayKeys-IS

## What is it?
Simply said, a quick workaround tool for splitting images, in a way that lets users customize the spacing between the split image cells, to be used with display key pads.  
_Should work for any Display Pad, as it currently doesnt interface with any of them directly._

## Why Make it?
Well I needed a way be able to quickly setup images across different Display Keys.  
Dont get me wrong, there are PLENTY of image splitting tools out there hosted on websites even, so you dont have to download anything.  
But none of them from what I found actually allow you to adjust anything other than  Rows/Columns.

## How do you use it?
The only thing anyone probably cares to read on here, so let me make this simple:
- **Download / Setup Instructions**
	- Download the DisplayKeys-IS_vX.X.X file, from the latest of the [Release page](https://github.com/Neuffexx/DisplayKeys-IS/releases)
	- Run
		> You may get a warning when first launching it, just click 'Run Anyway'.

  		> _If you feel uncomfortable to download the .exe your free to go over the single code file that is the Application to ensure its safe (ProjectFiles/DisplayKeys-IS.py).  
  		  Or the action that builds & publishes it (.github/workflows/release.yml)_
- **Usage Instructions (Or watch the [Usage Demonstration Video | v0.3.0](https://youtu.be/D6juk_5pe5Q))**
	- Select an Image to split  
	('Browse' button / Drag and Drop)
	- Select the Save Location  
	(Default save location if none is entered: _Desktop_)
	- (Optionally) Set Image Splitting Parameters
		- `Presets:` Will Split the image in a pre-saved combo of variables
          - Dropdown with the currently existing Presets
            - Automatically 'Default' profile selected. (2x6 grid, Spacing **_40 (pixels)_**)
            - `add` / `edit` / `delete` preset buttons beneath the Dropdown
            - To Import/Export Presets, go to `(Menu Bar) File>Presets`
		- `User Defined:` Will let you manually input the Parameters for Splitting Image-Cells.
	- Click the `Split Image` button.
  		- Settings will use defaults for any input not given.
	- Just assign in your Display Keypad's software.  
	  _And you're done :D_

## Whats Next?
Well I plan to add/improve on the following (in no particular order):
- Clean Up UI
  - +Make Preview more accurate to final result
  - Pop-up Windows need polish
  - Visualize what is Drag n Drop interactible when dragging into the window
- Improve Image Splitting Logic
  - Add Percentage option to Gap input  
    _(Will allow for aspect ratio Presets, not bound to image resolution)_
- Automate Image Assignment to Profiles
  - ! BaseCamp Software ! SDK has been released, looking into it
- Previewer
  - Add GIF support, for the Previewer  
    _(Splitting functionality already supports it)_
  - Add Different Previewing Modes

<pre>






	

</pre>

# Extra Stuff
## Examples
All Example Images that I used for testing can be found [here(placeholder)]().
> (Includes the original's used along with the split version I found work best for me, for demonstration/experimentation purposes)
## Documentation
Check out the [Documentation (WIP)](https://github.com/Neuffexx/DisplayKeys-IS/blob/Development/DOCUMENTATION.md) if you want to contribute or simply want to know how stuff works!
