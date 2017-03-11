/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';

/**
 * React Component: DayNames
 */
export default class DayNames extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in DayNames/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {
        return <div className="week names">
            <span className="day">Sun</span>
            <span className="day">Mon</span>
            <span className="day">Tue</span>
            <span className="day">Wed</span>
            <span className="day">Thu</span>
            <span className="day">Fri</span>
            <span className="day">Sat</span>
        </div>;
    }
}

DayNames.propTypes = {
    config: React.PropTypes.object,
};