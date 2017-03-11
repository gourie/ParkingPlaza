/*
*   Author: Joeri Nicolaes
*   ======================
*/

// Prep required for bundling all JS packages into one single bundle.js (done offline in DEV using Webpack)
// import react
import React from 'react';
import ReactDOM from 'react-dom';
import {Button, ButtonToolbar, DropdownButton, MenuItem, Modal, Overlay, OverlayTrigger, Tooltip} from 'react-bootstrap';
//var jquery = require('jquery');
import jquery from 'jquery';

// init widgets
import {DropdownList} from 'react-widgets';
import {DateTimePicker} from 'react-widgets';

//enable localizer (required for DateTime)
import Moment from 'moment';
import momentLocalizer from 'react-widgets/lib/localizers/moment';

momentLocalizer(Moment);

import HeaderApp from './HeaderApp';

// initialize Google Map Vars
var map;
var parkingMarker;
var destMarker;
var mapZoomLevel;
var cityGeoCode;
var mapBounds;

// Config for the app setup: TODO - retrieve from server
var config = {
  mapZoomLevel: 15,
  debug: true
};


/**
 * React Component: main app with state and UI functions for reservation of parking slot
 */
export default class ParkingMapApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in ParkingMapApp/constructor"); }
    super(props);
    // init state:
    // find poitype of the initialpoi
    var initPoi = this.props.initialPoi;
    var initPoiTypeState = this.props.availablePois.filter(function(poi){
        if (poi['poiname'] == initPoi) { return true; }
        else { return false;}
    }).map(function(poi){
        return poi['poitype'];
    });
    this.state = {
        showSearch: true,
        showParkingDetails: false,
        showReservation: this.props.reservationStatus,
        showHelp: true,
        // These will be updated when user clicks on the map (destination)
        lat: "",
        lon: "",
        // This will be updated when user selects search parameters (destination, parking start- and end-time)
        destination: this.props.initialPoi,
        startTime: new Date(),
        endTime: new Date(),
        eventList: this.props.eventList,
        selectedEvent: "",
        poitype: initPoiTypeState[0],
        // These will be updated with data from the API
        availableParkingSlot: {}, //assertion: one available parking slot expected from server
        center: {},
        // This will be updated in certain steps of workflow
        zoomLevel: config.mapZoomLevel,
        loggedIn: (this.props.loggedInAtStart == "true") ? true : false,
    };
    // catch bindings for click
    this.reserveParking = this.reserveParking.bind(this);
    this.renderMap = this.renderMap.bind(this);
    this.updateParkingSlotsOnMap = this.updateParkingSlotsOnMap.bind(this);
    this.updateAvailableParkingSlotState = this.updateAvailableParkingSlotState.bind(this);
    this.setPoi = this.setPoi.bind(this);
    this.selectEvent = this.selectEvent.bind(this);
    this.changeLoggedIn = this.changeLoggedIn.bind(this);
  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in ParkingMapApp/componentDidMount"); }

    //render new Map
    this.renderMap();
  }

  /**
   * Changed loggedIn state - function passed to HeaderApp
   */
  changeLoggedIn(value) {

    if (config.debug==true) { console.log("in EmailConfApp/changeLoggedIn"); }

    if (value == "true") {
        this.setState({loggedIn: true});
    } else {
        this.setState({loggedIn: false});
    }

  }

  /**
   * Method: fetch available parking slots from API
   * @lat: input from state; latitude of destination in decimal degrees (variable1 of destination requested by user)
   * @lon: input from state; longitude of destination in decimal degrees (variable2 of destination requested by user)
   * @startTime: input from state; start-time in JS data object (selected by user from TimeWidget)
   * @endTime: input from state; end-time in JS data object (selected by user from TimeWidget)
   * @data: output; parking slot with {id, lat, lon} that is available in the requested timeslot and nearest to the requested destination (server logic)
   */
  getAvailableParkingSlot(value) {
    if (config.debug == true) {
      console.log("in ParkingMapApp/getAvailableParkingSlot" + value);
    }

    if (this.state.poitype == "cityparking") { //city-parking
        //use HTTP POST (conform with REST API specs)
        var request = jquery.ajax({
          url: "/parkings/findAvailableParking",
          method: "POST",
          data: { poi: this.state.destination, lat: this.state.lat, lon: this.state.lon, startTime: this.state.startTime.toISOString(), endTime: this.state.endTime.toISOString()},
          dataType: "json"
        });
        return request;
    } else { //event-parking
        //use HTTP POST (conform with REST API specs)
        console.log(value);
        var request = jquery.ajax({
          url: "/parkings/findAvailableParking",
          method: "POST",
          data: { eventdescription: value['eventdescription'], eventstart: value['eventstart'] },
          dataType: "json"
        });
        return request;
    }
  }

  /**
   * Method: update React state with Parking slot received from server and set Boolean showParkingDetails true
   */
  updateAvailableParkingSlotState(value) {

    if (config.debug == true) {
      console.log("in ParkingMapApp/updateAvailableParkingSlotState");
    }

    this.getAvailableParkingSlot(value).then((function (data) {
      // Update the state, pass updateParkingSlotsOnMap as a callback
      //console.log(data);
      this.setState({
        //lat: lat,
        //lon: lon,
        // feed data received from server into state
        availableParkingSlot: data,
      }, this.updateParkingSlotsOnMap); /// Pass updateParkingSlotsOnMap as a callback
    }).bind(this));

  }

  /**
   * Method: render the map on page
   */
  renderMap() {

    if (config.debug == true) {
      console.log("in ParkingMapApp/renderMap");
    }

    var initPoi = this.props.initialPoi;
	var initCoord = this.props.availablePois.map(function(poi){
            if (poi['poiname'] == initPoi) {
                var lat = poi['poicenter']['lat']
                var lon = poi['poicenter']['lon']
                return {initialLat: lat, initialLon: lon};
            } else {
            //default to Belgium --TODO: fetch from server
                return {initialLat: "50.8482659", initialLon: "4.3911987", zoomLevel: "7"}
            }
    });
    this.setState({zoomLevel: initCoord[0].zoomLevel});

    //Google Maps options
    var mapOptions = {
      center: new google.maps.LatLng(initCoord[0].initialLat, initCoord[0].initialLon),
      zoom: this.state.zoomLevel
    };

    //Google maps variable, tied to map reference set in Render ('non-React style' but only option using Google Maps)
    map = new google.maps.Map(this.refs['map'], mapOptions);

    // Add an event listener for click to map
    google.maps.event.addListener(map, 'click', (function (event) {
      var latLng = event.latLng;
      var lat = latLng.lat();
      var lng = latLng.lng();

      // remove old marker if any
      if (this.state.lat !== "") {
        destMarker.setMap(null);
      }

      //change state of destination
      this.setState({lat: lat});
      this.setState({lon: lng});

      //create DestinationMarker based on new state and show on Map
      var dest = new google.maps.LatLng(this.state.lat, this.state.lon);
      destMarker = new google.maps.Marker({
        position: dest,
        map: map,
        title: "Where you want to go", //title appears as tooltip
        //image based icon
        //icon: image,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          strokeColor: 'red',
          scale: 3
        },
        draggable: false
      });
 
      //this.locationSearch();

      // Find available parking slots (based on new state (lat,lng) and (start-time,end-time) if available)
      this.updateAvailableParkingSlotState();
    }).bind(this));
  }

  /**
   * Method: update map with updated State
   */
  updateParkingSlotsOnMap() {

    if (config.debug == true) {
      console.log("in ParkingMapApp/updateParkingSlotsOnMap");
    }

    // remove old marker if any
    if (typeof parkingMarker != 'undefined') {
      parkingMarker.setMap(null);
    }

    // update marker on map if data fetched from server
    if (this.state.availableParkingSlot) {
        var latLng = new google.maps.LatLng(this.state.availableParkingSlot['lat'], this.state.availableParkingSlot['lon']);

        parkingMarker = new google.maps.Marker({
          position: latLng,
          map: map,
          title: this.state.availableParkingSlot['id'], //title appears as tooltip

          //image based icon
          //icon: image,
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            strokeColor: 'blue',
            scale: 3
          },
          draggable: false
        });
    }
    this.setState({showParkingDetails: true});

    //if you GB is shown, zoom-in --DISABLED: user can zoom manually (bug not showing correctly)
