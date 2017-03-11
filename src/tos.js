/*
*   Author: Joeri Nicolaes
*   ======================
*/

import 'babel-polyfill';

import React from 'react';
import ReactDom from 'react-dom';
import TosApp from './TosApp';
import HeaderApp from './HeaderApp';

// read attribute sent via script and convert String into list of cities
var scriptTag = document.getElementById('myscript');
var s = scriptTag.getAttribute("data-conf");
//console.log(s);
var o = JSON.parse(s);

ReactDom.render(
	<TosApp tos={o['tos']} userProps={o['userprops']} loggedInAtStart={o['loggedin']} availablePoiTypes={o['poitypes']} />,
	document.getElementById("content")
);
