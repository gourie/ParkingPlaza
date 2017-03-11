/*
*   Author: Joeri Nicolaes
*   ======================
*/

import React from 'react';
import ReactDom from 'react-dom';
import ParkingMapApp from './ParkingMapApp';

// read attribute sent via script and convert String into list of cities
var scriptTag = document.getElementById('myscript');
var s = scriptTag.getAttribute("data-conf");
var o = JSON.parse(s);

// ParkingApp properties fed by server
// #1- poi: list of released Pois as {name, center, poitype})
// #2- poitypes: List of available Poitypes as (poitypename)
// #3- string displayName of user if login done (currently only catched at sign-up), else ""
// #4- boolean flag for showing LoginModal (false if nothing sent)
var serverConfig = {
  poiList: o['poi'],
  poiTypes: o['poitypes'],
  eventList: o['events'],
  initialPoi: o['initialPoi'],
  user: o['userprops'],
  loggedIn: o['loggedin'],
  reservationStatus: o['reservationstatus']
};

/**
 * Standard React method: link the ParkingApp to the html DOM element
 */
ReactDom.render(
	<ParkingMapApp reservationStatus={serverConfig.reservationStatus} userProps={serverConfig.user} loggedInAtStart={serverConfig.loggedIn} availablePois={serverConfig.poiList} availablePoiTypes={serverConfig.poiTypes} initialPoi={serverConfig.initialPoi} eventList={serverConfig.eventList} />,
	document.getElementById("content")
);