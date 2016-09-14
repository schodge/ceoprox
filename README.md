##CEO Proximity Alert Readme

This is the code for the CEO Proximity Alert webcast. Since much of this
code requires credentials, these have been removed from the source files
with comments inserted to put your own credentials in.

Since the original development had credentials in place, this repo is
a new repo, missing the dev history of the files. Some of the files
are a bit outdated at this point, as they were replaced by better ideas.
They are being left in because you may find some of the code useful.

There are three broad categories of code here:

(1) Particle firmware. Designed to work with the particle asset tracker
libs.
(2) Code to interface to SnapLogic. This code is easily adaptable to 
any system where you write and fetch to your database through an 
intermediate REST-ish system.
(3) Flask code and Google Maps heatmap code. There weren't used as much
in dev, and should be considered starting points for further work.

There is also some misc code, for example, the battery plotting scripts.

Pull requests are always welcome, particularly to add the tests missing
from, currently, everything.
