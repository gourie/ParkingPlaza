/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import moment from 'moment';

/**
 * React Component: DaySlot
 */
export default class DaySlot extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in DaySlot/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in DaySlot/render"); }

        var slots = [],
            nbslots = (this.props.slotend - this.props.slotstart)/this.props.slotsize;

        for (var i = 0; i < nbslots-1; i++) {
            var day = {
                name: date.format("dd").substring(0, 1),
                number: date.date(),
                isCurrentMonth: date.month() === month.month(),
                isToday: date.isSame(new Date(), "day"),
                date: date
            };
            slots.push(<span key={day.date.toString()} className={"day" + (day.isToday ? " today" : "") + (day.isCurrentMonth ? "" : " different-month") + (day.date.isSame(this.props.selected) ? " selected" : "")} onClick={this.props.select.bind(null, day)}>{day.number}</span>);
            date = date.clone();
            date.add(1, "d");

        }

        return <div className="week" key={days[0].toString()}>
            {days}
        </div>
    }
}

DaySlot.propTypes = {
    config: React.PropTypes.object,
};