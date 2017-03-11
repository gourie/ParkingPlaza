INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('RSC Anderlecht - Test Match6', '2016-08-16 20:00:00+02', 1, 12);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert7', '2016-08-17 20:00:00+02', 2, 13);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-16 19:00:00+02', '2016-08-16 23:00:00+02', 15, 1, 1, 1, 12);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-17 19:00:00+02', '2016-08-17 23:00:00+02', 10, 1, 1, 1, 13);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-16 19:00:00+02', '2016-08-16 23:00:00+02', 15, 1, 1, 1, 12);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-17 19:00:00+02', '2016-08-17 23:00:00+02', 10, 1, 1, 1, 13);

-- Re-rest Beta DB V8.1 Schedules for testing (all set to available)
UPDATE schedule
SET statusid=1, userid=NULL
WHERE startdatetime > '2016-08-07'

-- GENERATE Beta DB V8.1
DELETE FROM events;
DELETE FROM users;
DELETE FROM owner;
DELETE FROM paymentgwstatus;
DELETE FROM unit;
DELETE FROM schedule;
DELETE FROM poievents;
DELETE FROM poi;
DELETE FROM poitype;


INSERT INTO poitype (poitypeid, poitype)
  VALUES (1, 'eventparking')

INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('RSC Anderlecht', 'Belgie', 'Anderlecht', 1, 1, '(50.835132, 4.297921)', 15);
INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('Vorst Nationaal', 'Belgie', 'Vorst', 2, 1, '(50.810313,4.326047)', 10);

INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('RSC Anderlecht - Test Match1', '2016-07-24 20:00:00+02', 1, 1);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('RSC Anderlecht - Test Match2', '2016-07-28 20:00:00+02', 1, 2);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('RSC Anderlecht - Test Match3', '2016-07-31 18:00:00+02', 1, 3);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('RSC Anderlecht - Test Match4', '2016-08-06 20:00:00+02', 1, 4);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('RSC Anderlecht - Test Match5', '2016-08-10 20:00:00+02', 1, 10);

INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert1', '2016-07-26 20:00:00+02', 2, 5);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert2', '2016-07-30 20:00:00+02', 2, 6);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert3', '2016-08-03 15:00:00+02', 2, 7);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert4', '2016-08-05 20:00:00+02', 2, 8);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert5', '2016-08-07 20:00:00+02', 2, 9);
INSERT INTO poievents (eventdescription, eventstart, poiid, poieventid)
  VALUES ('Vorst Test concert6', '2016-08-09 20:00:00+02', 2, 11);

INSERT INTO users(fullname, email, useruuid, userid, properties)
  VALUES ('test user1', 'pplazatest1@gmail.com', '2577527d-f2b7-4469-91d2-f91663906571', 1, '{"id": "104827487236946373578", "etag": "\"xw0en60W6-NurXn4VBU-CMjSPEw/ysTWJNFw5HjVYhuhS6P2qfvpfuw\"", "kind": "plus#person", "name": {"givenName": "Parking", "familyName": "Plaza"}, "image": {"url": "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg?sz=50", "isDefault": true}, "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzYwNTcxOC05MGRlLTRkZjAtYjYzMC0zNzEwMjZlMTQyNzAiLCJleHAiOjE0Njc0NTc0MDh9.iW28zNajZKrpM4XB9YHcdBMZQ1Br0HcqkcNe-7hAuLk", "emails": [{"type": "account", "value": "pplazatest1@gmail.com"}], "language": "nl", "verified": false, "isPlusUser": false, "objectType": "person", "displayName": "Parking Plaza", "toscheckdone": "2016-06-25T13:03:28.215334+02:00"}');
