/*
*   Author: Joeri Nicolaes
*   ======================
*/

// __tests__/eventparking-test.js
'use strict';

import { expect } from 'chai';
import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import EventParking from '../src/Components/EventParking';
import ShowParkingDetailsModal from '../src/Components/ShowParkingDetailsModal';
import ShowReservationModal from '../src/Components/ShowReservationModal';
import TestUtils from 'react-addons-test-utils';

// simulate test data received from server (indexHandler)
var availablePois = [  // 'poiname', 'poicountry', 'poicity', 'poicenter', 'poitype'
  { poiname: "R.S.C. Anderlecht", poicountry: 'Belgium', poicity: 'Anderlecht', poicenter: "(50.834295,4.298057)", poitype: "eventparking"}
];
var initialPoi = "R.S.C. Anderlecht";
var config = { debug: false };
var reservationStatus = false;
var linktodirections = "";

describe("EventParking module", function() {

    it('props spec: initialPoi', () => {
        expect(mount(<EventParking initialPoi={initialPoi} availablePois={availablePois} config={config} reservationStatus={reservationStatus} linktodirections={linktodirections}/>).props().initialPoi).to.equal(initialPoi);
    });

    it('props spec: availablePois', () => {
        expect(mount(<EventParking initialPoi={initialPoi} availablePois={availablePois} config={config} reservationStatus={reservationStatus} linktodirections={linktodirections}/>).props().availablePois).to.equal(availablePois);
    });

    it('props spec: config', () => {
        expect(mount(<EventParking initialPoi={initialPoi} availablePois={availablePois} config={config} reservationStatus={reservationStatus} linktodirections={linktodirections}/>).props().config).to.equal(config);
    });

    it('props spec: reservationStatus', () => {
        expect(mount(<EventParking initialPoi={initialPoi} availablePois={availablePois} config={config} reservationStatus={reservationStatus} linktodirections={linktodirections}/>).props().reservationStatus).to.equal(reservationStatus);
    });

    it('props spec: linktodirections', () => {
        expect(mount(<EventParking initialPoi={initialPoi} availablePois={availablePois} config={config} reservationStatus={reservationStatus} linktodirections={linktodirections}/>).props().linktodirections).to.equal(linktodirections);
    });

    it('props spec: possible to set props', () => {
        const wrapper = mount(<EventParking initialPoi={initialPoi} availablePois={availablePois} config={config} reservationStatus={reservationStatus} linktodirections={linktodirections}/>);
        wrapper.setProps({ linktodirections: "test" });
        expect(wrapper.props().linktodirections).to.equal("test");
    });

});
