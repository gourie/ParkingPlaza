/*
*   Author: Joeri Nicolaes
*   ======================
*/

// __tests__/scheduleitem-test.js
'use strict';

import { expect } from 'chai';
import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import ScheduleItem from '../src/Components/ScheduleItem';
import TestUtils from 'react-addons-test-utils';

// simulate test data received from server (setScheduleAPIHandler)
var schedules = [
  { eventstart: '17/6', eventdescription: 'RSCA-Test1', schedulestatus: 'available', changed: 'false'},
  { eventstart: '10/6', eventdescription: 'RSCA-Test2', schedulestatus: 'available', changed: 'true'},
  { eventstart: '5/6', eventdescription: 'RSCA-Test3', schedulestatus: 'not available', changed: 'false'}
];
var item = schedules[0];
var itemChanged = schedules[1];

describe("ScheduleItem module", function() {

    it('props spec: item', () => {
        expect(mount(<ScheduleItem key={item.eventstart} item={item}/>).props().item).to.equal(item);
    });

    it('props spec: possible to set props', () => {
        const wrapper = mount(<ScheduleItem key={item.eventstart} item={item}/>);
        wrapper.setProps({ item: schedules[1] });
        expect(wrapper.props().item).to.equal(schedules[1]);
    });

    it('render spec: 1x `div.schedule.row`', () => {
    expect(shallow(<ScheduleItem key={item.eventstart} item={item}/>).find('div.schedule.row').length).to.equal(1);
    });

    it('key spec: eventdescription set as key', () => {
        expect(shallow(<ScheduleItem key={item.eventstart} item={item}/>).find('div.schedule.row').key()).to.equal(item.eventdescription);
    });

    it('render spec: 1x `div.schedule.row` if changed flag set in props', () => {
    expect(shallow(<ScheduleItem key={item.eventstart} item={itemChanged}/>).is('div.schedule.row.changed')).to.equal(true);
    });

    it('render spec: 4x `.schedule`', () => {
    expect(mount(<ScheduleItem key={item.eventstart} item={item}/>).find('.schedule').length).to.equal(4);
    });

    it('render spec: 3x `div.schedule.item`', () => {
    expect(shallow(<ScheduleItem key={item.eventstart} item={item}/>).find('div.schedule.item').length).to.equal(3);
    });

    it('render spec: check if render contains item.eventstart', () => {
    expect(shallow(<ScheduleItem key={item.eventstart} item={item}/>).text()).to.contain(item.eventstart);
    });

    it('render spec: check if render contains item.eventdescription', () => {
    expect(shallow(<ScheduleItem key={item.eventstart} item={item}/>).text()).to.contain(item.eventdescription);
    });

    it('render spec: check if render contains item.schedulestatus', () => {
    expect(shallow(<ScheduleItem key={item.eventstart} item={item}/>).text()).to.contain(item.schedulestatus);
    });

});

describe('loading of ScheduleItem module by parent', () => {



//    it("renders an div", function () {
//
//        var schedule = TestUtils.renderIntoDocument(
//            <ScheduleItem key={item.eventstart} item={item} />
//        );
//
//        var div = TestUtils.findRenderedDOMComponentWithClass(
//           schedule, 'schedule'
//        );
//
//        print(div);
//        //expect(div.type).to.be.a('div');
//    });

//  it('render and check output', () ==> {
//      var item = {};
//      <ScheduleItem key={item.eventstart} item={item} />
//
//      var renderer = TestUtils.createRenderer();
//      result = renderer.getRenderOutput();
//      expect(result.type).toBe('div');
//      expect(result.props.children).toEqual([
//          <span className="heading">Title</span>,
//          <BecomeOwnerApp userProps=userPropsInput poiTypes=poiTypesInput />
//      ]);
//  });

//  it('changes the text after click', () => {
//    // Render a checkbox with label in the document
//    const checkbox = TestUtils.renderIntoDocument(
//      <CheckboxWithLabel labelOn="On" labelOff="Off" />
//    );
//
//    const checkboxNode = ReactDOM.findDOMNode(checkbox);
//
//    // Verify that it's Off by default
//    expect(checkboxNode.textContent).toEqual('Off');
//
//    // ...
//  });
});