/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

// import react
//import React from 'react';
import React from 'react';
//import 'react-widgets/lib/less/react-widgets.less';
import {Button, ButtonToolbar, Dropdown, MenuItem, Modal, Glyphicon, Input, OverlayTrigger, Popover} from 'react-bootstrap';
import jquery from 'jquery';

import BecomeOwnerApp from './BecomeOwnerApp';

// init widgets
import DatePicker from 'react-datepicker';
import moment from 'moment';

// Config for the app setup TODO - retrieve from server
var config = {
  debug: true
};

/**
 * React Component: HeaderApp
 */
//module.exports = React.createClass({
export default class HeaderApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in HeaderApp/constructor"); }
    super(props);
    // init state
    this.state = {
        showBecomeOwnerModal: false,
        showSignupModal: false,
        showLoginModal: false,
        showImage: true,
        reservations: [],
        showReservationsModal: false,
        myaccountinfo:{},
        showMyAccountModal: false,
        showEmailSignupModal: false,
        emailSignupPending: false,
        showSignupSuccessModal: false,
        myParkings: [],
        showMyParkingsModal: false,
        birthDay: moment(),
        toschecked: false,
        firstname: "",
        lastname: "",
        email: "",
        showEmailLoginModal: false,
        userProps: this.props.userProps,
        wrongPassword: false,
        wrongEmail: false,
        invalidSignupEmail: false,
        askPasswordConfirmation: false,
        wrongSignupPassword: false,
        signupPasswordMatch: false,
        showLoginPassword: false,
        showSignupPassword: false,
        notEmailLoginUser: false,
    };

    // catch bindings for click
    this.loginWithEmail = this.loginWithEmail.bind(this);
    this.newUserWithEmail = this.newUserWithEmail.bind(this);
    this.setemail = this.setemail.bind(this);
    this.confirmpassword = this.confirmpassword.bind(this);
    this.passwordVisibilitySignup = this.passwordVisibilitySignup.bind(this);
    this.changeBirthday = this.changeBirthday.bind(this);
    this.loginKeyPressed = this.loginKeyPressed.bind(this);
    this.passwordVisibility = this.passwordVisibility.bind(this);
    this.showAccount = this.showAccount.bind(this);
    this.getReservations = this.getReservations.bind(this);
    this.getParkings = this.getParkings.bind(this);
    this.logout = this.logout.bind(this);
    this.setToscheckbox = this.setToscheckbox.bind(this);
    this.closeSignupSuccessModal = this.closeSignupSuccessModal.bind(this);
    this.openLoginModalFromBecomeOwnerModal = this.openLoginModalFromBecomeOwnerModal.bind(this);
    this.openSignupModalFromBecomeOwnerModal = this.openSignupModalFromBecomeOwnerModal.bind(this);
    this.setUserProps = this.setUserProps.bind(this);
  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in HeaderApp/componentDidMount"); }

  }

  /**
   * Method:
   *  - fetch and show reservations for given user
   */
  getReservations() {

    if (config.debug==true) { console.log("in HeaderApp/getReservations"); }

    //Step1: (conform REST API) GET method to call API Collection resource
    jquery.ajax({
      url: "/reservations",
      method: "GET",
      //data: { lat: this.state.lat, lon: this.state.lon, startTime: this.state.startTime.toISOString(), endTime: this.state.endTime.toISOString()},
      dataType: "json",
      //Step2: change UI
      success: function(data) {
        this.setState({ reservations: data });
        this.setState({ showReservationsModal: true});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });

  }

  /**
   * Method:
   *  - fetch and show parkings for given user
   */
  getParkings() {

      if (config.debug==true) { console.log("in HeaderApp/getParkings"); }
        jquery.ajax({
        url: "/myparkings",
        method: "GET",
        dataType: "json",
        //Step2: change UI
        success: function(data) {
            this.setState({ myParkings: data });
            this.setState({ showMyParkingsModal: true });
        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
  }

  /**
   * Method:
   *  - logout given user
   */
  logout() {

    if (config.debug==true) { console.log("in HeaderApp/logout"); }
    this.props.changeLoggedIn('false');
    this.setState({ userProps: {} });

    //this.forceUpdate();
  }

  /**
   * Method:
   *  - fetch and show account settings for given user
   *    TEMP: just alert that this feature is not yet ready
   */
  showAccount() {
    //alert("this feature is not ready yet");
    if (config.debug==true) { console.log("in HeaderApp/showAccount"); }

    //Step1: (conform REST API) GET method to call API Collection resource
    jquery.ajax({
        url: "/AccountInfo",
        method: "GET",
        dataType: "json",
        //Step2: change UI
        success: function(data) {
            this.setState({ myaccountinfo: data });
            this.setState({ showMyAccountModal: true});
        }.bind(this),
        error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
        }.bind(this)
    });
  }

  /**
   * Method:
   *  - change Birthday set by user
   */
  changeBirthday(value) {

    if (config.debug==true) { console.log("in HeaderApp/changeBirthday"); }
    this.setState({ birthDay: value});
  }

  /**
   * Method:
   *  - change toscheckbox setting
   */
  setToscheckbox() {

    if (config.debug==true) { console.log("in HeaderApp/setToscheckbox"); }
    if (this.state.toschecked)
    {
        //unchecked
        this.setState({toschecked: false});

    }
    else
    {
        //checked
        this.setState({toschecked: true});
    }
  }

  /**
   * Method:
   *  - POST to server new user for registration/signup
   */
  newUserWithEmail() {

    if (config.debug==true) { console.log("in HeaderApp/newUserWithEmail"); }

    //reset some variables
    this.setState({ signupPasswordMatch: false });

    if (!this.state.wrongSignupPassword) {
      jquery.ajax({
          //Step1: (conform REST API) POST method -> server will send to home or login screen
          url: "/auth/email-signup",
          method: "POST",
          data: { firstname: this.state.firstname, lastname: this.state.lastname, email: this.state.email, password: this.refs.pw.getValue(), birthdate: this.state.birthDay.toDate() },
          dataType: "json",
          //Step2: update UI
          success: function(data) {
            if (data == "invalid email") {
                this.setState({ showSignupModal: false });
                this.setState({ invalidSignupEmail: true });
            } else {
                this.setState({ showSignupModal: false });
                this.setState({ showEmailSignupModal: false });
                this.setState({ emailSignupPending: true });
                this.setState({ showSignupSuccessModal: true });
                this.setState({ userProps: data });
            }
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
      });
    }
  }

    /**
   * Method:
   *  - confirm user password entered second time during signup
   * Return: true if user entered twice the same password, false else
   * TODO: add checks for intelligent pw
   */
  confirmpassword(){

    if (config.debug==true) { console.log("in HeaderApp/confirmpassword"); }

    try {
        if (this.refs.pw.getValue() != this.refs.pw2.getValue()) {
            this.setState({ wrongSignupPassword: true });
            this.setState({ askPasswordConfirmation: true });
        }
    }
    catch(TypeError) {
        // pw2 not yet completed
        console.log("typeerror catch")
        this.setState({ wrongSignupPassword: true });
        this.setState({ askPasswordConfirmation: true });
    }
    if (this.refs.pw.getValue() == this.refs.pw2.getValue()) {
        this.setState({ askPasswordConfirmation: false });
        this.setState({ wrongSignupPassword: false });
        this.setState({ signupPasswordMatch: true });
    }

  }

    /**
   * Method:
   *  - set email address during signup
   * Return:
   */
  setemail() {

      if (config.debug==true) { console.log("in HeaderApp/setemail"); }

      // check valid email
      // var re1 = /[A-Z0-9]+@[A-Z0-9.-]+.[A-Z]{2,4}/igm;
      // var re2 = /[A-Z0-9._%+-]+@gmail.com/igm;
      // if (re2.test(this.refs.em.getValue())) { alert("why don't you use Google signup?"); }

      this.setState( {email: this.refs.em.getValue()} );

  }

    /**
   * Method:
   *  - login user with email address
   */
  loginWithEmail() {

    if (config.debug==true) { console.log("in HeaderApp/loginWithEmail"); }

    // reset wrongPassword and wrongEmail state (might be impacted by previous step)
    this.setState({ wrongPassword: false });
    this.setState({ wrongEmail: false });
    this.setState({ notEmailLoginUser: false });

    jquery.ajax({
          //Step1: (conform REST API) POST method -> server will send to home or login screen
          url: "/auth/email-login",
          method: "POST",
          data: { email: this.state.email, password: this.refs.loginpw.getValue() },
          dataType: "json",
          //Step2: update UI
          success: function(data) {
            console.log(data)
            if (data == "incorrect password") {
                this.setState({ showLoginModal: false });
                this.setState({ wrongPassword: true });
            } else if (data == "no password") {
                this.setState({ notEmailLoginUser: true });
                this.setState({ showEmailLoginModal: false });
                this.setState({ showLoginModal: true });
            } else if (data == "incorrect email") {
                this.setState({ showLoginModal: false });
                this.setState({ wrongEmail: true });
            } else {
                this.setState({ showLoginModal: false });
                this.setState({ showEmailLoginModal: false });
                this.props.changeLoggedIn('true');
                this.setState({ userProps: data });
            }
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
    });

    //this.forceUpdate();
  }

    /**
   * Method:
   *  - change password visibility based on clicks on eye-glyph
   */
  passwordVisibility(event) {

    if (config.debug==true) { console.log("in HeaderApp/passwordVisibility"); }

    console.log(event.type);

    if (event.type == "mousedown") { this.setState( {showLoginPassword: true} ); }
    if (event.type == "mouseup") { this.setState( {showLoginPassword: false} ); }
    if (event.type == "mouseout") { this.setState( {showLoginPassword: false} ); }
  }

    /**
   * Method:
   *  - change password visibility during signup based on clicks on eye-glyph
   */
  passwordVisibilitySignup(event) {

    if (config.debug==true) { console.log("in HeaderApp/passwordVisibilitySignup"); }

    if (event.type == "mousedown") { this.setState( {showSignupPassword: true} ); }
    if (event.type == "mouseup") { this.setState( {showSignupPassword: false} ); }
    if (event.type == "mouseout") { this.setState( {showSignupPassword: false} ); }
  }

    /**
   * Method:
   *  - check for enter key & invoke server commit if all fields have been entered
   */
  loginKeyPressed(event) {

    if (config.debug==true) { console.log("in HeaderApp/loginKeyPressed"); }

    if (event.type == "keypress" && event.key == "Enter" && this.state.email && this.refs.loginpw.getValue()) {
        // Enter pressed + email address & pw have been provided  => send to server
        this.loginWithEmail();
    }
  }

  closeSignupSuccessModal() {

    if (config.debug==true) { console.log("in HeaderApp/closeSignupSuccessModal"); }

    this.setState({ showSignupSuccessModal: false});

    if (this.state.emailSignupPending) {    //if email-signup pending: switch back off
        var newState = !this.state.emailSignupPending;
        this.setState({ emailSignupPending: newState });
    }

  }

  openSignupModalFromBecomeOwnerModal() {

    if (config.debug==true) { console.log("in HeaderApp/openSignupModalFromBecomeOwnerModal"); }

    this.setState({ showBecomeOwnerModal: false});
    this.setState({ showSignupModal: true});

  }

  openLoginModalFromBecomeOwnerModal() {

    if (config.debug==true) { console.log("in HeaderApp/openLoginModalFromBecomeOwnerModal"); }

    this.setState({ showBecomeOwnerModal: false});
    this.setState({ showLoginModal: true});

  }

  setUserProps(value) {

    if (config.debug==true) { console.log("in HeaderApp/setUserProps", value); }

    this.props.changeLoggedIn('true');
    this.setState({ userProps: value });

  }

  /**
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {
    if (config.debug==true) { console.log("in Headerapp/render"); }
    let openBecomeOwnerModal = () => this.setState({ showBecomeOwnerModal: true});
    let closeBecomeOwnerModal = () => this.setState({ showBecomeOwnerModal: false});
    let openSignupModal = () => this.setState({ showSignupModal: true});
    let closeSignupModal = () => this.setState({ showSignupModal: false});
    let openLoginModal = () => this.setState({ showLoginModal: true});
    let closeLoginModal = () => this.setState({ showLoginModal: false});
    let closeReservationsModal = () => this.setState({ showReservationsModal: false});
    let close = () => this.setState({ showBecomeOwnerModal: false});

    let emailSignup = () => this.setState({ showEmailSignupModal: true});
    let closeEmailSignupModal = () => this.setState({ showEmailSignupModal: false});
    let setfirstname = () => this.setState( {firstname: this.refs.fname.getValue()} );
    let setlastname = () => this.setState( {lastname: this.refs.lname.getValue()} );
    let setemail = () => this.setState( {email: this.refs.em.getValue()} );
    let emailLogin = () => this.setState({ showEmailLoginModal: true});
    let closeEmailLoginModal = () => this.setState({ showEmailLoginModal: false});
    let closeMyAccountModal = () => this.setState({ showMyAccountModal: false});
    let closeMyParkingModal = () => this.setState({showMyParkingsModal: false});

    var reservationsList;
    if (this.state.reservations.length != 0) {
        reservationsList = this.state.reservations.map(function(reservation){
            return <div className="row">
                        <div className="col-md-4 col-xs-12">
                          <p className="text-muted"><strong>Parking id</strong> { reservation['parkingId'] }</p>
                        </div>
                        <div className="col-md-4 col-xs-12">
                          <p className="text-muted"><strong>Start</strong> { new Date(reservation['startTime']).toDateString() + ' ' + new Date(reservation['startTime']).toLocaleTimeString() }</p>
                        </div>
                        <div className="col-md-4 col-xs-12">
                          <p className="text-muted"><strong>End</strong> { new Date(reservation['endTime']).toDateString() + ' ' + new Date(reservation['endTime']).toLocaleTimeString() }</p>
                        </div>
                    </div>;
        });

    }

    var myParkingList
    if (this.state.myParkings.length !=0){
        myParkingList = this.state.myParkings.map(function(ParkingOverview){
        return <div className="row">
                    <div className="col-md-12 col-xs-12">
                        <p className="text-muted"><strong>Parking Type </strong> { ParkingOverview['ParkingType'] }</p>
                    </div>
                    <div className="col-md-12 col-xs-12">
                        <p className="text-muted"><strong>Address </strong> { ParkingOverview['FullAddress'] }</p>
                    </div>
                    <div className="col-md-12 col-xs-12">
                        <a href={"/schedule?unit=" + ParkingOverview['UnitFriendlyName']}>Link to unit schedule</a>
                    </div>
                    <div>
                        <hr />
                    </div>
                </div>
                ;
        });
    }

    return (
      <div className="headerApp hdr-content">
        <div className="fixed-header hdr-content">
            <div className="banner-container pull-left hdr-content">
              <a href="/" id="logo"></a>
              <a href="/" id="logo-small"></a>
            </div>
            <div className="pull-right hdr-content">
                { this.props.loggedIn ?
                    <div>
                      <ButtonToolbar className="user-large">
                        <OverlayTrigger trigger={['hover', 'focus']} placement="bottom" overlay={<Popover id='add your parking'>You could earn 50 to 150euro per year with your private parking.</Popover>}>
                            <Button className="hdr-btn add-parking-btn" onClick={openBecomeOwnerModal}>Add Your Private Parking</Button>
                        </OverlayTrigger>
                        <Dropdown id="bg-vertical-dropdown">
                          <Dropdown.Toggle>
                            <Glyphicon glyph="user" className="fa-fw" />
                            {this.state.userProps["userName"]}
                          </Dropdown.Toggle>
                          { this.state.userProps['ownerYesNo'] ?
                              <Dropdown.Menu>
                                  <MenuItem eventKey="1" onSelect={this.showAccount}>My Account</MenuItem>
                                  <MenuItem eventKey="2" onSelect={this.getReservations}>My Reservations</MenuItem>
                                  <MenuItem eventKey="3" onSelect={this.getParkings}>My Parkings</MenuItem>
                                  <MenuItem eventKey="4" onSelect={this.logout}>Log out</MenuItem>
                              </Dropdown.Menu>
                          :
                              <Dropdown.Menu>
                                  <MenuItem eventKey="1" onSelect={this.showAccount}>My Account</MenuItem>
                                  <MenuItem eventKey="2" onSelect={this.getReservations}>My Reservations</MenuItem>
                                  <MenuItem eventKey="3" onSelect={this.logout}>Log out</MenuItem>
                              </Dropdown.Menu>
                          }
                        </Dropdown>
                      </ButtonToolbar>
                      <ButtonToolbar className="user-small">
                          <Dropdown pullRight id="bg-vertical-dropdown">
                              <Dropdown.Toggle>
                                <Glyphicon glyph="user" className="fa-fw" />
                              </Dropdown.Toggle>
                              { this.state.userProps['ownerYesNo'] ?
                                  <Dropdown.Menu>
                                      <MenuItem eventKey="1" onSelect={this.showAccount}>My Account</MenuItem>
                                      <MenuItem eventKey="2" onSelect={this.getReservations}>My Reservations</MenuItem>
                                      <MenuItem eventKey="3" onSelect={this.getParkings}>My Parkings</MenuItem>
                                      <MenuItem divider/>
                                      <MenuItem eventKey="4" onSelect={openBecomeOwnerModal}><strong>Add Your Private Parking</strong></MenuItem>
                                      <MenuItem eventKey="5" onSelect={this.logout}>Log out</MenuItem>
                                  </Dropdown.Menu>
                              :
                                  <Dropdown.Menu>
                                      <MenuItem eventKey="1" onSelect={this.showAccount}>My Account</MenuItem>
                                      <MenuItem eventKey="2" onSelect={this.getReservations}>My Reservations</MenuItem>
                                      <MenuItem divider/>
                                      <MenuItem eventKey="3" onSelect={openBecomeOwnerModal}><strong>Add Your Private Parking</strong></MenuItem>
                                      <MenuItem eventKey="4" onSelect={this.logout}>Log out</MenuItem>
                                  </Dropdown.Menu>
                              }
                        </Dropdown>
                      </ButtonToolbar>
                    </div>
                  :
                  <div>
                      <ButtonToolbar className="user-large">
                        <OverlayTrigger trigger={['hover', 'focus']} placement="bottom" overlay={<Popover id='add your parking'>You could earn 50 to 150euro per year with your private parking.</Popover>}>
                            <Button className="hdr-btn add-parking-btn" onClick={openBecomeOwnerModal}>Add Your Private Parking</Button>
                        </OverlayTrigger>
                        <Button className="hdr-btn" onClick={openSignupModal}>Sign up</Button>
                        <Button className="hdr-btn" onClick={openLoginModal}>Log in</Button>
                      </ButtonToolbar>
                      <ButtonToolbar className="user-small">
                          <Dropdown pullRight id="bg-vertical-dropdown">
                              <Dropdown.Toggle>
                                <i className="fa fa-bars user-small"></i>
                              </Dropdown.Toggle>
                              <Dropdown.Menu>
                                  <MenuItem eventKey="1" onSelect={openSignupModal}>Sign up</MenuItem>
                                  <MenuItem eventKey="2" onSelect={openLoginModal}>Log in</MenuItem>
                                  <MenuItem eventKey="3" onSelect={openBecomeOwnerModal}><strong>Add Your Private Parking</strong></MenuItem>
                              </Dropdown.Menu>
                        </Dropdown>
                      </ButtonToolbar>
                  </div>
                }
            </div>
        </div>
        <div className="tagline">
            <h1 className="title">Looking for a parking space?</h1>
            <h4 className="title">Drive straight to your reserved parking and arrive on time without any hassle</h4>
        </div>
        <div className="tagline-small">
            <h2 className="title">Looking for a parking space?</h2>
            <h4 className="title">Drive straight to your reserved parking and arrive on time without any hassle</h4>
        </div>

        <Modal
            show={this.state.showBecomeOwnerModal}
            onHide={closeBecomeOwnerModal}
            bsSize="large"
        >
            <Modal.Header closeButton>
              <Modal.Title>Earn money with Parking Plaza</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <BecomeOwnerApp loggedIn={this.props.loggedIn} userProps={this.state.userProps} poiTypes={this.props.poiTypes} becomeownersetuserprops={this.setUserProps}/>
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showMyAccountModal}
            onHide={closeMyAccountModal}
            style={{height: 900}}
        >
            <Modal.Header closeButton>
                <Modal.Title>My Account Info</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            { this.state.userProps['ownerYesNo'] ?
                <div>
                    <div className="row">
                        <div className="col-md-6 col-xs-12">
                            <p className="text-muted"><strong>Display Name</strong> { this.state.myaccountinfo['fullname'] }</p>
                        </div>
                        <div className="col-md-6 col-xs-12">
                            <p className="text-muted"><strong>Email</strong> { this.state.myaccountinfo['email'] }</p>
                        </div>
                    </div>
                    <p> If you would like to update this information, please contact us via <a href="mailto:support@parking-plaza.com?Subject=Update%20Account%20Info">email</a>.</p>
                </div>
            :
                <div>
                    <div className="row">
                        <div className="col-md-4 col-xs-12">
                            <p className="text-muted"><strong>Display Name</strong> { this.state.myaccountinfo['fullname'] }</p>
                        </div>
                        <div className="col-md-4 col-xs-12">
                            <p className="text-muted"><strong>Email</strong> { this.state.myaccountinfo['email'] }</p>
                        </div>
                    </div>
                    <p> If you would like to update this information, please contact us via <a href="mailto:support@parking-plaza.com?Subject=Update%20Account%20Info">email</a>.</p>
                </div>
            }
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showSignupModal}
            onHide={closeSignupModal}
            style={{height: 500}}
            className="sign-up-modal"
        >
            <Modal.Header closeButton>
              <Modal.Title>Sign up</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="signup-modal">
                    { !this.state.toschecked ?
                    <div>
                        <OverlayTrigger trigger={['hover', 'focus']} placement="bottom" overlay={<Popover id='check Terms of Service'>Please check the Terms of Service first</Popover>}>
                            <Button className="signup-button" bsSize="large" block><img id="google-logo" src="/images/g-logo.png" alt="Google Signup Button"></img>Sign up with Google account</Button>
                        </OverlayTrigger>
                        <OverlayTrigger trigger={['hover', 'focus']} placement="bottom" overlay={<Popover id='check Terms of Service'>Please check the Terms of Service first</Popover>}>
                            <Button className="signup-button" bsSize="large" block><Glyphicon id="email-logo" glyph="envelope" />Sign up with your email</Button>
                        </OverlayTrigger>
                    </div>
                    :
                    <div>
                        <Button className="signup-button" href="/auth/google-signup" bsSize="large" block><img id="google-logo" src="/images/g-logo.png" alt="Google Signup Button"></img>Sign up with Google account</Button>
                        <Button className="signup-button" onClick={emailSignup} bsSize="large" block><Glyphicon id="email-logo" glyph="envelope" />Sign up with your email</Button>
                    </div>
                    }
                    <div className="checkbox">
                        <label>
                          <input type="checkbox" ref="toscheckbox" className="tosbox" checked={this.state.toschecked} onChange={this.setToscheckbox} /> I accept the <a href="/tos"> Terms of Service</a>.
                        </label>
                    </div>
                </div>
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showEmailSignupModal}
            onHide={closeEmailSignupModal}
            style={{height: 500}}
            className="sign-up-modal"
        >
            <Modal.Header closeButton>
              <Modal.Title>Sign up with your email</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { this.state.invalidSignupEmail ?
                    <form>
                        <div className="alertmessage">
                            You have entered an invalid email address, please verify and enter it again.
                        </div>
                        <span className="input-group-addon span-color">First name</span>
                        <Input type="text" placeholder="Enter your first name" ref="fname" onChange={setfirstname}/>
                        <span className="input-group-addon span-color">Last name</span>
                        <Input type="text" placeholder="Enter you last name" ref="lname" onChange={setlastname}/>
                        <span className="input-group-addon span-color">Email address</span>
                        <Input className="form-control" type="email" placeholder="Enter your email" ref="em" onChange={this.setemail} bsStyle="error" />
                        <span className="input-group-addon span-color">Password</span>
                        <div className="password">
                            { this.state.showSignupPassword ?
                                <Input className="form-control" type="text" placeholder="Enter your new password" ref="pw" onChange={this.confirmpassword}/>
                            :
                                <Input className="form-control" type="password" placeholder="Enter your new password" ref="pw" onChange={this.confirmpassword}/>
                            }
                            <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibilitySignup} onMouseUp={this.passwordVisibilitySignup} onMouseOut={this.passwordVisibilitySignup}></span>
                        </div>
                        { this.state.askPasswordConfirmation ?
                            <div>
                                <span className="input-group-addon span-color">Confirm your password</span>
                                <div className="password">
                                    { this.state.showSignupPassword ?
                                        <Input className="form-control" type="text" placeholder="Enter your password again" ref="pw2" onChange={this.confirmpassword}/>
                                    :
                                        <Input className="form-control" type="password" placeholder="Enter your password again" ref="pw2" onChange={this.confirmpassword}/>
                                    }
                                    <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibilitySignup} onMouseUp={this.passwordVisibilitySignup} onMouseOut={this.passwordVisibilitySignup}></span>
                                </div>
                            </div>
                        : null }
                        <span className="input-group-addon span-color">Birthday</span>
                        <DatePicker className="birthdaypicker" selected={this.state.birthDay} locale="en-gb" onChange={this.changeBirthday} isClearable={true} showYearDropdown dateFormatCalendar="MMMM"/>
                        <Button className="confirmbutton" onClick={this.newUserWithEmail}>Signup</Button>
                    </form>
                :
                    <form className="signup-modal">
                        <span className="input-group-addon span-color">First name</span>
                        <Input type="text" placeholder="Enter your first name" ref="fname" onChange={setfirstname}/>
                        <span className="input-group-addon span-color">Last name</span>
                        <Input type="text" placeholder="Enter you last name" ref="lname" onChange={setlastname}/>
                        <span className="input-group-addon span-color">Email address</span>
                        <Input className="form-control" type="email" placeholder="Enter your email" ref="em" onChange={this.setemail} />
                        <span className="input-group-addon span-color">Password</span>
                        { this.state.signupPasswordMatch ?
                            <div className="password">
                                { this.state.showSignupPassword ?
                                    <Input className="form-control" type="text" placeholder="Enter your new password" ref="pw" onChange={this.confirmpassword} bsStyle="success" />
                                :
                                    <Input className="form-control" type="password" placeholder="Enter your new password" ref="pw" onChange={this.confirmpassword} bsStyle="success" />
                                }
                                <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibilitySignup} onMouseUp={this.passwordVisibilitySignup} onMouseOut={this.passwordVisibilitySignup}></span>
                            </div>
                        :
                            <div className="password">
                                { this.state.showSignupPassword ?
                                    <Input className="form-control" type="text" placeholder="Enter your new password" ref="pw" onChange={this.confirmpassword} />
                                :
                                    <Input className="form-control" type="password" placeholder="Enter your new password" ref="pw" onChange={this.confirmpassword} />
                                }
                                <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibilitySignup} onMouseUp={this.passwordVisibilitySignup} onMouseOut={this.passwordVisibilitySignup}></span>
                            </div>
                        }
                        { this.state.wrongSignupPassword ?
                            <div>
                                { this.state.askPasswordConfirmation ?
                                    <div>
                                        <span className="input-group-addon span-color">Confirm your password</span>
                                        <div className="password">
                                            { this.state.showSignupPassword ?
                                                <Input className="form-control" type="text" placeholder="Enter your password again" ref="pw2" onChange={this.confirmpassword} bsStyle="error" />
                                            :
                                                <Input className="form-control" type="password" placeholder="Enter your password again" ref="pw2" onChange={this.confirmpassword} bsStyle="error" />
                                            }
                                            <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibilitySignup} onMouseUp={this.passwordVisibilitySignup} onMouseOut={this.passwordVisibilitySignup}></span>
                                        </div>
                                    </div>
                                : null }
                            </div>
                        :
                            <div>
                                { this.state.askPasswordConfirmation ?
                                    <div>
                                        <span className="input-group-addon span-color">Confirm your password</span>
                                        <div className="password">
                                            { this.state.showSignupPassword ?
                                                <Input className="form-control" type="text" placeholder="Enter your password again" ref="pw2" onChange={this.confirmpassword} />
                                            :
                                                <Input className="form-control" type="password" placeholder="Enter your password again" ref="pw2" onChange={this.confirmpassword} />
                                            }
                                            <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibilitySignup} onMouseUp={this.passwordVisibilitySignup} onMouseOut={this.passwordVisibilitySignup}></span>
                                        </div>
                                    </div>
                                : null }
                            </div>
                        }
                        <span className="input-group-addon span-color">Birthday</span>
                        <DatePicker className="birthdaypicker" selected={this.state.birthDay} locale="en-gb" onChange={this.changeBirthday} isClearable={true} showYearDropdown dateFormatCalendar="MMMM"/>
                        <Button className="confirmbutton" onClick={this.newUserWithEmail}>Sign Up</Button>
                    </form>
                }
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showSignupSuccessModal}
            onHide={this.closeSignupSuccessModal}
            className="sign-up-modal"
        >
            <Modal.Header closeButton>
              <Modal.Title>Thanks for signing up with Parking Plaza!</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { this.state.emailSignupPending ?
                    <div>
                        <div className="row ownermodal">
                            You will receive an email shortly to activate your account.
                        </div>
                        <div className="row ownermodal">
                            The activation is required once for security reasons as it allows us to make sure that your email address is used properly.
                        </div>
                    </div>
                :
                    <div className="text-muted">
                        You can get started now by searching for free parking slots or add your own private parking space to Parking Plaza on our <a href="https://www.parking-plaza.com" target="_blank">website</a>.
                    </div>
                }
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showMyParkingsModal}
            onHide={closeMyParkingModal}
            style={{height: 900}}
        >
            <Modal.Header closeButton>
                <Modal.Title>My Parking Info</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            { this.state.myParkings.length !=0 ?
                <div>
                {myParkingList}
                </div>
            :
                <div>
                    <p> You currently have no parking units registered in our system. Please add your parking unit first. </p>
                </div>
            }
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showLoginModal}
            onHide={closeLoginModal}
            style={{height: 500}}
        >
            <Modal.Header closeButton>
              <Modal.Title>Log in</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { this.state.notEmailLoginUser ?
                    <div>
                        <div className="alertmessage">
                            You signed up with a Google account, please use this to login.
                        </div>
                        <Button className="signup-button" href="/auth/google-login" bsSize="large" block><img id="google-logo" src="/images/g-logo.png" alt="Google Signup Button"></img>Login with Google account</Button>
                    </div>
                :   <div>
                        <Button className="signup-button" href="/auth/google-login" bsSize="large" block><img id="google-logo" src="/images/g-logo.png" alt="Google Signup Button"></img>Login with Google account</Button>
                        <Button className="signup-button" onClick={emailLogin} bsSize="large" block><Glyphicon id="email-logo" glyph="envelope" />Login with your email</Button>
                    </div>
                }
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showEmailLoginModal}
            onHide={closeEmailLoginModal}
            style={{height: 500}}
            className="login-modal"
        >
            <Modal.Header closeButton>
              <Modal.Title>Login with your email</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { this.state.wrongEmail ?
                    <div>
                        <div className="alertmessage">
                            You have entered an incorrect email address, please try again.
                        </div>
                        <form className="login-modal">
                            <span className="input-group-addon span-color">Email address</span>
                            <Input className="form-control" type="email" placeholder={this.state.email} ref="em" onChange={setemail} bsStyle="error" hasFeedback />
                            <span className="input-group-addon span-color">Password</span>
                            <div className="password">
                                { this.state.showLoginPassword ?
                                    <Input className="form-control" type="text" ref="loginpw" onKeyPress={this.loginKeyPressed}/>
                                :
                                    <Input className="form-control" type="password" ref="loginpw" onKeyPress={this.loginKeyPressed}/>
                                }
                                <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibility} onMouseUp={this.passwordVisibility} onMouseOut={this.passwordVisibility}></span>
                            </div>
                            <Button className="confirmbutton" onClick={this.loginWithEmail}>Login</Button>
                        </form>
                    </div>
                : null }
                { (!this.state.wrongEmail && this.state.wrongPassword) ?
                    <div>
                        <div className="alertmessage">
                            You have entered an incorrect password, please verify and enter it again.
                        </div>
                        <form className="login-modal">
                            <span className="input-group-addon span-color">Email address</span>
                            <Input className="form-control" type="email" placeholder={this.state.email} ref="em" onChange={setemail}/>
                            <span className="input-group-addon span-color">Password</span>
                            <div className="password">
                                { this.state.showLoginPassword ?
                                    <Input className="form-control" type="text" ref="loginpw" onKeyPress={this.loginKeyPressed}/>
                                :
                                    <Input className="form-control" type="password" ref="loginpw" bsStyle="error" onKeyPress={this.loginKeyPressed}/>
                                }
                                <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibility} onMouseUp={this.passwordVisibility} onMouseOut={this.passwordVisibility}></span>
                            </div>
                            <Button className="confirmbutton" onClick={this.loginWithEmail}>Login</Button>
                        </form>
                    </div>
                : null }
                { (!this.state.wrongEmail && !this.state.wrongPassword) ?
                    <form className="login-modal">
                        <span className="input-group-addon span-color">Email address</span>
                        <Input className="form-control" type="email" placeholder={this.state.email} ref="em" onChange={setemail} />
                        <span className="input-group-addon span-color">Password</span>
                        <div className="password">
                            { this.state.showLoginPassword ?
                                <Input className="form-control" type="text" ref="loginpw" onKeyPress={this.loginKeyPressed}/>
                            :
                                <Input className="form-control" type="password" ref="loginpw" onKeyPress={this.loginKeyPressed}/>
                            }
                            <span className="glyphicon glyphicon-eye-open" onMouseDown={this.passwordVisibility} onMouseUp={this.passwordVisibility} onMouseOut={this.passwordVisibility}></span>
                        </div>
                        <Button className="confirmbutton" onClick={this.loginWithEmail}>Login</Button>
                    </form>
                : null }
            </Modal.Body>
        </Modal>

        <Modal
            show={this.state.showReservationsModal}
            onHide={closeReservationsModal}
            style={{height: 700}}
        >
            <Modal.Header closeButton>
              <Modal.Title>My Reservations</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { this.state.reservations == 0 ?
                <div>
                    <p> You have no reservations yet. </p>
                </div>
                : <div> {reservationsList} </div>
                }
            </Modal.Body>
        </Modal>
      </div>
    );
  }
}

HeaderApp.propTypes = {
    userProps: React.PropTypes.object,
    poiTypes: React.PropTypes.array,
    loggedIn: React.PropTypes.bool,
};