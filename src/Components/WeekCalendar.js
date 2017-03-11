/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import moment from 'moment';
import DayNames from './DayNamesWeekView';
import Day from './Day';

/**
 * React Component: WeekCalendar
 */
export default class WeekCalendar extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in WeekCalendar/constructor"); }

        // init state
        this.state = {
            month: this.props.selected.clone(),
            week: this.props.selected.clone(),
            selectedDay: null
        };

        // catch bindings for click
        this.previous = this.previous.bind(this);
        this.next = this.next.bind(this);
        this.select = this.select.bind(this);
        this.renderDays = this.renderDays.bind(this);
        this.renderWeekLabel = this.renderWeekLabel.bind(this);

    }

    /**
     * Standard React method: runs after initial render
     */
    componentDidMount() {

        if (this.props.config.debug==true) { console.log("in WeekCalendar/componentDidMount"); }
    }

    /**
     * Go to previous month
     */
    previous() {

        if (this.props.config.debug==true) { console.log("in WeekCalendar/previous"); }

        var we = this.state.week;
        we.add(-1, "w");
        this.setState({ week: we });
    }

    /**
     * Go to next month
     */
    next() {

        if (this.props.config.debug==true) { console.log("in WeekCalendar/next"); }

        var we = this.state.week;
        we.add(1, "w");
        this.setState({ week: we });
    }

    /**
     * Updated selected day
     */
    select(day) {

        if (this.props.config.debug==true) { console.log("in WeekCalendar/select"); }

        this.state.selectedDay = day.date;
        this.forceUpdate();
    }

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in WeekCalendar/render"); }

        return <div className="calendar">
            <div className="header">
                <i className="fa fa-angle-left" onClick={this.previous}></i>
                {this.renderWeekLabel()}
                <i className="fa fa-angle-right" onClick={this.next}></i>
            </div>
            <DayNames config={this.props.config}/>
            {this.renderDays()}
        </div>;
    }

    /**
     * Render days in Week view
     */
    renderDays() {
        var slots = [],
            done = false,
            slotsize = this.props.slot.size,
            slotstart = this.props.slot.start,
            slotend = this.props.slot.end,
            date = (this.props.viewstart == 'startofweek') ? this.state.week.clone().startOf("week").day("Sunday").add(slotstart,"h") : this.state.week.clone().add(slotstart,"h"),  //Sunday May, 22 - WeekView starts at week (hard-coded to Sunday) - TODO: change to fetch from locale
            count = 0;

        //days.push(<DaySlot key={date.toString()} slotsize={slotsize} slotstart={slotstart} slotend={slotend} config={this.props.config} />);

        while (!done) {
            slots.push(<Day key={date.toString()} date={date.clone()} nbofDays={this.props.viewdays} select={this.select} selected={this.state.selectedDay} config={this.props.config} />);
            date.add(slotsize, "h");
            done = count++ > ((slotend - slotstart)/slotsize - 1);
        }

        return slots;
    }

    /**
     * Render Week labels
     */
    renderWeekLabel() {
        return <span> {'Week ' + this.state.week.format("W") + " (" + this.state.week.startOf("week").format("DD MMM - ") + this.state.week.endOf("week").format("DD MMM") + ")"} </span>;
    }

}

WeekCalendar.propTypes = {
    selected: React.PropTypes.object,
    config: React.PropTypes.object,
    viewstart: React.PropTypes.string,
    viewdays: React.PropTypes.number,
};