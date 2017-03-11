/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import ScheduleItem from './ScheduleItem';
import ListHeader from './ListHeader';
import ListFooter from './ListFooter';
import FooterApp from '../FooterApp';
import HeaderApp from '../HeaderApp';

/**
 * React Component: ParkingList
 */
export default class ParkingList extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in ParkingList/constructor"); }

        this.state = {
            loggedIn: (this.props.loggedInAtStart == "true") ? true : false,
        };

        this.changeLoggedIn = this.changeLoggedIn.bind(this);

    }

    /**
     * Standard React method: runs after initial render
     */
    componentDidMount() {

        if (this.props.config.debug==true) { console.log("in ParkingList/componentDidMount"); }
    }

   /**
    * Changed loggedIn state - function passed to HeaderApp
    */
   changeLoggedIn(value) {

        if (this.props.config.debug==true) { console.log("in EmailConfApp/changeLoggedIn"); }

        if (value == "true") {
            this.setState({loggedIn: true});
        } else {
            this.setState({loggedIn: false});
        }

   }

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in ParkingList/render"); }

        var schedules = this.props.schedules;

        var scheduleCount = schedules.reduce(function(accum, schedule) {
				return schedule.future ? accum : accum + 1;
			}, 0);
	    var itemChanged = false;
        var scheduleItems = schedules.map(function(item) {
            item.eventstart = new Date(item.eventstart).toDateString() + ' ' + new Date(item.eventstart).toLocaleTimeString();
            if (item.changed == "true") {
                itemChanged = true;
            }
            return (
                <ScheduleItem
                    key={item.eventstart}
                    item={item}
                />
            );
		});

        return (

            <div className="homeApp">
                <HeaderApp userProps={this.props.userProps} poiTypes={this.props.availablePoiTypes} loggedIn={this.state.loggedIn} changeLoggedIn={this.changeLoggedIn}/>
                { this.state.loggedIn ?
                    <div className="pane-wide schedule">
                        <h3>Your Parking Schedule</h3>
                        { this.props.userProps.ownerYesNo ?
                            <div>
                                <div className="title-line">
                                    { scheduleCount != 0 ?
                                        <div>
                                            { itemChanged ? <div>Thanks for updating the parking schedule marked in blue. </div> : null}
                                            <p>Here is an overview of your parking unit's availability.</p>
                                            <p>If you would like to update your parking schedule, please contact us via <a href="mailto:support@parking-plaza.com?Subject=Update%20Parking%20Schedule">email</a>.</p>
                                        </div>
                                    :
                                        <div>Your parking unit has no future available schedules set.</div>
                                    }
                                </div>
                                <div className="container parkinglist">
                                    <div className="header row">
                                         <span>Schedule for parking at {this.props.unitaddress}</span>
                                    </div>
                                    <ListHeader config={this.props.config} />
                                    {scheduleItems}
                                    <ListFooter config={this.props.config} count={scheduleCount} nowShowing={this.props.viewfilter.type}/>
                                </div>
                            </div>
                        : <div className="title-line">
                                You don't have any parking units yet registered in our system. Please add parking first and then set your schedule!
                           </div>
                        }
                    </div>
                :
                    <div className="pane-wide schedule">
                        <p className="text-muted alertmessage"> Please log in first to see your parking schedule. </p>
                    </div>
                }
                <div className="footer schedule">
                    <FooterApp />
                </div>
            </div>
        );
    }

}

ParkingList.propTypes = {
    unitaddress: React.PropTypes.string,
    schedules: React.PropTypes.array,
    viewfilter: React.PropTypes.object,
    config: React.PropTypes.object,
    userProps: React.PropTypes.object,
    loggedInAtStart: React.PropTypes.string,
    availablePois: React.PropTypes.array,
    availablePoiTypes: React.PropTypes.array,
};