/*
*   Author: Joeri Nicolaes
*   ======================
*/

import 'babel-polyfill';

import React from 'react';
import { render } from 'react-dom';
import TestApp from './TestApp';

render(
	<TestApp />, document.getElementById("myDiv")
);