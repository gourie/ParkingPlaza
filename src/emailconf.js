/*
*   Author: Joeri Nicolaes
*   ======================
*/

import 'babel-polyfill';

import React from 'react';
import ReactDom from 'react-dom';
import EmailConfApp from './EmailConfApp';

// read attribute sent via script and convert String into list of cities
var scriptTag = document.getElementById('myscript');
var s = scriptTag.getAttribute("data-conf");
//console.log(s);
var o = JSON.parse(s);

ReactDom.render(
	<EmailConfApp userProps={o['userprops']} loggedInAtStart={o['loggedin']} emailconf={o['emailconf']} availablePoiTypes={o['poitypes']} />,
	document.getElementById("header")
);
