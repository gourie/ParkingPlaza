/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
//import Utils from '../utils';

/**
 * React Component: ListFooter
 */
export default class ListFooter extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in ListFooter/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {
        //var activeWord = Utils.pluralize(this.props.count, 'schedule');

        var nowShowing = this.props.nowShowing;

        return (
            <div className="footer row">
                <span className="count"><strong>{this.props.count}</strong> schedules found</span>
            </div>
        );
    }
}

ListFooter.propTypes = {
    config: React.PropTypes.object,
    nowShowing: React.PropTypes.string,
    count: React.PropTypes.number
};