-- Update PROD DB V8.1 poievents based on updated RSCA calendar (17/09)
UPDATE poievents
SET eventstart = '2016-10-16 18:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KSC Lokeren';

UPDATE poievents
SET eventstart = '2016-10-26 20:30:00+02'
WHERE eventdescription = 'RSC Anderlecht - KV Mechelen';

INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - OH Leuven', '2016-09-21 19:30:00+02', 1);

-- Update PROD DB V8.1 poievents based on updated RSCA calendar (02/09)
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - FK Qabala', '2016-09-15 19:00:00+02', 1);

UPDATE poievents
SET eventstart = '2016-09-25 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KVC Westerlo';

UPDATE poievents
SET eventstart = '2016-10-16 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KSC Lokeren';

UPDATE poievents
SET eventstart = '2016-10-26 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KV Mechelen';

INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - 1. FSV Mainz 05', '2016-11-03 19:00:00+02', 1);

INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - St Etienne', '2016-12-08 19:00:00+02', 1);

UPDATE poievents
SET eventstart = '2016-11-03 19:00:00+01'
WHERE eventdescription = 'RSC Anderlecht - 1. FSV Mainz 05';

UPDATE poievents
SET eventstart = '2016-12-08 19:00:00+01'
WHERE eventdescription = 'RSC Anderlecht - St Etienne';



-- Update PROD DB V8.1 poievents based on updated RSCA calendar (17/08)
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - Slavia Prague', '2016-08-25 20:00:00+02', 1);


-- Update PROD DB V8.1 poievents based on updated RSCA calendar (08/08)
UPDATE poievents
SET eventstart = '2016-08-28 18:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KAA Gent';

UPDATE poievents
SET eventstart = '2016-09-11 18:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - SC Charleroi';

UPDATE poievents
SET eventstart = '2016-11-04 20:00:00+01'
WHERE eventdescription = 'RSC Anderlecht - KV Oostende';

UPDATE poievents
SET eventstart = '2016-11-25 20:00:00+01'
WHERE eventdescription = 'RSC Anderlecht - Excel Mouscron';

-- Update PROD DB V8.1 poievents based on updated RSCA calendar
UPDATE poievents
SET eventstart = '2016-08-26 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KAA Gent';

UPDATE poievents
SET eventstart = '2016-09-09 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - SC Charleroi';

UPDATE poievents
SET eventstart = '2016-09-23 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KVC Westerlo';

UPDATE poievents
SET eventstart = '2016-10-14 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KSC Lokeren';

UPDATE poievents
SET eventstart = '2016-10-25 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KV Mechelen';

UPDATE poievents
SET eventstart = '2016-11-04 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - KV Oostende';

UPDATE poievents
SET eventstart = '2016-11-25 20:00:00+02'
WHERE eventdescription = 'RSC Anderlecht - Excel Mouscron';

-- GENERATE PROD DB V8.1

DELETE FROM events;
DELETE FROM paymentgwstatus;
DELETE FROM users;
DELETE FROM owner;
DELETE FROM unit;
DELETE FROM schedule;
DELETE FROM poievents;
DELETE FROM poi;
DELETE FROM poitype;

INSERT INTO poitype (poitypeid, poitype)
  VALUES (1, 'eventparking')

INSERT INTO poi (poifriendlyname, country, city, poiid, poitypeid, center, pricepertimeunit)
  VALUES ('R.S.C. Anderlecht', 'Belgie', 'Anderlecht', 1, 1, '(50.835132, 4.297921)', 15);


INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KV Kortrijk', '2016-08-07 18:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KAA Gent', '2016-08-27 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - SC Charleroi', '2016-09-10 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KVC Westerlo', '2016-09-24 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KSC Lokeren', '2016-10-15 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KV Mechelen', '2016-10-26 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KV Oostende', '2016-11-05 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - Excel Mouscron', '2016-11-26 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - Club Brugge KV', '2016-12-10 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KAS Eupen', '2016-12-17 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - STVV', '2017-01-21 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - Standard de Liège', '2017-01-28 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - Zulte Waregem', '2017-02-11 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - KRC Genk', '2017-02-25 20:00:00+02', 1);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('RSC Anderlecht - Waasland-Beveren', '2017-03-11 20:00:00+02', 1);
