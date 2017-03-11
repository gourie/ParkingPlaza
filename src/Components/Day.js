/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import moment from 'moment';

/**
 * React Component: Day
 */
export default class Day extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in Day/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in Day/render"); }

        var days = [],
            date = this.props.date;

        // add slot label
        days.push(<span key={date.format("HH:mm").toString()} className={"day header"}>{date.format("HH:mm").toString()}</span>);
        for (var i = 0; i < this.props.nbofDays; i++) {
            var day = {
                name: date.format("dd").substring(0, 1),
                number: date.date(),
                isPast: date < moment(),
                isToday: date.isSame(new Date(), "day"),
                date: date
            };
            days.push(<span key={day.date.toString()} className={"day" + (day.isToday ? " today" : "") + (day.isPast && !day.isToday ? " day-in-past" : "") + (day.date.isSame(this.props.selected) ? " selected" : "")} onClick={this.props.select.bind(null, day)}></span>);
            date = date.clone();
            date.add(1, "d");
        }

        return <div className="week" key={days[0].toString()}>
            {days}
        </div>
    }
}

Day.propTypes = {
    date: React.PropTypes.object,
    config: React.PropTypes.object,
    nbofDays: React.PropTypes.number,
};