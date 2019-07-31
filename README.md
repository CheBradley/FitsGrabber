# FitsGrabber
FitsGrabber is a script that will automatically download 1" cutouts from the FIRST or Stripe 82 catalogs, whichever is specified by the user. The size of the cutouts can be changed, 1" is the default. Also, the default location for the downloaded images will be the downloads folder, but the user has to option to place the images somewhere else.
The code will find the Ra and Dec values (or convert them if the file is in decimal format), as long as they are in one of these 4 formats:

01 49 31.740 +01 24 03.60 

01:49:31.740 +01:24:03.60 

J204626.10+002337.6 

9.9610137   0.0874534 (decimal, separated by a tab) 

The second and third formats can also have other information on the line, the code will only read the Ra and Dec values.
