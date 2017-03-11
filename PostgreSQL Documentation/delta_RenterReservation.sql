-- Table: public.poitype
-- DROP TABLE public.poitype;
CREATE TABLE public.poitype
(
  poitypeid integer PRIMARY KEY,
  poitype text,
  properties jsonb
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.poitype
  OWNER TO "ParkingPlaza";

-- Populate table with currently available poitypes
INSERT INTO poitype (poitype, poitypeid)
  VALUES ('eventparking', 1);
INSERT INTO poitype (poitype, poitypeid)
  VALUES ('cityparking', 2);

-- Alter table POI (not tested)
ALTER TABLE poi
ADD poitypeid integer REFERENCES poitype (poitypeid)



-- Sequence: public.poievents_poieventid_seq
-- DROP SEQUENCE public.poievents_poieventid_seq;
CREATE SEQUENCE public.poievents_poieventid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 2
  CACHE 1;
ALTER TABLE public.poievents_poieventid_seq
  OWNER TO "ParkingPlaza";

-- Table: public.poievents
-- DROP TABLE public.poievents;
CREATE TABLE public.poievents
(
  poieventid integer PRIMARY KEY DEFAULT nextval('poievents_poieventid_seq'::regclass),
  eventdescription text NOT NULL,
  eventstart timestamp with time zone NOT NULL,
  properties jsonb,
  poiid integer REFERENCES poi (poiid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.poievents
  OWNER TO "ParkingPlaza";



-- Table: public.timeunit
DROP TABLE public.timeunit;
CREATE TABLE public.timeunit
(
  timeunitid integer PRIMARY KEY,
  timeunit text,
  properties jsonb
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.timeunit
  OWNER TO "ParkingPlaza";

-- Populate table with currently available timeunits
INSERT INTO timeunit (timeunit, timeunitid)
  VALUES ('fixedprice', 1);
INSERT INTO timeunit (timeunit, timeunitid)
  VALUES ('hourly', 2);
INSERT INTO timeunit (timeunit, timeunitid)
  VALUES ('daily', 3);

-- Alter table SCHEDULE
ALTER TABLE schedule
ADD timeunitid integer REFERENCES timeunit (timeunitid);
ALTER TABLE schedule
RENAME COLUMN priceperhour TO pricepertimeunit;

ALTER TABLE schedule
ADD poieventid integer REFERENCES poievents (poieventid);

-- TESTING ONLY !!!!!!!!!!!!!!
-------------------------------

-- DROP all entries in poievents table
DELETE FROM poievents;
-- Start MANUAL Table fill for POIID==2 (R.S.C. Anderlecht)
-- Timezone UTC+2 used because of CEST aka Central European Summer Time (Daylight Saving Time - from March, 27 till October, 30)
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('R.S.C. Anderlecht - K.A.A Gent', '2016-05-01 14:30:00+02', 2);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('R.S.C. Anderlecht - K.V. Oostende', '2016-05-08 14:30:00+02', 2);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('R.S.C. Anderlecht - S.V. Zulte Waregem', '2016-05-22 14:30:00+02', 2);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('R.S.C. Anderlecht - Test1', '2016-07-08 18:00:00+02', 2);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('R.S.C. Anderlecht - Test2', '2016-07-15 20:00:00+02', 2);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('R.S.C. Anderlecht - Test3', '2016-06-10 19:00:00+02', 2);
-- TEST: add K.R.C Genk to have other POI (resulting POIID==3)
INSERT INTO poi (poifriendlyname, country, city, poitypeid, center)
  VALUES ('K.R.C. Genk', 'Belgie', 'Genk', 1, '(51.005009, 5.533164)');
-- Start MANUAL Table fill for POIID==3 (K.R.C. Genk)
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('K.R.C. Genk - Club Brugge K.V', '2016-04-20 20:30:00+02', 3);
INSERT INTO poievents (eventdescription, eventstart, poiid)
  VALUES ('K.R.C. Genk - Test1', '2016-06-05 20:30:00+02', 3);

-- DROP all entries in UNIT tables
DELETE FROM unit;
-- MANUALLY refill tables UNIT & SCHEDULE with test entries
-- Unit entries: 6 units belonging to one single owner with id=1 and poiid=1; unitid hardcoded to 1
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid)
  VALUES ('M1', '(51.021819, 4.478960)', 1, 1, 1, 1, 'Mechelen', 1);
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid)
  VALUES ('M2', '(51.021784, 4.479051)', 1, 1, 1, 1, 'Mechelen', 2);
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid)
  VALUES ('M3', '(51.021711, 4.478811)', 1, 1, 1, 1, 'Mechelen', 3);
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid)
  VALUES ('M4', '(51.028246, 4.471587)', 1, 1, 1, 1, 'Mechelen', 4);
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid)
  VALUES ('M5', '(51.028137, 4.471339)', 1, 1, 1, 1, 'Mechelen', 5);
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname, unitid)
  VALUES ('M6', '(51.028269, 4.471449)', 1, 1, 1, 1, 'Mechelen', 6);

-- DROP all entries in SCHEDULE tables
DELETE FROM schedule;
-- Schedule entries: available schedules for 6 units belonging to ownerID==1 and availability set for today ( May, 11)
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid)
  VALUES (1, 1, '2016-05-11 09:00:00+02', '2016-05-11 17:00:00+02', 2, 2, 1, 1);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid)
  VALUES (2, 1, '2016-05-11 11:00:00+02', '2016-05-11 15:00:00+02', 2, 2, 1, 1);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid)
  VALUES (3, 1, '2016-05-11 10:00:00+02', '2016-05-11 13:00:00+02', 2, 2, 1, 1);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (4, 1, '2016-05-22 13:30:00+02', '2016-05-22 17:30:00+02', 15, 1, 1, 1, 4);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (5, 1, '2016-05-22 13:30:00+02', '2016-05-22 17:30:00+02', 20, 1, 1, 1, 4);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (6, 1, '2016-05-22 13:30:00+02', '2016-05-22 17:30:00+02', 10, 1, 1, 1, 4);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (5, 1, '2016-07-08 17:00:00+02', '2016-07-08 21:00:00+02', 20, 1, 1, 1, 8);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (6, 1, '2016-07-15 19:00:00+02', '2016-07-15 23:00:00+02', 10, 1, 1, 1, 9);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (1, 1, '2016-05-22 13:30:00+02', '2016-05-22 17:30:00+02', 10, 1, 1, 1, 4);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 1, '2016-06-10 18:00:00+02', '2016-06-10 22:00:00+02', 10, 1, 1, 1, 10);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (3, 1, '2016-06-10 18:00:00+02', '2016-06-10 22:00:00+02', 10, 1, 1, 1, 10);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (2, 1, '2016-06-05 19:30:00+02', '2016-06-05 23:30:00+02', 10, 1, 1, 1, 11);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (3, 1, '2016-06-05 19:30:00+02', '2016-06-05 23:30:00+02', 10, 1, 1, 1, 11);