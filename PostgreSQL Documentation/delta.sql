ALTER TABLE users ADD COLUMN useruuid UUID

-- Joeri - 18/03/2016
-- Add cityName field to Table public.unit
ALTER TABLE unit ADD COLUMN cityName text
-- Add point object to Table public.poi
ALTER TABLE poi ADD COLUMN center point
-- Update the two existing POI's with their center "lat,lon"
UPDATE poi
SET center='51.02787,4.47950'
WHERE poifriendlyname='Mechelen'

UPDATE poi
SET center='50.835118,4.298426'
WHERE poifriendlyname='Voetbal Anderlecht'

-- Joeri - 09/03/2016

-- Table: public.poitype
-- DROP TABLE public.poitype;

CREATE SEQUENCE poitype_poitypeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.poitype
(
  poitype text,
  properties jsonb,
  poitypeid integer NOT NULL DEFAULT nextval('poitype_poitypeid_seq'::regclass),
  CONSTRAINT poitypeid PRIMARY KEY (typeid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.poitype
  OWNER TO "ParkingPlaza";


-- Add poitypeid field to Table public.poi
ALTER TABLE poi ADD COLUMN poitypeid integer NOT NULL


-- Basic config (admin setting)
INSERT INTO type(type) VALUES ('parking lot')
INSERT INTO type(type) VALUES ('garagebox')

INSERT INTO poitype(poitype) VALUES ('eventparking')
INSERT INTO poitype(poitype) VALUES ('cityparking')