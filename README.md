# IntersectingLines
A program that approximates a given image by drawing straight lines across the screen

It doesn't work quite as well as I would like. a few Optimizations I'm considering are fully implementing the lookup table, and stopping the deviance calculation once it has surpassed the current lowest deviance. That if statement might just slow things down though. Will need to test to find anything conclusive.


Running it yourself
Just copy and paste the file path of any jpg you have into the filename variable (somewhere around line 123)

Also, this might break if you use a different colorspace than I am. However, I'm pretty sure that whatever the default color space is for a jpg is what I use, so I wouldn't stress too much. Beyond that, everything about this has been written and run in VS code using pygame 2.5.2 and a Python debugger. It's not anything too terrible large or complex, so I don't expect many issues.
It definitely runs faster on smaller images.



Additional notes
Originally I was considering having each new line drawn along whichever line in the image had highest deviance. This would allow the developing image to approximate the target in potentially far fewer lines. Instead, the location (but not orientation) of each line is currently randomly selected. In addition, there are currently 32 subdivisions of all possible angle, and I would like to go at least an order of magnitude up. I also considered basing deviation not on the pixels directly affected, but rather on how the average of the pixels changes, using similar algorithms to those used in say, a box blur. Since the image is already blurry, I hypothesize that the blur would be more accurate if it actually worked as a blur and not a 1:1 render.

However, to implement all of these ideas would, I believe, significantly slow down the program, and so they only become viable once much better optimizations are implemented. I have to choose between quantity and quality for all of the lines, and more lines means I get a shabby result after 1 minute, rather than a (maybe) terrific result after 1 hour. Maybe the lookup table would help a lot, but I'm not sure. It's still a draw call on every frame, since I don't know how to batch that. Yeah yeah, I'll learn at some point, but it sounds lower-level than my pay grade.
