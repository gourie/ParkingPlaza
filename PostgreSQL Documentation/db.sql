--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE "ParkingPlaza";
ALTER ROLE "ParkingPlaza" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION NOBYPASSRLS PASSWORD 'md5f04820139a7dde57793eaec4a4a3bd4f' VALID UNTIL 'infinity';
CREATE ROLE jeroen;
ALTER ROLE jeroen WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;






--
-- Database creation
--

CREATE DATABASE "Benares" WITH TEMPLATE = template0 OWNER = "ParkingPlaza";
REVOKE ALL ON DATABASE template1 FROM PUBLIC;
REVOKE ALL ON DATABASE template1 FROM jeroen;
GRANT ALL ON DATABASE template1 TO jeroen;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect "Benares"

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.0
-- Dumped by pg_dump version 9.5.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: cube; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS cube WITH SCHEMA public;


--
-- Name: EXTENSION cube; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION cube IS 'data type for multidimensional cubes';


--
-- Name: earthdistance; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS earthdistance WITH SCHEMA public;


--
-- Name: EXTENSION earthdistance; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION earthdistance IS 'calculate great-circle distances on the surface of the Earth';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: currency; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE currency (
    currency text,
    properties jsonb,
    currencyid integer NOT NULL
);


ALTER TABLE currency OWNER TO "ParkingPlaza";

--
-- Name: currency_currencyid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE currency_currencyid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE currency_currencyid_seq OWNER TO "ParkingPlaza";

--
-- Name: currency_currencyid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE currency_currencyid_seq OWNED BY currency.currencyid;


--
-- Name: events; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE events (
    "timestamp" timestamp without time zone,
    groupname text,
    properties jsonb,
    eventid integer NOT NULL
);


ALTER TABLE events OWNER TO "ParkingPlaza";

--
-- Name: events_eventid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE events_eventid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE events_eventid_seq OWNER TO "ParkingPlaza";

--
-- Name: events_eventid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE events_eventid_seq OWNED BY events.eventid;


--
-- Name: owner; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE owner (
    userid integer NOT NULL,
    bankaccount text NOT NULL,
    properties jsonb,
    ownerid integer NOT NULL
);


ALTER TABLE owner OWNER TO "ParkingPlaza";

--
-- Name: owner_ownerid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE owner_ownerid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE owner_ownerid_seq OWNER TO "ParkingPlaza";

--
-- Name: owner_ownerid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE owner_ownerid_seq OWNED BY owner.ownerid;


--
-- Name: poi; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE poi (
    poifriendlyname text NOT NULL,
    country text,
    city text,
    properties jsonb,
    poiid integer NOT NULL
);


ALTER TABLE poi OWNER TO "ParkingPlaza";

--
-- Name: poi_poiid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE poi_poiid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE poi_poiid_seq OWNER TO "ParkingPlaza";

--
-- Name: poi_poiid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE poi_poiid_seq OWNED BY poi.poiid;


--
-- Name: schedule; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE schedule (
    unitid integer NOT NULL,
    ownerid integer NOT NULL,
    startdatetime timestamp without time zone,
    enddatetime timestamp without time zone,
    priceperhour integer,
    currencyid integer NOT NULL,
    statusid integer NOT NULL,
    userid integer NOT NULL,
    properties jsonb,
    scheduleid integer NOT NULL
);


ALTER TABLE schedule OWNER TO "ParkingPlaza";

--
-- Name: schedule_scheduleid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE schedule_scheduleid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE schedule_scheduleid_seq OWNER TO "ParkingPlaza";

--
-- Name: schedule_scheduleid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE schedule_scheduleid_seq OWNED BY schedule.scheduleid;


--
-- Name: status; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE status (
    status text,
    properties jsonb,
    statusid integer NOT NULL
);


ALTER TABLE status OWNER TO "ParkingPlaza";

--
-- Name: status_statusid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE status_statusid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE status_statusid_seq OWNER TO "ParkingPlaza";

--
-- Name: status_statusid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE status_statusid_seq OWNED BY status.statusid;


--
-- Name: type; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE type (
    type text,
    properties jsonb,
    typeid integer NOT NULL
);


ALTER TABLE type OWNER TO "ParkingPlaza";

