-- test entries for poi, owner, unit

INSERT INTO poi(poifriendlyname, country, city, poitypeid) VALUES ('Mechelen', 'Belgie', 'Mechelen', 2)
INSERT INTO poi(poifriendlyname, country, city, poitypeid) VALUES ('Voetbal Anderlecht', 'Belgie', 'Anderlecht', 1)

-- assertion: user with PK userid=1 exists (through signup)
INSERT INTO owner(userid, bankaccount) VALUES (1, 'BE12-3456791-01')

INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid) VALUES ('Mech1', '(51.021631,4.478939)', 1, 1, 1, 1)
INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid) VALUES ('Mech2', '(51.02173,4.479127)', 1, 1, 1, 1)
INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid) VALUES ('Mech3', '(51.021776,4.478979)', 1, 1, 1, 1)
INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid) VALUES ('Mech4', '(51.021651,4.478839)', 1, 1, 1, 1)
INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid) VALUES ('Mech5', '(51.02169,4.478752)', 1, 1, 1, 1)
INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid) VALUES ('Mech6', '(51.028183,4.471611)', 1, 1, 1, 1)




