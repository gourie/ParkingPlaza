# README #

## What is this repository for? ##

* Quick summary: Parking Plaza repository for application server
* Version: current TEST release [beta.parking-plaza.com](https://beta.parking-plaza.com) is v1.0.50
* Version: current PROD release [www.parking-plaza.com](https://www.parking-plaza.com) is v1.0.50

### Released Features and User Stories
* US Authentication using Google
* US Authentication using Email
* US Become Owner
* US Add Parking unit
* US OwnerSetSchedule (email notification + /schedule endpoint)
* US Renter FindParking
* US Renter BookParking
* Mobile-friendly for smart phone devices
* User info consultation (my account, my reservations, my parkings)
* Terms of Service page with Privacy Policy as Art12

### Rel1.0 enhancements & fixes ###
* Site content update/alignment done (issue #62)
* User info consultation for my parkings in test (issue #31)
* US FindParking for Event integrated into home screen (issue #81)
* Web application optimised for mobile (issue #54)
* HTTP to HTTPS redirect (typing in parking-plaza.com works in all cases and yield secure connection always)
* AWS PROD instances (EC2, RDS) timezone changed to 'Europe/Brussels'
* AWS TEST Mollie redirect
* AWS TEST Google signup / login fixed (Google API console settings)
* AWS PROD / TEST Google API call fixed (required for GooglePlacesSuggest used in Rent your Parking modal)
* TosApp error when clicking "Rent Your Parking?" button
* Tos checkbox not showing correctly on all devices/browsers (sign up and becomeowner)
* User-agent not properly added to Events table for IndexHandler
* Added favicon (logo in browser tab)
* Rent Your Parking? button on EmailConfirmationPage
* Changed the Email Signup confirmation modal to explain the why behind the confirmation email.
* Modified Add your parking button/modal/emails based on feedback of beta testers
* Owner Add Unit email adapted to commercial conditions defined for pilot start
* Bugfix: Owner Set Schedule API handler contained incorrect UpdateUnitProperties function (unit fulladdress gone after setschedule >> no more address in UI!)
* Bugfix: MyAccount info got corrupted after adding a new parking unit
* Bugfix: entering wrong email address at email sign-up would throw application error >> workaround: changed to add user to DB (with possibly wrong email address)
* Mollie prod & beta key added
* Invoice layout changed to conform with BTW law (Art 9 KB 19)
* Every user can see the available events, only logged in user can be find and book parking
* Bugfix in FindParkingModal: if no capacity is available, the text explains this instead of showing modal with empty fields for parking, etc
* Enhancement to Owner Set schedule email + schedule page to explain better how it works (unit address, event description + date, ...)
* Enhancement: added sitemap.txt for Google SEO
* Unit friendlyname depreciated from Schedule page and MyParkings modal
* Enhancement Schedule page: alert if user not logged in
* Bugfix: Login via email & logout doesn't change loggedIn to correct state which causes UI not to update accordingly > fixed in Home, Schedule, Tos, Emailconf page
* Bugfix: schedule token expiration error: extended the expiration date to 8days + captured ExpiredSignatureError to avoid UI error
* Bugfix: schedule page error for users who are not owner (unlikely since link is not shared but fixed anyway)
* Enhancement Home page: changed eventlist (removed capacity), carrousel (timer) and some text as per beta feedback
* Enhancement Home page: larger logo + text in web browser as per beta feedback
* Enhancement Event parking list: no longer showing 'SOLD OUT' next to event (no capacity shown in modal once you click on event in list)
* Enhancement Suggestions Box added to home page: user can suggest a location where he would like Parking Plaza to provide parking capacity (email notification to admin on server)
* Enhancement Become Owner: integrated email signup if no user has been logged in yet (one screen to become owner)
* Change: unit gets automatically added to Poi if Postgresql calculated distance <=2.5km (1.5km before) based on experience with unit A4 for RSCA

### Rel1.0 known issues ###
* My Parkings menu doesn't appear after becoming owner and adding parking (workaround: refresh page)
* Find Parking: scheduler returns same record twice

## Wiki

Please check the Wiki pages for howto's/learnings on several DevOps topics


## Issues ##

Logging and task list on issues raised by developers or testers
* Bugs
* Proposals/enhancements
* Tasks