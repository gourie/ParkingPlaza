/*
*   Author: Joeri Nicolaes
*   ======================
*/

//import React from 'react';
import React from 'react';
import ReactDOM from 'react-dom';
import {Panel, Button, Input, ButtonInput, Carousel, CarouselItem, CarouselCaption} from 'react-bootstrap';
import {DropdownList} from 'react-widgets';
import HeaderApp from './HeaderApp';
import FooterApp from './FooterApp';
import EventParking from './Components/EventParking';

// Config for the app setup: TODO - retrieve from server
var config = {
  debug: true
};

/**
 * React Component: HomeApp
 */
//var HomeApp = React.createClass({
export default class HomeApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in HomeApp/constructor"); }
    super(props);
    // init state:
    // TODO: fetch dashboard items from server (now hard-coded)
    this.state = {
        parkingcapacity: 15,
        totalparkingsmonth: 120,
        parkingoverviewvisible: false,
        loggedIn: (this.props.loggedInAtStart == "true") ? true : false,
    };
    // catch bindings for click
    this.openEventPage = this.openEventPage.bind(this);
    this.changeLoggedIn = this.changeLoggedIn.bind(this);

  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in HomeApp/componentDidMount"); }

    //(this.props.loggedInAtStart == "true") ? this.setState({loggedIn: true}) : false;

  }

  /**
   * Method:
   *  - handle event panel click
   */
  handleEventPanelClick() {

    if (config.debug==true) { console.log("in HomeApp/handleEventPanelClick"); }

  }

  /**
   * Method:
   *  - handle city panel click
   */
  handleCityPanelClick() {

    if (config.debug==true) { console.log("in HomeApp/handleCityPanelClick"); }

  }

  /**
   * Method:
   *  - suggest Event
   */
  suggestPoI(value) {

    if (config.debug==true) { console.log("in HomeApp/suggestPoI", value); }

  }

  /**
   * Method:
   *  - open EventParking page with selected value when 'dropdownlist' has been selected.
   */
  openEventPage(value) {

    if (config.debug==true) { console.log("in HomeApp/openEventPage", value); }

    window.location.assign("/map?destination="+value);

  }

  /**
   * Changed loggedIn state - function passed to HeaderApp
   */
  changeLoggedIn(value) {

    if (config.debug==true) { console.log("in HomeApp/changeLoggedIn"); }

    if (value == "true") {
        this.setState({loggedIn: true});
    } else {
        this.setState({loggedIn: false});
    }

  }

  /**
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {

    if (config.debug==true) { console.log("in HomeApp/render"); }

    var PoiNames = this.props.availablePois.map(function(poi){
        return poi['poiname'];
    });
    var eventPoiNames = this.props.availablePois.filter(function(poi){
        if (poi['poitype'] == 'eventparking') { return true; }
        else { return false;}
    }).map(function(poi){
        return poi['poiname'];
    });
    var cityPoiNames = this.props.availablePois.filter(function(poi){
        if (poi['poitype'] == 'cityparking') { return true; }
        else { return false;}
    }).map(function(poi){
        return poi['poiname'];
    });

    return (
        <div className="homeApp">
            <HeaderApp userProps={this.props.userProps} poiTypes={this.props.availablePoiTypes} loggedIn={this.state.loggedIn} changeLoggedIn={this.changeLoggedIn}/>

            <div className="pane">
                <h3>Find a parking space near event</h3>
                <div className="row title-line">
                    <EventParking loggedIn={this.state.loggedIn} initialPoi={"List of available events"} availablePois={this.props.availablePois} config={config} reservationStatus={this.props.reservationStatus} linktodirections={this.props.linktodirections}/>
                </div>
            </div>
            <div className="pane-wide">
                <h3>How it works</h3>
                <Carousel className="home-carousel" interval={15000}>
                    <Carousel.Item>
                        <img className="carousel-img" alt="carousel" src="/images/carousel3.png"/>
                        <Carousel.Caption className="carousel-capt">
                            <h3 className="title-tag">How can I rent a parking?</h3>
                            <p>Once logged in, you can reserve a parking space upfront or instantly.</p>
                            <p>Tell us which event you want to visit: the system will automatically return one available parking nearby. </p>
                            <p>The parking will be reserved as soon as you have paid the due amount via secure online payment. </p>
                            <p>You will receive an invoice via email after successful payment. </p>
                        </Carousel.Caption>
                    </Carousel.Item>
                    <Carousel.Item>
                        <img className="carousel-img" alt="carousel" src="/images/carousel3.png"/>
                        <Carousel.Caption className="carousel-capt">
                            <h3 className="title-tag">Where does it work?</h3>
                            <p>The Parking Plaza platform has been launched as a pilot in Belgium.</p>
                            <p>Renters just need a car and an internet connection.</p>
                            <p>Owners can add their private parking place(s).</p>
                            <p>Parking Plaza will grow organically as new private parking spaces are added and new renters sign up.</p>
                        </Carousel.Caption>
                    </Carousel.Item>
                    <Carousel.Item>
                        <img className="carousel-img" alt="carousel" src="/images/carousel3.png"/>
                        <Carousel.Caption className="carousel-capt">
                            <h3 className="title-tag">How do I let my private parking?</h3>
                            <p>Once logged in, you can register your private parking in our system via the "Rent your private parking?" button at the <a href="#">top</a>.</p>
                            <p>Once your private parking is added to our system, you will receive a confirmation email.</p>
                            <p>The system will notify you a few days upfront via email every time an event nearby your parking is upcoming.</p>
                            <p>You decide for each event whether or not to let your private parking. </p>
                        </Carousel.Caption>
                    </Carousel.Item>
                    <Carousel.Item>
                        <img className="carousel-img" alt="carousel" src="/images/carousel3.png"/>
                        <Carousel.Caption className="carousel-capt">
                            <h3 className="title-tag">What happens behind the scenes?</h3>
                            <p>The Parking Plaza platform connects Owners who want to rent out their private parking with Renters looking for parking.</p>
                            <p>The Parking Plaza team makes sure all personal information, schedules and payments are handled safely and correctly. </p>
                        </Carousel.Caption>
                    </Carousel.Item>
                </Carousel>
            </div>
            { this.state.parkingoverviewvisible ?
                <div className="pane">
                    <h3>Who is using it?</h3>
                    <div className="row title-line">
                        <div className="col-md-5 col-md-offset-1 col-xs-3 col-xs-offset-3 panel-col">
                            <div className="title-line text-muted ">
                                <blockquote>
                                    <p className="text-right">Free parking Capacity</p>
                                    <footer className="text-right">The total number of available parkings hours from all owners</footer>
                                </blockquote>
                            </div>
                            <div className="title-line text-muted text-right metric-right">{this.state.parkingcapacity}</div>
                        </div>
                        <div className="col-md-5 col-xs-3">
                            <div className="title-line text-muted ">
                                <blockquote>
                                    <p className="text-left">Parkings last month</p>
                                    <footer className="text-left">The total number of parking hours from all renters during the previous month </footer>
                                </blockquote>
                            </div>
                            <div className="title-line text-muted text-left metric-left">{this.state.totalparkingsmonth}</div>
                        </div>
                    </div>
                </div>
            : null }
            <div className="pane">
                <h3>About us</h3>
                <div>
                    <div className="title-line text-muted">The Parking Plaza team are young Belgian entrepreneurs with a passion to solve problems with technology.</div>
                    <div className="title-line text-muted">We believe that it is a waste not to use resources to their full potential. </div>
                    <div className="title-line text-muted">So we made it our mission to find free capacity in existing private parking spaces and make them available for people who need for a parking.</div>
                    <div className="title-line text-muted">More details about our services can be found in <a href="/tos"> Terms of Service</a>. </div>
                </div>
            </div>
            <div className="footer">
                <FooterApp />
            </div>
        </div>
    );
  }
}

HomeApp.propTypes = {
    userProps: React.PropTypes.object,
    loggedInAtStart: React.PropTypes.string,
    availablePois: React.PropTypes.array,
    availablePoiTypes: React.PropTypes.array,
    reservationStatus: React.PropTypes.bool,
    linktodirections: React.PropTypes.string,
};

