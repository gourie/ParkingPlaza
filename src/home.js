/*
*   Author: Joeri Nicolaes
*   ======================
*/

import 'babel-polyfill';

import React from 'react';
import ReactDom from 'react-dom';
import HomeApp from './HomeApp';
import FooterApp from './FooterApp';
import HeaderApp from './HeaderApp';

// read attribute sent via script and convert String into list of cities
var scriptTag = document.getElementById('myscript');
var s = scriptTag.getAttribute("data-conf");
//console.log(s);
var o = JSON.parse(s);

// ParkingApp properties fed by server
// #1- poi: list of released Pois as {name, center, poitype})
// #2- poitypes: List of available Poitypes as (poitypename)
// #3- string displayName of user if login done (currently only catched at sign-up), else ""
// #4- boolean flag for showing LoginModal (false if nothing sent)
var serverConfig = {
  poiList: o['poi'],
  poiTypes: o['poitypes'],
  user: o['userprops'],
  loggedIn: o['loggedin'],
  reservationStatus: o['reservationstatus'],
  linktodirections: o['linktodirections']
};

ReactDom.render(
	<HomeApp userProps={serverConfig.user} loggedInAtStart={serverConfig.loggedIn} availablePois={serverConfig.poiList} availablePoiTypes={serverConfig.poiTypes} reservationStatus={serverConfig.reservationStatus} linktodirections={serverConfig.linktodirections}/>,
	document.getElementById("content")
);
