CREATE TABLE paymentgwstatus
(
  userid integer,
  ordernr integer,
  description text,
  paymentgwref text,
  status text,
  paymentdatetime timestamp with time zone,
  amountinclbtw double precision,
  invoicelink text,
  paymentid serial,
  properties jsonb,
  useruuid uuid,
  unitid integer,
  starttime timestamp with time zone,
  endtime timestamp with time zone,
  amountexclbtw double precision,
  btwamount double precision,
  CONSTRAINT paymentid PRIMARY KEY (paymentid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE paymentgwstatus
  OWNER TO "ParkingPlaza";