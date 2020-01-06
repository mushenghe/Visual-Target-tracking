# Visual Target tracking
## Project Description
This project is one of the homework of EE333 Computer Vision course at Northwestern University. This project to implement head tracking based on three different template-matching methods.<br>
I separated this task to two basic tasks:<br>
1. Initialization<br>
I first read the 0001image and manually draw a circle around the girl’s head. I found the center of the
circle by show the image several times and play with the parameters. Store this processed first image as
the old_image.
2. Apply image matching method&search method:<br>
I applied three matching methods and got 3 videos. The application for the three methods are very
similar. I made a fixed search window for all the three methods, the center of circle for the next frame
is the point that satisfied the method inside the search window.<br>
1) SSD: sum of squared difference<br>
I wrote a SSD function that takes the old image, the next image and the center of circle of the old image
, then return the center of circle of the next image. To find the center of circle of the next image, I
searched all the points within the search window and compute the D value, the center I found has the
minimum value of D.<br>
2) CC: cross-correlation<br>
Similar to the implementation of SSD method, I wrote a CC function which finds the coordinate that
holds that maximum C value.<br>
3) NCC: normalized cross-correlation<br>
Similar to the implementation of methods above, the NCC function finds the coordinate that maximize
the N value.<br>
All methods above also draw circle on the colored image and write that image to the video. The image
then become the old image.<br>
Result:<br>
The output video using SSD method turns out to be the best, the circle always follow the head even
though there’s partial occlusion.<br>
