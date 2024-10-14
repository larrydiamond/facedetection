Hi William!

I had this working a while ago and havent followed up sadly.

It uses OpenCV2 to do face detection from my PC with a USB camera and will announce the name of the person

I created a labeleddirectory that I passed in that has a number of files in it 

Larry_Diamond.jpg
George_Washington.jpg

etc etc etc

and then I got it to the point that the camera would announce the person who was there
line 101 speech_engine.say("We have detected " + name)

it loads known images on line 63

and saves the face on line 87

it runs in a loop (its python so I dont know I can say a tight loop)

I wanted to move this to a pi zero 2 w or a pico 2 with a cheapo camera

but once there's an image file on line 87, you could attempt to locally see if there's a package in the image.

opencv has some good free classes and that's how I got this far

https://opencv.org/university/free-courses/

I think I took the opencv bootcamp
