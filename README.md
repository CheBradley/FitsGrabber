# FitsGrabber
FitsGrabber is a script that will automatically download 1" cutouts from the FIRST or Stripe 82 catalogs, whichever is specified by the user. You will need to have selenium installed. The size of the cutouts can be changed with Imagesize.send_keys('newsize'). Also, the default location for the downloaded images will be the downloads folder, but the user has to option to place the images somewhere else.
The code will find the Ra and Dec values (or convert them if the file is in decimal format), as long as they are in one of these 4 formats:

- 01 49 31.740 +01 24 03.60 

- 01:49:31.740 +01:24:03.60 

- J204626.10+002337.6 

- 9.9610137  0.0874534 (decimal, separated by a tab) 

The second and third formats can also have other information on the line, the code will only read the Ra and Dec values.
If the Ra and Dec values are not found within the region, they will be removed and added to a list of values not found. In addition to the images, there will be three other text files produced. One has the values that were found, another has the values that were not found, and the last is just a formatted version of the original list.
