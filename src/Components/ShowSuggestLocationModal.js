/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import { Button, Input, Modal } from 'react-bootstrap';
import GooglePlacesSuggest from 'react-google-places-suggest';

/**
 * React Component: ShowSuggestLocationModal
 */
export default class ShowSuggestLocationModal extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);
        // init state
        this.state = {
            email: null,
            search: "",
            selectedCoordinate: null,
            entryError: false,
        };

        this.checkLocationInfo = this.checkLocationInfo.bind(this);

        if (this.props.config.debug==true) { console.log("in ShowSuggestLocationModal/constructor"); }

    }

    /**
     * Check whether all required location info fields have been completed and submit callback once ok
     */
    checkLocationInfo() {

        if (this.props.config.debug==true) { console.log("in ShowSuggestLocationModal/checkLocationInfo"); }

        var checkInfo = false;

        if (!this.props.loggedIn) {
            (this.state.email != '' && this.state.selectedCoordinate != null) ? checkInfo = true : false;
        } else {
            (this.state.selectedCoordinate != null) ? checkInfo = true : false;
        }

        if (checkInfo) {
            this.setState({ entryError: false });
            var suggestInfo = {
                'location' : this.state.selectedCoordinate,
                'emailaddress' : this.state.email,
            };
            //console.log(suggestInfo);
            this.props.suggestLocation(suggestInfo);
        } else {
            this.setState({ entryError: true });
        }

    }

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in ShowSuggestLocationModal/render"); }

        /**
          * GooglePlacesSuggest handler method
          */
        const { search } = this.state
        let handleSearchChange = (e) => this.setState({ search: e.target.value });
        let handleSelectSuggest = (suggestName, coordinate) => this.setState({ search: suggestName, selectedCoordinate: coordinate });
        let setemail = () => this.setState( {email: this.refs.em.getValue()} );

        return (
            <Modal
                show={this.props.show}
                onHide={this.props.hide.bind(null, 'location')}
              >
                <Modal.Header closeButton>
                    { !this.props.successFlag ?
                        <Modal.Title>Suggest Location</Modal.Title>
                    :
                        <Modal.Title>Thanks for your suggestion</Modal.Title>
                    }
                </Modal.Header>
                <Modal.Body>
                    { !this.props.successFlag ?
                        <div>
                            <p>We are sorry that you don't find the location you want to visit. </p>
                            <p>Tell us where you want to go and we will investigate whether it's possible to add parkings there. </p>
                            { !this.props.loggedIn ?
                                <Input className="form-control" type="email" placeholder="Your email address" ref="em" onChange={setemail} />
                            : null }
                            <GooglePlacesSuggest onSelectSuggest={ handleSelectSuggest.bind(this) } search={ this.state.search }>
                                <input
                                    type="text"
                                    value={ this.state.search }
                                    placeholder="Location address"
                                    onChange={ handleSearchChange.bind(this) }
                                />
                            </GooglePlacesSuggest>
                            { this.state.entryError ?
                                <div className="alertmessage"> Please complete all fields and hit Send again. </div>
                            : null}
                        </div>
                    :
                        <div>
                            <p>Thanks for your time to send us your suggestion!</p>
                            <p>We will investigate your request shortly and will inform you via email once Parking Plaza capacity has been made available at {this.state.search}. </p>
                            <p>For any further questions or suggestions, please contact us via <a href="mailto:support@parking-plaza.com?Subject=Suggest%Location">email</a>.</p>
                        </div>
                    }
                </Modal.Body>
                <Modal.Footer>
                  { !this.props.successFlag ?
                    <Button className="modalLeftButton" onClick={this.checkLocationInfo}>Send</Button>
                  : null }
                  <Button onClick={this.props.hide.bind(null, 'location')}>Cancel</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

ShowSuggestLocationModal.propTypes = {
    config: React.PropTypes.object,
    show: React.PropTypes.bool,
    loggedIn: React.PropTypes.bool,
    successFlag: React.PropTypes.bool,
};