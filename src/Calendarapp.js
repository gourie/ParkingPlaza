/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import ReactDom from 'react-dom';
import moment from 'moment';
import MonthCalendar from './Components/MonthCalendar';
import WeekCalendar from './Components/WeekCalendar';

// Config for the app setup TODO - retrieve from server
var config = {
  debug: true
};

var slot = {
  size: 2,
  start: 8,
  end: 22
};

ReactDom.render(
	<WeekCalendar viewstart={"startofweek"} viewdays={7} slot={slot} selected={moment()} config={config} />,
	document.getElementById("testDiv")
);

//ReactDom.render(
//	<MonthCalendar selected={moment()} config={config} />,
//	document.getElementById("testDiv")
//);