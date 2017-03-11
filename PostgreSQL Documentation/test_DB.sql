-- GENERATE TEST DB V8.1

-- DROP all entries in users table
DELETE FROM users;
-- Start MANUAL Table fill for USERS
INSERT INTO users(fullname, email, useruuid, userid)
  VALUES ('test user1', 'test1@parking-plaza.com', '2577527d-f2b7-4469-91d2-f91663906571', 1);
INSERT INTO users(fullname, email, useruuid, userid)
  VALUES ('test user2', 'test2@parking-plaza.com', '2577527d-f2b7-4469-91d2-f91663906572', 2);
INSERT INTO users(fullname, email, useruuid, userid)
  VALUES ('test user3', 'test3@parking-plaza.com', '2577527d-f2b7-4469-91d2-f91663906573', 3);
INSERT INTO users(fullname, email, useruuid, userid)
  VALUES ('test user4', 'test4@parking-plaza.com', '2577527d-f2b7-4469-91d2-f91663906574', 4);
INSERT INTO users(fullname, email, useruuid, userid)
  VALUES ('test user5', 'test5@parking-plaza.com', '2577527d-f2b7-4469-91d2-f91663906575', 5);
INSERT INTO users
  VALUES (6, 'test user6', 'test6@parking-plaza.com', '{"id": "104944001666965103847", "url": "https://plus.google.com/104944001666965103847", "etag": "\"xw0en60W6-NurXn4VBU-CMjSPEw/e1oxCY22zyFFZ4QkcEcYqr3la_I\"", "kind": "plus#person", "name": {"givenName": "Jeroen", "familyName": "Machiels"}, "urls": [{"type": "otherProfile", "label": "Picasa Web Albums", "value": "http://picasaweb.google.com/jeroenmachiels"}], "image": {"url": "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg?sz=50", "isDefault": true}, "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1YTI4NjdjMC04ZjhhLTQ2YmQtYjA5ZC1lOWUyODc2NmEzMTciLCJleHAiOjE0NjYyNzM4OTV9.iT2sNo0nTJnKBWY1cwQ9puVAJlQh6G7aoWb6cz13Vfw", "emails": [{"type": "account", "value": "jeroenmachiels@gmail.com"}], "gender": "male", "language": "en_GB", "verified": false, "isPlusUser": true, "objectType": "person", "displayName": "Jeroen Machiels", "toscheckdone": "2016-06-11T20:18:15.215506+02:00", "circledByCount": 29}', '5a2867c0-8f8a-46bd-b09d-e9e28766a317');
INSERT INTO users
  VALUES (7, 'test email user7', 'test7@parking-plaza.com', '{"token": "", "password": "12", "birthdate": "Tue Jun 28 2016 10:39:37 GMT+0200 (CEST)", "toscheckdone": "2016-06-28T10:39:59.427543+02:00", "confirmation-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbGFkZHJlc3MiOiJwcGxhemF0ZXN0MkBnbWFpbC5jb20iLCJleHAiOjE0NjcyNzU5OTl9.6dBBG4I7L2NDF6Ut71EVTTT3g4gwfOqmYYf4rylhjCc", "email-confirmation": "pending"}' , '2577527d-f2b7-4469-91d2-f91663906577');


-- DROP all entries in tables
DELETE FROM schedule;
DELETE FROM poievents;
DELETE FROM poi;

INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('Mechelen', 'Belgie', 'Mechelen', 1, 1, '(51.02787,4.4795)', 2);
INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('Leuven', 'Belgie', 'Leuven', 2, 1, '(50.879973, 4.699591)', 1.7);
INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('R.S.C. Anderlecht', 'Belgie', 'Anderlecht', 3, 2, '(50.835132, 4.297921)', 15);
INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('K.R.C. Genk', 'Belgie', 'Genk', 4, 2, '(51.005009,5.533164)', 5);
UPDATE poi
  SET center='(50.834295, 4.298057)'
  WHERE poifriendlyname='R.S.C. Anderlecht';

INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('R.S.C. Anderlecht - K.A.A Gent', '2016-05-01 14:30:00+02', 3, 1);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('R.S.C. Anderlecht - K.V. Oostende', '2016-05-08 14:30:00+02', 3, 2);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('R.S.C. Anderlecht - S.V. Zulte Waregem', '2016-05-22 14:30:00+02', 3, 3);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('R.S.C. Anderlecht - Test1', '2016-07-08 18:00:00+02', 3, 4);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('R.S.C. Anderlecht - Test2', '2016-07-15 20:00:00+02', 3, 5);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('R.S.C. Anderlecht - Test3', '2016-06-10 19:00:00+02', 3, 6);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('K.R.C. Genk - Club Brugge K.V', '2016-04-20 20:30:00+02', 4, 7);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('K.R.C. Genk - Test1', '2016-06-05 20:30:00+02', 4, 8);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('K.R.C. Genk - Test2', '2016-06-10 14:30:00+02', 4, 9);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('K.R.C. Genk - Test3', '2016-06-15 18:00:00+02', 4, 10);

INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-06-10 18:00:00+02', '2016-06-10 22:00:00+02', 15, 1, 1, 1, 6);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (5, 5, '2016-06-10 13:30:00+02', '2016-06-10 17:30:00+02', 5, 1, 1, 1, 9);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-05-22 13:30:00+02', '2016-05-22 17:30:00+02', 15, 1, 1, 1, 3);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid, userid)
  VALUES (2, 1, '2016-07-08 17:00:00+02', '2016-07-08 21:00:00+02', 15, 1, 1, 4, 4, 5);
INSERT INTO schedule (scheduleid, unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, 1, '2016-06-24 13:30:00+02', '2016-06-24 17:30:00+02', 15, 1, 1, 1, NULL);


-- DROP all entries in UNIT tables
DELETE FROM unit;
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('A1', '(50.835,4.298)', 1, 1, 3, 1, 'Anderlecht', 1, '{"fulladdress": "Teststraatt 1, Anderlecht, Belgium", "setschedule": {"poieventid": 10, "timestamp":"26/2"}}');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('A2', '(50.84,4.28)', 2, 1, 3, 2, 'Anderlecht', 2, '{"fulladdress": "Teststraatt 2, Anderlecht, Belgium"}');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('A3', '(50.83,4.275)', 3, 1, 3, 3, 'Anderlecht', 3, '{"fulladdress": "Teststraatt 3, Anderlecht, Belgium"}');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('G1', '(51.005,5.53)', 4, 1, 4, 4, 'Genk', 4, '{"fulladdress": "Teststraatt 1, Genk, Belgium"}');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('G2', '(51.01,5.54)', 5, 1, 4, 5, 'Genk', 5, '{"fulladdress": "Teststraatt 2, Genk, Belgium"}');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('G3', '(51.02,5.55)', 5, 1, 4, 5, 'Genk', 6, '{"fulladdress": "Teststraatt 3, Genk, Belgium"}');
INSERT INTO unit
  VALUES ('L1', '(50.8057640000000035,4.13733280000000025)', 6, 1, 0, 2, '{"fulladdress": "Negenbunderstraat 10, Lennik, Belgium"}', 7, 'Lennik');
INSERT INTO unit
  VALUES ('L2', '(50.806474399999999,4.14523799999999998)', 6, 1, 0, 2, '{"fulladdress": "Joseph Van Den Bosschestraat 17, Lennik, Belgium"}', 8, 'Lennik');

DELETE FROM owner;
INSERT INTO owner(ownerid, userid, bankaccount)
  VALUES (1, 1, 'BE12-34567890-22');
INSERT INTO owner
  VALUES (6, 'BE063978129039', '{"ownermobile": "+32478222391", "toscheckdone": "2016-06-11T21:01:27.544302+02:00"}', 2);

DELETE FROM paymentgwstatus;
INSERT INTO paymentgwstatus(useruuid, ordernr, description, amountinclbtw, amountExclbtw, btwamount, unitid, starttime, endtime)
  VALUES ('2577527d-f2b7-4469-91d2-f91663906571', 123, 'test payment for unit-test', 20, 16.53, 3.47, 1, '2016-06-10 18:00:00+02', '2016-06-10 22:00:00+02');