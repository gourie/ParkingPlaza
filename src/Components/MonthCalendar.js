/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import moment from 'moment';
import Week from './Week';
import DayNames from './DayNames';

/**
 * React Component: MonthCalendar
 */
export default class MonthCalendar extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in MonthCalendar/constructor"); }

        // init state
        this.state = {
            month: this.props.selected.clone(),
            selectedDay: null
        };

        // catch bindings for click
        this.previous = this.previous.bind(this);
        this.next = this.next.bind(this);
        this.select = this.select.bind(this);
        this.renderWeeks = this.renderWeeks.bind(this);
        this.renderMonthLabel = this.renderMonthLabel.bind(this);

    }

    /**
     * Standard React method: runs after initial render
     */
    componentDidMount() {

        if (this.props.config.debug==true) { console.log("in MonthCalendar/componentDidMount"); }
    }

    /**
     * Go to previous month
     */
    previous() {

        if (this.props.config.debug==true) { console.log("in MonthCalendar/previous"); }

        var mo = this.state.month;
        mo.add(-1, "M");
        this.setState({ month: mo });
    }

    /**
     * Go to next month
     */
    next() {

        if (this.props.config.debug==true) { console.log("in MonthCalendar/next"); }

        var mo = this.state.month;
        mo.add(1, "M");
        this.setState({ month: mo });
    }

    /**
     * Updated selected day
     */
    select(day) {

        if (this.props.config.debug==true) { console.log("in MonthCalendar/select"); }

        this.state.selectedDay = day.date;
        this.forceUpdate();
    }

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in MonthCalendar/render"); }

        return <div className="calendar">
            <div className="header">
                <i className="fa fa-angle-left" onClick={this.previous}></i>
                {this.renderMonthLabel()}
                <i className="fa fa-angle-right" onClick={this.next}></i>
            </div>
            <DayNames config={this.props.config}/>
            {this.renderWeeks()}
        </div>;
    }

    /**
     * Render weeks in Month view
     */
    renderWeeks() {
        var weeks = [],
            done = false,
            date = this.state.month.clone().startOf("month").day("Sunday"),
            monthIndex = date.month(),
            count = 0;

        while (!done) {
            weeks.push(<Week key={date.toString()} date={date.clone()} month={this.state.month} select={this.select} selected={this.state.selectedDay} config={this.props.config} />);
            date.add(1, "w");
            done = count++ > 2 && monthIndex !== date.month();
            monthIndex = date.month();
        }

        return weeks;
    }

    /**
     * Render Month label
     */
    renderMonthLabel() {
        return <span>{this.state.month.format("MMMM, YYYY")}</span>;
    }
}

MonthCalendar.propTypes = {
    selected: React.PropTypes.object,
    config: React.PropTypes.object,
};