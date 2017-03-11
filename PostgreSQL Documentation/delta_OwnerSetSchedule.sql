-- Alter table POI
ALTER TABLE poi
ADD pricepertimeunit integer;

INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname)
  VALUES ('A1', '(50.832,4.277)', 1, 1, 2, 1, 'Anderlecht');
INSERT INTO unit (friendlyname, latitudelongitude, userid, typeid, poiid, ownerid, cityname)
  VALUES ('A2', '(50.84,4.28)', 43, 1, 2, 2, 'Anderlecht');


INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (245, 1, '2016-07-08 17:00:00+02', '2016-07-08 21:00:00+02', 15, 1, 1, 1, 8);
INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid)
  VALUES (245, 1, '2016-07-15 19:00:00+02', '2016-07-15 23:00:00+02', 15, 1, 1, 1, 9);

INSERT INTO owner(userid, bankaccount)
  VALUES (43, 'BE12-34567890-22');