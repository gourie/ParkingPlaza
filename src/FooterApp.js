/*
*   Author: Joeri Nicolaes
*   ======================
*/

import React from 'react';
import {Glyphicon} from 'react-bootstrap';
import jquery from 'jquery';

// Config for the app setup: TODO - retrieve from server
var config = {
  debug: true
};

/**
 * React Component: FooterApp that will be rendered on all Parking Plaza pages
 */
//module.exports = React.createClass({
export default class FooterApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in FooterApp/constructor"); }
    super(props);
    // init state
    this.state = {
        showLanguage: "English",
    };
    // catch bindings for click
  }

  /**
   * Standard React method: initialize state of this React component
   */
  //getInitialState: function() {
//  getInitialState() {
//    if (config.debug==true) { console.log("in getInitialState"); }
//
//    return {
//      showLanguage: "English"
//    };
//  }
  //},

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in FooterApp/componentDidMount"); }

    //(this.props.language != "") ? this.setState({showLanguage: this.props.language}) : false;
  }

  /**
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {
    if (config.debug==true) { console.log("in FooterApp/render"); }

    return (
      <div className="FooterApp ftr-content">
        <div className="row">
            <div className="col-md-3 col-md-offset-1 col-xs-10 col-xs-offset-1">
                <h4 className="ftr-title"> Headquarters </h4>
                <p className="ftr-line"> Spiltstraat 232 </p>
                <p className="ftr-line"> 1980 Zemst, Belgium </p>
            </div>
            <div className="col-md-4 col-md-offset-0 col-xs-10 col-xs-offset-1">
                <h4 className="ftr-title"> Contact us </h4>
                <a href="mailto:support@parking-plaza.com?Subject=Website%20Enquiry"><p className="ftr-line">support@parking-plaza.com</p></a>
                <a href="https://www.facebook.com/untappedparkingplaza" target="_blank"><p className="ftr-line">Facebook</p></a>
            </div>
            <div className="col-md-3 col-md-offset-0 col-xs-10 col-xs-offset-1">
                <h4 className="ftr-title"> Legal </h4>
                <p className="ftr-line"> BTW BE 0647.514.689</p>
                <p className="ftr-line"> IBAN BE95 7310 4208 6958</p>
                <p className="ftr-line"> <a href="/tos"> Terms of Service</a></p>
            </div>
        </div>
        <p className="ftr-text"> <Glyphicon glyph="copyright-mark" className="fa-fw" /> Untapped VOF 2016</p>
      </div>  /** END OF FooterApp div**/
    );
  }
}