//    if (this.state.showParkingDetails == true) {
//      mapBounds = map.getBounds();
//      //console.log(map.getBounds());
//      map.setZoom(16);
//    }
  }

  /**
   * Method: 
   *  - update state for start- or end-time when 'timeWidget' has been changed.
   *  - if start-time has been changed, automatically update end-time with same date (to increase UX)
   */
  changeTime(name, value) {
    
    if (config.debug==true) { console.log("in ParkingMapApp/changeTime", name); }
    //console.log(typeof value, value);
    
    this.setState({ [name+"Time"] : value});

    //pre-populate end-time date to speed-up entry
    if (name == 'start') {
      this.setState({endTime: value});
    }
  }

  /**
   * Method: 
   *  - call server API /parkings/reserveParking to reserve parking with given ID
   *  - change UI after API call (success, failure)
   */
  reserveParking() {

    if (config.debug == true) {
      console.log("in ParkingMapApp/reserveParking");
    }

    //Step1: (conform REST API) POST method to call API Controller resource
    jquery.ajax({
      url: "/parkings/reserveParking",
      method: "POST",
      data: { id: this.state.availableParkingSlot['id'], startTime: this.state.startTime.toISOString(), endTime: this.state.endTime.toISOString() },
      dataType: "json",
      //Step2: change UI
      success: function(data) {
        console.log(data);
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
   *  - update state of destination & change center when 'dropdownlist' has been selected.
   */
  setPoi(value) {

    if (config.debug==true) { console.log("in ParkingMapApp/setPoi", value); }
    //console.log(typeof value, value);

    this.setState({destination: value});

    //update state of poitype by finding poitype of the selected poi
    var newState = this.props.availablePois.filter(function(poi){
        if (poi['poiname'] == value) { return true; }
        else { return false;}
    }).map(function(poi){
        return poi['poitype'];
    });
    this.setState({poitype: newState[0]});

    //change center of map
    var lat;
    var lng;
    for (var i=0; i < this.props.availablePois.length; i++) {
        if (this.props.availablePois[i]['poiname'] == value) {
            lat = this.props.availablePois[i]['poicenter']['lat'];
            lng = this.props.availablePois[i]['poicenter']['lon'];
            break;
        }
    }

    var poiLatLng = new google.maps.LatLng(lat,lng);
    map.setCenter(poiLatLng);

    //for new poitype state eventparking:
    //fetch latest eventList and update state
    if (newState[0] == 'eventparking') {
        jquery.ajax({
          url: "/parkings/findAvailableEventParking",
          method: "POST",
          data: { poifname: value },
          dataType: "json",
          //Step2: change UI
          success: function(data) {
            console.log(data);
            this.setState({ eventList: data });
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    }

  }

  /**
   * Method:
   *  - act upon selection of event from dropdownlist.
   */
  selectEvent(value) {

    if (config.debug==true) { console.log("in ParkingMapApp/selectEvent", value); }
    //console.log(typeof value, value);

    this.setState({ selectedEvent : value});
    // re-init starttime and endtime variables
    this.setState({ startTime: new Date() });
    this.setState({ endTime: new Date() });

    // Find available parking slots (based on selectedevent) - if available
    var pos = value.search(/:/);
    var index = value.substring(0,pos);
    var test = this.state.eventList[index-1];
    console.log(test);
    this.updateAvailableParkingSlotState(test);

  }

  /**
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {
		if (config.debug==true) { console.log("in ParkingMapApp/render"); }
		let closeReserveParkingModal = () => this.setState({ showParkingDetails: false});
		let closeReservation = () => this.setState({ showReservation: false});
		let close = () => this.setState({ showParkingDetails: false});


		var PoiNames = this.props.availablePois.map(function(poi){
            return poi['poiname'];
        });

        var i=0;
		var eventDropDownList = this.state.eventList.map(function(event){
		    i+=1;
            return i + ': ' + new Date(event['eventstart']).toDateString() + ' ' + new Date(event['eventstart']).toLocaleTimeString() + '    ' + event['eventdescription']  + ' (' + event['eventcapacity'] + ')'
        });

    return (
      <div className="parkingApp">
          <HeaderApp userProps={this.props.userProps} poiTypes={this.props.availablePoiTypes} loggedIn={this.state.loggedIn} changeLoggedIn={this.changeLoggedIn}/>
          <div className="map-tagline">
                <h2 className="map-title">The Parking Community</h2>
          </div>
          <div className="map-pane">
            <div className="container">
              <div className="row">
                { this.state.showSearch ? <div className="panel-body">
                  { /* Search Fields  - destination, start time and end-time */ }
                  <div className="form-group col-md-4 col-xs-12">
                    <label className="form-label map-text">Point of Interest</label>
                    <div className="rw-widget">
                        <DropdownList ref="dropdown" placeholder={this.props.initialPoi} data={PoiNames} onChange={this.setPoi} />
                    </div>
                  </div>
                  { (this.state.poitype == "cityparking") ?
                      <div>
                          <div className="col-md-4 col-xs-12">
                              <label className="form-label map-text">Start-time</label>
                          <div className="rw-widget" id="startTimePicker">
                              <DateTimePicker value={this.state.startTime} step={60} onChange={this.changeTime.bind(this, 'start')} />
                            </div>
                          </div>
                          <div className="col-md-4 col-xs-12">
                              <label className="form-label map-text">End-time</label>
                          <div className="rw-widget">
                              <DateTimePicker value={this.state.endTime} step={60} onChange={this.changeTime.bind(this, 'end')} />
                            </div>
                          </div>
                      </div>
                  :
                      <div>
                        <div className="col-md-8 col-xs-12">
                            { (eventDropDownList.length == 0) ?
                                <div>
                                    <p className="map-text"> No events with parking capacity available. </p>
                                </div>
                              :
                                <div class="form-group">
                                    <label className="form-label map-text">Event (parking capacity)</label>
                                    <div className="rw-widget">
                                        <DropdownList ref="dropdownEvent" placeholder={"Select event to find parking"} data={eventDropDownList} onSelect={this.selectEvent} />
                                    </div>
                                </div>
                              }
                        </div>
                      </div>
                  }
                </div> : null }
              </div>
              <Modal
                show={this.state.showParkingDetails}
                onHide={closeReserveParkingModal}
              >
                <Modal.Header closeButton>
                  <Modal.Title>Confirm your parking</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    { this.state.availableParkingSlot ?
                    <div>
                        <div className="row">
                            <div className="col-md-12 col-xs-12">
                                <p>Placeholder for T&C of Reservation</p>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-md-4 col-xs-4">
                              <p className="text-muted"><strong>Parking id</strong> {this.state.availableParkingSlot['id']}</p>
                            </div>
                            <div className="col-md-4 col-xs-6">
                              <p className="text-muted"><strong>Parking price</strong> {this.state.availableParkingSlot['price']}</p>
                            </div>
                            <div className="col-md-4 col-xs-6">
                              <Button onClick={this.reserveParking} className="btn btn-primary" id="reservationButton" data-toggle="tooltip" title="Click this button to book your Parking.">Pay</Button>
                            </div>
                        </div>
                    </div> :
                    <div>
                       <p>There is no parking unit available. Please try again by changing your inputs.</p>
                       <p><strong>Hint:</strong> this prototype has slots available on May 11 between 9h and 17h</p>
                    </div>
                     }
                </Modal.Body>
                <Modal.Footer>
                  <Button onClick={closeReserveParkingModal}>Cancel</Button>
                </Modal.Footer>
              </Modal>

              <Modal
                show={this.state.showReservation}
                onHide={closeReservation}
              >
                <Modal.Header closeButton>
                  <Modal.Title>Reservation confirmed</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    { this.state.availableParkingSlot ?
                    <div>
                        <p>We received your payment of {this.state.availableParkingSlot['price']}.</p>
                        <p>Thanks for reserving <strong>Parking {this.state.availableParkingSlot['id']}</strong>!</p>
                        <p>Placeholder for Reservation confirmation text (legal stuff)</p>
                    </div>
                    : null }
                </Modal.Body>
                <Modal.Footer>
                  <Button onClick={closeReservation}>Close</Button>
                </Modal.Footer>
              </Modal>

            </div>
          </div>
          <div id="mapCanvas" ref="map">
          </div>
      </div>
		);
  }
}

ParkingMapApp.propTypes = {
    userProps: React.PropTypes.object,
    loggedInAtStart: React.PropTypes.string,
    availablePois: React.PropTypes.array,
    availablePoiTypes: React.PropTypes.array,
    initialPoi: React.PropTypes.string,
    eventList: React.PropTypes.array
};