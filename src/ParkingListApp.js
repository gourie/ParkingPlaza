/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import ReactDom from 'react-dom';
import ParkingList from './Components/ParkingList';

// read attribute sent via script and convert String into list of cities
var scriptTag = document.getElementById('myscript');
var s = scriptTag.getAttribute("data-conf");
//console.log(s);
var o = JSON.parse(s);

// ParkingListApp properties fed by server
// #1- filter: {direction, status})
// #2- schedules: List of available Poitypes as (poitypename)
// #3- userprops
// #4- loggedin

// Config for the app setup TODO - retrieve from server
var config = {
  debug: true
};

ReactDom.render(
	<ParkingList userProps={o['userprops']} loggedInAtStart={o['loggedin']} availablePois={o['poi']} availablePoiTypes={o['poitypes']} schedules={o['schedules']} viewfilter={o['filter']} unitaddress={o['unitaddress']} config={config} />,
	document.getElementById("content")
);