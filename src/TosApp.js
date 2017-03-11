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
export default class TosApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    if (config.debug==true) { console.log("in TosApp/constructor"); }
    super(props);
    // init state
    this.state = {
        showLanguage: "English",
        loggedIn: (this.props.loggedInAtStart == "true") ? true : false,
    };
    // catch bindings for click
    this.changeLoggedIn = this.changeLoggedIn.bind(this);
  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {

    if (config.debug==true) { console.log("in TosApp/componentDidMount"); }

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
    if (config.debug==true) { console.log("in TosApp/render"); }

    var toslines;
    if (this.props.tos.length != 0) {
        toslines = this.props.tos.map(function(line) {
            if (line == "Untapped Terms of Service") {
                return <h4 className="tostitle">
                            { line }
                       </h4>
            }
            if (line.startsWith("Last updated on")) {
                return <div className="tosdate">
                            { line }
                       </div>
            }
            if (line.startsWith("Article")) {
                return <div className="tosheader">
                            { line }
                       </div>
            }
            else {
                return <div className="tosline">
                            { line }
                       </div>;
            }
        });
    }

    return (
        <div className="TosApp">
            <HeaderApp userProps={this.props.userProps} poiTypes={this.props.availablePoiTypes} loggedIn={this.state.loggedIn} changeLoggedIn={this.changeLoggedIn}/>
            <div> {toslines} </div>
            <div className="footer">
                <FooterApp />
            </div>
        </div>
    );
  }
}

TosApp.propTypes = {
    tos: React.PropTypes.array,
    userProps: React.PropTypes.object,
    loggedInAtStart: React.PropTypes.string,
};