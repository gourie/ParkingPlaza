/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import {DropdownList} from 'react-widgets';
import jquery from 'jquery';
import React from 'react';
import ShowParkingDetailsModal from './ShowParkingDetailsModal';
import ShowReservationModal from './ShowReservationModal';
import ShowSuggestLocationModal from './ShowSuggestLocationModal';
import DropDownListItem from './DropDownListItem';

/**
 * React Component: ListHeader
 */
export default class EventParking extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);
        // find poitype of the initialpoi
        this.state = {
            showParkingDetails: false,
            showReservation: this.props.reservationStatus,
            showSuggestLocation: false,
            suggestLocationSuccess: false,
            selectedPoi: "",
            selectedEventindex: "",
            availableParkingSlot: {},
            eventList: [],

        };
        // catch bindings for click
        this.setPoi = this.setPoi.bind(this);
        this.selectEvent = this.selectEvent.bind(this);
        this.hide = this.hide.bind(this);
        this.reserveParking = this.reserveParking.bind(this);
        this.resetScheduleState = this.resetScheduleState.bind(this);
        this.suggestLocation = this.suggestLocation.bind(this);

        if (this.props.config.debug==true) { console.log("in EventParking/constructor"); }

    }

    /**
    * Standard React method: runs after initial render
    */
    componentDidMount() {

        if (this.props.config.debug==true) { console.log("in EventParking/componentDidMount"); }
        this.setPoi(this.props.initialPoi);

    }

    /**
     * Hide given modal (parking or reservation)
     */
    hide(modal) {

        if (this.props.config.debug==true) { console.log("in EventParking/hide", modal); }

        if (modal=='parking') {
            this.setState({ showParkingDetails: false });
            this.resetScheduleState();
        } else if (modal=='reservation') {
            this.setState({ showReservation: false });
        } else if (modal=='location') {
            this.setState({ showSuggestLocation: false });
        }
        //this.forceUpdate();
    }

    /**
    * Method:
    *  - reset schedule state for the availableParkingSlot (user aborted the reservation workflow)
    */
    resetScheduleState() {

        if (this.props.config.debug==true) { console.log("in EventParking/resetScheduleState"); }

        if (this.props.loggedIn) {
            jquery.ajax({
                url: "/parkings/resetSchedulestate",
                method: "POST",
                data: { eventdescription: this.state.eventList[this.state.selectedEventindex]['eventdescription'] },
                dataType: "json",
                success: function(data) {
                    console.log(data);
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                }.bind(this)
            });
        }
    }

    /**
    * Method:
    *  - update state for selected Poi
    */
    setPoi(value) {

        if (this.props.config.debug==true) { console.log("in EventParking/setPoi", value.name); }
        this.setState({ selectedPoi: value.name });

        if (value != "List of available events") {
            // catch suggest location
            if (value.name == 'Suggest Location') {
                console.log('suggest location selected')
                this.setState({ showSuggestLocation : true });
            } else {
                jquery.ajax({
                    url: "/parkings/findAvailableEventParking",
                    method: "POST",
                    data: { poifname: value.name },
                    dataType: "json",
                    //Step2: change UI
                    success: function(data) {
                    //console.log(data);
                    this.setState({ eventList: data });
                    }.bind(this),
                    error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                    }.bind(this)
                });
            }
        }

    }

    /**
    * Method:
    *  - act upon selection of event from dropdownlist.
    */
    selectEvent(value) {

        if (this.props.config.debug==true) { console.log("in EventParking/selectEvent", value); }

        if (this.props.loggedIn) {

            // Find available parking slots (based on selectedevent) - if available
            var index = value.substring(0,value.search(/:/));
            this.setState({ selectedEventindex : index-1});

            jquery.ajax({
              url: "/parkings/findAvailableParking",
              method: "POST",
              data: { eventdescription: this.state.eventList[index-1]['eventdescription'], eventstart: this.state.eventList[index-1]['eventstart'] },
              dataType: "json",
              //Step2: change UI
              success: function(data) {
                //console.log(data);
                if (data == "invalid") {
                    this.setState({ availableParkingSlot: {} });
                } else {
                    this.setState({ availableParkingSlot: data });
                }
              }.bind(this),
              error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
              }.bind(this)
            });

        } else {
            this.setState({ availableParkingSlot: {} });
        }

        this.setState({ showParkingDetails : true });

    }

    /**
    * Method:
    *  - call server API /parkings/reserveParking to reserve parking with given ID
    *  - change UI after API call (success, failure)
    */
    reserveParking() {

        if (this.props.config.debug == true) {
          console.log("in EventParking/reserveParking");
        }

        //Step1: (conform REST API) POST method to call API Controller resource
        jquery.ajax({
          url: "/parkings/reserveParking",
          method: "POST",
          data: { id: this.state.availableParkingSlot['id'], eventdescription: this.state.eventList[this.state.selectedEventindex]['eventdescription']},
          dataType: "json",
          //Step2: change UI
          success: function(data) {
            //console.log(data);
            if(data.startsWith("https://")){
                    window.location.replace(data);
                    console.log("in data.startswith")
                    //redirect towards url provided via data
            }
            else {
                    alert('feedback server:' + data);
                    console.log("in else of data.startswith")
            }
            //TODO: add errorhandling (catch 'errors' and if adapt UI it different feedback)
            //this.setState({ showParkingDetails: false });
            //this.setState({ showReservation: true });
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });

        //Step3: visually indicate to user that he/she has a reservation
        //STUB: add small icon??
    }

    /**
    * Method:
    *  - call server API /parkings/suggestLocation to suggest a new location
    *  - change UI after API call (success, failure)
    */
    suggestLocation (value) {

        if (this.props.config.debug == true) {
          console.log("in EventParking/suggestLocation", value);
        }

        //reset success flag
        this.setState({ suggestLocationSuccess : false });

        //Step1: (conform REST API) POST method to call API Controller resource
        jquery.ajax({
          url: "/parkings/suggestLocation",
          method: "POST",
          data: { location: JSON.stringify(value.location), email: value.emailaddress},
          dataType: "json",
          //Step2: change UI
          success: function(data) {
            this.setState({ suggestLocationSuccess : true });
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });

    }

    /**
     * Standard React method: render
     */
    render() {

		var PoiNames = this.props.availablePois.map(function(poi){
            return poi['poiname'];
        });
        // add suggest location option that triggers modal when clicked
        PoiNames.push('Suggest Location');

        var poinames = this.props.availablePois.map(function(poi){
            return {'name': poi['poiname'], 'type': ''};
        });
        // add suggest location option that triggers modal when clicked
        poinames.push({'name' : 'Suggest Location', 'type' : 'bold'});

        var i=0;
        // var text = 'SOLD OUT';
		var eventDropDownList = this.state.eventList.map(function(event){
		    i+=1;
		    if (event['eventcapacity'] == 0) {
		        // return i + ': ' + new Date(event['eventstart']).toDateString() + ' ' + new Date(event['eventstart']).toLocaleTimeString() + '    ' + event['eventdescription'] + ' ' + text
		        return i + ': ' + new Date(event['eventstart']).toDateString() + ' ' + new Date(event['eventstart']).toLocaleTimeString() + '    ' + event['eventdescription']
		    } else {
                return i + ': ' + new Date(event['eventstart']).toDateString() + ' ' + new Date(event['eventstart']).toLocaleTimeString() + '    ' + event['eventdescription']
            }
        });

        return (
            <div>
                <div className="row">
                    <div className="form-group col-md-4 col-xs-12">
                        <label className="form-label text-muted">Where do you want to go?</label>
                        <div className="rw-widget">
                            <DropdownList ref="dropdown" placeholder={this.props.initialPoi} data={poinames} textField='name' itemComponent={DropDownListItem} onChange={this.setPoi} />
                        </div>
                    </div>
                    <div className="col-md-8 col-xs-12">
                        { (eventDropDownList.length == 0) ?
                            <div>
                                <p className="text-muted"> No events with parking capacity available. </p>
                            </div>
                          :
                            <div class="form-group">
                                <label className="form-label text-muted">Event</label>
                                <div className="rw-widget">
                                    <DropdownList ref="dropdownEvent" placeholder={"Select event to find parking"} data={eventDropDownList} onSelect={this.selectEvent} />
                                </div>
                            </div>
                          }
                    </div>
                </div>
                <ShowParkingDetailsModal config={this.props.config} hide={this.hide} show={this.state.showParkingDetails} availableParkingSlot={this.state.availableParkingSlot} reserveParking={this.reserveParking} loggedIn={this.props.loggedIn}/>
                <ShowReservationModal config={this.props.config} hide={this.hide} show={this.state.showReservation} availableParkingSlot={this.state.availableParkingSlot} linktodirections={this.props.linktodirections}/>
                <ShowSuggestLocationModal config={this.props.config} hide={this.hide} show={this.state.showSuggestLocation} successFlag={this.state.suggestLocationSuccess} suggestLocation={this.suggestLocation} loggedIn={this.props.loggedIn}/>
            </div>
        );
    }
}

EventParking.propTypes = {
    loggedIn: React.PropTypes.bool,
    initialPoi: React.PropTypes.string,
    availablePois: React.PropTypes.array,
    config: React.PropTypes.object,
    reservationStatus: React.PropTypes.bool,
    linktodirections: React.PropTypes.string,
};