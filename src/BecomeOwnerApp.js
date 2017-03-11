/*
*   Author: Joeri Nicolaes
*   ======================
*/

// import react
//import React from 'react';
import React from 'react';
import jquery from 'jquery';
import {Button, Input} from 'react-bootstrap';
import {DropdownList} from 'react-widgets';
import GooglePlacesSuggest from 'react-google-places-suggest';

import EmailSignup from './Components/EmailSignup';

// Config for the app setup: TODO - retrieve from server
var config = {
  debug: true
};

/**
 * React Component: BecomeOwnerAp
 */
//module.exports = React.createClass({
export default class BecomeOwnerApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in BecomeOwnerApp/constructor"); }
    super(props);
    // init state
    this.state = {
        addUnitSuccess: false,
        alertAfterAddUnit: false,
        isOwner: this.props.userProps['ownerYesNo'],
        parkingLocation: "",
        search: "",
        selectedCoordinate: null,
        parkingTypeSelected: this.props.poiTypes[0],
        toschecked: false,
        forgottochecktos: false,
    };
    // catch bindings for click
//    handleSelectSuggest = handleSelectSuggest.bind(this);
//    handleSearchChange = handleSearchChange.bind(this);
//    selectParkingType = selectParkingType.bind(this);
//    setParkingLocation = setParkingLocation.bind(this);
    this.becomeOwnerFunction = this.becomeOwnerFunction.bind(this);
    this.setToscheckbox = this.setToscheckbox.bind(this);
    this.becomeowneruserprops = this.becomeowneruserprops.bind(this);
  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in BecomeOwnerApp/componentDidMount"); }
    //(this.props.language != "") ? this.setState({showLanguage: this.props.language}) : false;
  }

  /**
   * Method:
   *  - send owner details
   *    TEMP: just alert that this feature is not yet ready
   */
  becomeOwnerFunction() {

    if (config.debug==true) { console.log("in BecomeOwnerApp/becomeOwnerFunction"); }

    this.setState({ forgottochecktos: false});

    if (this.state.isOwner==true) {
        jquery.ajax({
          //Step1: (conform REST API) POST method
          url: "/parkings/add",
          method: "POST",
          // Simplified within #62 to remove parking type from UI!!
          // data: { parkingtype: this.state.parkingTypeSelected, unitaddress: JSON.stringify(this.state.selectedCoordinate) },
          data: { unitaddress: JSON.stringify(this.state.selectedCoordinate) },
          dataType: "json",
          //Step2: change UI
          success: function(data) {
            this.setState({ addUnitSuccess: data});
            if (data == false) { this.setState({ alertAfterAddUnit: true}); }
            console.log(data);
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    } else {
      //new owner
      if (this.state.toschecked) {
        jquery.ajax({
            //Step1: (conform REST API) POST method
            url: "/parkings/add",
            method: "POST",
            // Simplified within #62 to remove parking type from UI!!
            // data: { parkingtype: this.state.parkingTypeSelected, unitaddress: JSON.stringify(this.state.selectedCoordinate), ownerbankaccount: this.refs.ownerbankaccount.getValue(), ownermobile: this.refs.ownermobile.getValue()},
            // data: { unitaddress: JSON.stringify(this.state.selectedCoordinate), ownerbankaccount: this.refs.ownerbankaccount.getValue(), ownermobile: this.refs.ownermobile.getValue()},
            data: { unitaddress: JSON.stringify(this.state.selectedCoordinate)},
            dataType: "json",
            //Step2: change UI
            success: function(data) {
                this.setState({ addUnitSuccess: data });
                this.setState({ isOwner: data });
                if (data == false) { this.setState({ alertAfterAddUnit: true}); }
                console.log(data);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
      } else {
        this.setState({ forgottochecktos: true });
      }
    }
  }

  /**
   * Method:
   *  - change toscheckbox setting
   */
  setToscheckbox() {

    if (config.debug==true) { console.log("in BecomeOwnerApp/setToscheckbox"); }

    if (this.state.toschecked)
    {
        //unchecked
        this.setState({toschecked: false});

    }
    else
    {
        //checked
        this.setState({toschecked: true});
        this.setState({ forgottochecktos: false });
    }
  }

  becomeowneruserprops(value) {

    if (config.debug==true) { console.log("in BecomeOwnerApp/setUserProps", value); }

    this.props.becomeownersetuserprops(value);

  }

  /**
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {
    if (config.debug==true) { console.log("in BecomeOwnerApp/render"); }
    let selectParkingType = (value) => this.setState({ parkingTypeSelected: value});
    let setParkingLocation = (value) => this.setState({ parkingLocation: value});

    /**
      * GooglePlacesSuggest handler method
      */
    const { search } = this.state
    let handleSearchChange = (e) => this.setState({ search: e.target.value });
    let handleSelectSuggest = (suggestName, coordinate) => this.setState({ search: suggestName, selectedCoordinate: coordinate });

    return (
        <div>
            { !this.state.addUnitSuccess ?
                <div className="row ownermodal">
                    Hello <b>{this.props.userProps['userName']}</b>,
                </div>
            : null }
            { !this.state.isOwner?
                <div>
                    <div className="row ownermodal">
                        Great, you own a private parking space and are interested to rent it on Parking Plaza when you don't use it!
                    </div>
                    <div className="row ownermodal">
                        You will always be in control of your parking: once your parking is added, you tell us whether your parking can be let or not. By default, your parking is <strong>not</strong> available for rent.
                    </div>
                    <div className="row ownermodal linebelow">
                        How much can you earn? We estimate that if your parking is nearby an event location with regular visitors, you can earn from 50 to 150euro yearly.
                    </div>
                    { !this.props.loggedIn ?
                        <div className="row ownermodal lineabove">
                            <div className="row ownermodal">
                                <strong>Step 1</strong>
                            </div>
                            <EmailSignup config={config} setUserProps={this.becomeowneruserprops} />
                            <div className="row ownermodal linebelow"></div>
                            <div className="row ownermodal">
                                <strong>Step 2</strong>
                            </div>
                        </div>
                    : null }

                    <div className="row ownermodal lineabove">
                        Please complete the address of your private parking below.
                    </div>
                    <div className="row ownermodal">
                        We will then set the price of your parking and start reaching out to visitors who would be interested to use it.
                    </div>
                </div>
            : null }
            { (this.state.isOwner && !this.state.addUnitSuccess) ?
                    <div>
                        <div className="row ownermodal">
                            Great, you want to add another private parking!
                        </div>
                    </div>
            : null }
            { !this.state.addUnitSuccess ?
                <div>
                    <div className="row">
                        <div className="col-md-12 col-xs-12">
                              <span>Parking address: </span>
                              <GooglePlacesSuggest onSelectSuggest={ handleSelectSuggest.bind(this) } search={ this.state.search }>
                                <input
                                  type="text"
                                  value={ this.state.search }
                                  placeholder="Enter the full address of your parking"
                                  onChange={ handleSearchChange.bind(this) }
                                />
                              </GooglePlacesSuggest>
                        </div>
                    </div>
                    <div className="ownermodal">
                        { this.state.forgottochecktos ?
                              <div className="alertmessage">
                                Please tick Terms of Service checkbox!
                              </div>
                        : null }
                        { (!this.state.isOwner)?
                            <div>
                                <div className="checkbox">
                                    <label>
                                      <input type="checkbox" ref="toscheckbox" className="tosbox" checked={this.state.toschecked} onChange={this.setToscheckbox} /> I accept the <a href="/tos"> Terms of Service</a>.
                                    </label>
                                </div>
                            </div>
                        : null }
                    </div>
                    <div className="ownermodal">
                        <Button onClick={this.becomeOwnerFunction}>Continue</Button>
                    </div>
                    { this.state.alertAfterAddUnit ?
                        <div className="modaltext">
                            <b>The address you entered is incorrect, please verify and try again.</b>
                        </div>
                    : null }
                </div>
            :
                <div>
                    { this.state.addUnitSuccess == "no-poi" ?
                        <div>
                            <div className="row ownermodal">
                                Congratulations: your private parking space is one of the first in your neighbourhood that has been added to our system!
                            </div>
                            <div className="row ownermodal">
                                The Parking Plaza team will now do some market research to set the price of your parking and reach out to potential renters.
                            </div>
                            <div className="row ownermodal">
                                Within a few days, you will receive a confirmation email once this activation step has been completed and your parking is ready to use!
                            </div>
                            <div className="row ownermodal">
                                If you have any further questions please contact us via <a href="mailto:support@parking-plaza.com?Subject=Info%20Required%20After%20ParkingSpaceListing">email</a> or <a href="https://www.facebook.com/untappedparkingplaza" target="_blank">Facebook</a>.
                            </div>
                        </div>
                    :
                        <div>
                            <div className="row ownermodal">
                                Congratulations: your private parking space has been successfully added to our system!
                            </div>
                            <div className="row ownermodal">
                                Now it's up to you to tell us when your parking is available! By default, your parking is <strong>not</strong> available for rent.
                                The system will notify you a few days upfront via email every time an event nearby your parking is upcoming.
                            </div>
                            <div className="row ownermodal">
                                You will receive a confirmation email with more details in a few moments.
                                If you have any further questions please contact us via <a href="mailto:support@parking-plaza.com?Subject=Info%20Required%20After%20ParkingSpaceListing">email</a> or <a href="https://www.facebook.com/untappedparkingplaza" target="_blank">Facebook</a>.
                            </div>

                        </div>
                    }
                </div>
            }
        </div>
    );
  }
}

BecomeOwnerApp.propTypes = {
    userProps: React.PropTypes.object,
    poiTypes: React.PropTypes.array,
    loggedIn: React.PropTypes.bool,
};

