/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';

/**
 * React Component: ListHeader
 */
export default class ListHeader extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in ListHeader/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {
        return (
            <div className="names row">
                <div className="names col-md-4 col-xs-4">Time</div>
                <div className="names col-md-5 col-xs-5">Event</div>
                <div className="names col-md-3 col-xs-3">Status</div>
            </div>
        );
    }
}

ListHeader.propTypes = {
    config: React.PropTypes.object,
};