/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';

/**
 * React Component: DropDownListItem
 */
export default class DropDownListItem extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        //console.log("in DropDownListItem/constructor", this.props.item);

    }

    /**
     * Standard React method: render
     */
    render() {
        var item = this.props.item;

        return (
            <span className={item.type == "bold" ? " boldlistitem" : ""}>
                {item.name}
            </span>
        );
    }
}

DropDownListItem.propTypes = {
    item: React.PropTypes.object,
};