/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';


/**
 * React Component: ScheduleItem
 */
export default class ScheduleItem extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

    }

    /**
     * Standard React method: render
     */
    render() {
        return (
            <div className={"schedule row" + (this.props.item.changed == "true" ? " changed" : "")} key={this.props.item.eventdescription}>
                <div className="schedule item col-md-4 col-xs-4">
                    {this.props.item.eventstart}
                </div>
                <div className="schedule item col-md-5 col-xs-5">
                    {this.props.item.eventdescription}
                </div>
                <div className="schedule item col-md-3 col-xs-3">
                    {this.props.item.schedulestatus}
                </div>
            </div>
        );
    }
}

ScheduleItem.propTypes = {
    item: React.PropTypes.object,
};