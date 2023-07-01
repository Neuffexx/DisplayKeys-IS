## Now you can see it `move it move it`
A small but functional update, was going to wait a bit longer to add more to the tool before creating another release.
But this felt 'core' enough of a needed functionality that I wanted to get it out there as soon as possible.

> Just a heads up, community reports + some of my own testing, showed that the more gives you .gif files are assigned to as single
> scene/layer of buttons, the slower these .gif files will play.

> Addtionally, I noticed that sometimes the timeings are off between when they start playing.
> This is expected when first assigning it, but should be resolved when you switch to a different scene and back.

### Changes:
- Added Support for .gif files
   - Now when an image or gif is selected it will automatically determine which type it is
   - supported formats are: `.png, .jpg, .jpeg, .bmp, .gif`
      - In comparison to static image files, BaseCamp does not save `.gif` files on the profile.
        Instead, it saved the path to that file. So be warned, do not delete the files after you added them.
- Also added file information to the .exe (description, version, copyright, etc.)
 