--
-- Name: type_typeid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE type_typeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE type_typeid_seq OWNER TO "ParkingPlaza";

--
-- Name: type_typeid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE type_typeid_seq OWNED BY type.typeid;


--
-- Name: unit; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE unit (
    friendlyname text NOT NULL,
    latitudelongitude point,
    userid integer NOT NULL,
    typeid integer NOT NULL,
    poiid integer NOT NULL,
    ownerid integer NOT NULL,
    properties jsonb,
    unitid integer NOT NULL
);


ALTER TABLE unit OWNER TO "ParkingPlaza";

--
-- Name: unit_unitid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE unit_unitid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unit_unitid_seq OWNER TO "ParkingPlaza";

--
-- Name: unit_unitid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE unit_unitid_seq OWNED BY unit.unitid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ParkingPlaza
--

CREATE TABLE users (
    userid integer NOT NULL,
    fullname text,
    email text,
    properties jsonb
);


ALTER TABLE users OWNER TO "ParkingPlaza";

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: ParkingPlaza
--

CREATE SEQUENCE users_userid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_userid_seq OWNER TO "ParkingPlaza";

--
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ParkingPlaza
--

ALTER SEQUENCE users_userid_seq OWNED BY users.userid;


--
-- Name: currencyid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY currency ALTER COLUMN currencyid SET DEFAULT nextval('currency_currencyid_seq'::regclass);


--
-- Name: eventid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY events ALTER COLUMN eventid SET DEFAULT nextval('events_eventid_seq'::regclass);


--
-- Name: ownerid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY owner ALTER COLUMN ownerid SET DEFAULT nextval('owner_ownerid_seq'::regclass);


--
-- Name: poiid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY poi ALTER COLUMN poiid SET DEFAULT nextval('poi_poiid_seq'::regclass);


--
-- Name: scheduleid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY schedule ALTER COLUMN scheduleid SET DEFAULT nextval('schedule_scheduleid_seq'::regclass);


--
-- Name: statusid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY status ALTER COLUMN statusid SET DEFAULT nextval('status_statusid_seq'::regclass);


--
-- Name: typeid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY type ALTER COLUMN typeid SET DEFAULT nextval('type_typeid_seq'::regclass);


--
-- Name: unitid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY unit ALTER COLUMN unitid SET DEFAULT nextval('unit_unitid_seq'::regclass);


--
-- Name: userid; Type: DEFAULT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY users ALTER COLUMN userid SET DEFAULT nextval('users_userid_seq'::regclass);


--
-- Name: currencyid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY currency
    ADD CONSTRAINT currencyid PRIMARY KEY (currencyid);


--
-- Name: eventid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY events
    ADD CONSTRAINT eventid PRIMARY KEY (eventid);


--
-- Name: ownerid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY owner
    ADD CONSTRAINT ownerid PRIMARY KEY (ownerid);


--
-- Name: poiid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY poi
    ADD CONSTRAINT poiid PRIMARY KEY (poiid);


--
-- Name: scheduleid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT scheduleid PRIMARY KEY (scheduleid);


--
-- Name: statusid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY status
    ADD CONSTRAINT statusid PRIMARY KEY (statusid);


--
-- Name: typeid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY type
    ADD CONSTRAINT typeid PRIMARY KEY (typeid);


--
-- Name: unitid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY unit
    ADD CONSTRAINT unitid PRIMARY KEY (unitid);


--
-- Name: userid; Type: CONSTRAINT; Schema: public; Owner: ParkingPlaza
--

ALTER TABLE ONLY users
    ADD CONSTRAINT userid PRIMARY KEY (userid);


--
-- Name: public; Type: ACL; Schema: -; Owner: jeroen
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM jeroen;
GRANT ALL ON SCHEMA public TO jeroen;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.0
-- Dumped by pg_dump version 9.5.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: jeroen
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: public; Type: ACL; Schema: -; Owner: jeroen
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM jeroen;
GRANT ALL ON SCHEMA public TO jeroen;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.0
-- Dumped by pg_dump version 9.5.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: template1; Type: COMMENT; Schema: -; Owner: jeroen
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: jeroen
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM jeroen;
GRANT ALL ON SCHEMA public TO jeroen;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