INSERT INTO users(fullname, email, useruuid, userid, properties)
  VALUES ('test user2', 'pplazatest2@gmail.com', '2577527d-f2b7-4469-91d2-f91663906572', 2, '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhNjY3NTgzNC00NGRlLTQyYmItYTQ5Ny1jYmVhZjY2YjgzMmUiLCJleHAiOjE0Njk1NjQyMzB9.n7vFoF5ChyST8G53ED3qtQJ_QLM5E3PmgIK0LHawwXc", "password": "123", "birthdate": "Tue Jul 19 2016 22:08:48 GMT+0200 (CEST)", "toscheckdone": "2016-07-19T22:16:40.763071+02:00", "confirmation-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbGFkZHJlc3MiOiJwcGxhemF0ZXN0MkBnbWFpbC5jb20iLCJleHAiOjE0NjkxMzIyMDB9.vX8sCb6Vek2iD9eSWvEyEsNIOn2IQQ3m-qpSWdzd4OU", "email-confirmation": "2016-07-19T22:17:10.400178+02:00"}');

INSERT INTO owner
  VALUES (1, 'BE063812903997', '{"ownermobile": "+32477123456", "toscheckdone": "2016-07-22T21:30:27.544302+02:00"}', 1);
INSERT INTO owner
  VALUES (2, 'BE081290399763', '{"ownermobile": "+32477456123", "toscheckdone": "2016-07-22T21:30:27.544302+02:00"}', 2);

INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('A1', '(50.830478, 4.296455)', 1, 1, 1, 1, 'Anderlecht', 1, '{"fulladdress": "Koning-Soldaatlaan 69, Anderlecht, Belgium"}');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid, properties)
  VALUES ('V1', '(50.808529, 4.321368)', 2, 1, 2, 2, 'Vorst', 2, '{"fulladdress": "Denayerlaan 6, Vorst, Belgium"}');

INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-07-24 19:00:00+02', '2016-07-24 23:00:00+02', 15, 1, 1, 1, 1);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-07-28 19:00:00+02', '2016-07-28 23:00:00+02', 15, 1, 1, 1, 2);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-07-31 17:00:00+02', '2016-07-31 21:00:00+02', 15, 1, 1, 1, 3);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-06 19:00:00+02', '2016-08-06 23:00:00+02', 15, 1, 1, 1, 4);

INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-07-26 19:00:00+02', '2016-07-26 23:00:00+02', 10, 1, 1, 1, 5);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-07-30 19:00:00+02', '2016-07-30 23:00:00+02', 10, 1, 1, 1, 6);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-03 14:00:00+02', '2016-08-03 18:00:00+02', 10, 1, 1, 1, 7);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-05 19:00:00+02', '2016-08-05 23:00:00+02', 10, 1, 1, 1, 8);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-07 19:00:00+02', '2016-08-07 23:00:00+02', 10, 1, 1, 1, 9);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-10 19:00:00+02', '2016-08-10 23:00:00+02', 15, 1, 1, 1, 10);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-09 19:00:00+02', '2016-08-09 23:00:00+02', 10, 1, 1, 1, 11);

INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-07-24 19:00:00+02', '2016-07-24 23:00:00+02', 15, 1, 1, 1, 1);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-07-28 19:00:00+02', '2016-07-28 23:00:00+02', 15, 1, 1, 1, 2);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-07-31 17:00:00+02', '2016-07-31 21:00:00+02', 15, 1, 1, 1, 3);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 2, '2016-08-06 19:00:00+02', '2016-08-06 23:00:00+02', 15, 1, 1, 1, 4);

INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-07-26 19:00:00+02', '2016-07-26 23:00:00+02', 10, 1, 1, 1, 5);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-07-30 19:00:00+02', '2016-07-30 23:00:00+02', 10, 1, 1, 1, 6);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-03 14:00:00+02', '2016-08-03 18:00:00+02', 10, 1, 1, 1, 7);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-05 19:00:00+02', '2016-08-05 23:00:00+02', 10, 1, 1, 1, 8);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-07 19:00:00+02', '2016-08-07 23:00:00+02', 10, 1, 1, 1, 9);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-10 19:00:00+02', '2016-08-10 23:00:00+02', 15, 1, 1, 1, 10);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-08-09 19:00:00+02', '2016-08-09 23:00:00+02', 10, 1, 1, 1, 11);
