/*
*   Author: Joeri Nicolaes
*   ======================
*/

// import react
//import React from 'react';
import React from 'react';
import HeaderApp from './HeaderApp';
import FooterApp from './FooterApp';

// Config for the app setup: TODO - retrieve from server
var config = {
  debug: true
};

/**
 * React Component: FooterApp that will be rendered on all Parking Plaza pages
 */
//module.exports = React.createClass({
export default class EmailConfApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in EmailConfApp/constructor"); }
    super(props);

    this.state = {
        loggedIn: (this.props.loggedInAtStart == "true") ? true : false,
    };

    this.changeLoggedIn = this.changeLoggedIn.bind(this);
  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in EmailConfApp/componentDidMount"); }

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
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {
    if (config.debug==true) { console.log("in EmailConfApp/render"); }

    return (
        <div className="EmailConfApp">
            <HeaderApp userProps={this.props.userProps} poiTypes={this.props.availablePoiTypes} loggedIn={this.state.loggedIn} changeLoggedIn={this.changeLoggedIn}/>
            <div className="pane">
            { this.props.emailconf['status'] ?
                <div>
                    <div className="title-line text-muted">
                        Welcome to Parking Plaza, the online solution to book a parking near your favorite event and arrive on time without any hassle!
                    </div>
                    <div className="title-line text-muted">
                        Your account has now been activated; an email with more details has been sent to <b>{this.props.emailconf['email']}</b>.
                    </div>
                    <div className="title-line text-muted">
                        If you have any further questions please contact us via <a href="mailto:support@parking-plaza.com?Subject=Info%20Required%20After%20ParkingSpaceListing">email</a> or <a href="https://www.facebook.com/untappedparkingplaza" target="_blank">Facebook</a>.
                    </div>
                </div>
                :
                <div>
                    <div className="title-line text-muted">
                        The confirmation code used for this email account is not valid, please sign up again on our <a href="https://www.parking-plaza.com" target="_blank">website</a>.
                    </div>
                    <div className="title-line text-muted">
                        If you have any further questions please contact us via <a href="mailto:support@parking-plaza.com?Subject=Info%20Required%20After%20ParkingSpaceListing">email</a> or <a href="https://www.facebook.com/untappedparkingplaza" target="_blank">Facebook</a>.
                    </div>
                </div>
            }
            </div>
            <div className="footer">
                <FooterApp />
            </div>
        </div>
    );
  }
}

EmailConfApp.propTypes = {
    userProps: React.PropTypes.object,
    loggedInAtStart: React.PropTypes.string,
    emailconf: React.PropTypes.bool,
};