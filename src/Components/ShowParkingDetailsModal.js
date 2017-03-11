/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import { Button, Modal } from 'react-bootstrap';

/**
 * React Component: ShowParkingDetailsModal
 */
export default class ShowParkingDetailsModal extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in ShowParkingDetailsModal/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {
        return (
            <Modal
                show={this.props.show}
                onHide={this.props.hide.bind(null, 'parking')}
              >
                <Modal.Header closeButton>
                  <Modal.Title>Confirm your parking</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    { this.props.loggedIn ?
                        <div>
                            { Object.keys(this.props.availableParkingSlot).length != 0 ?
                            <div>
                                <div className="row">
                                    <div className="col-md-12 col-xs-12">
                                        <p>We have the following parking available for this event:</p>
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-md-12 col-xs-12">
                                      <p className="text-muted"><strong>Address</strong> {this.props.availableParkingSlot['address']}</p>
                                    </div>
                                    <div className="col-md-3 col-xs-3">
                                      <p className="text-muted"><strong>Price</strong> {this.props.availableParkingSlot['price']}</p>
                                    </div>
                                    <div className="col-md-9 col-xs-9">
                                      <p className="text-muted"><strong>Distance to stadium</strong> {this.props.availableParkingSlot['distance']} km</p>
                                    </div>
                                    <div className="col-md-12 col-xs-12">
                                      <Button onClick={this.props.reserveParking} className="btn btn-primary" id="reservationButton" data-toggle="tooltip" title="Click this button to book your Parking.">Pay</Button>
                                    </div>
                                </div>
                            </div> :
                            <div className="row">
                                <div className="col-md-12 col-xs-12">
                                    <p className="text-muted">Sorry, there is no parking unit available at this time.</p>
                                </div>
                            </div>
                            }
                        </div>
                    :
                        <div className="row">
                            <p className="text-muted alertmessage"> Please log in first to book a parking. </p>
                        </div>
                    }
                </Modal.Body>
                <Modal.Footer>
                  <Button onClick={this.props.hide.bind(null, 'parking')}>Cancel</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

ShowParkingDetailsModal.propTypes = {
    config: React.PropTypes.object,
    show: React.PropTypes.bool,
    availableParkingSlot: React.PropTypes.object,
    loggedIn: React.PropTypes.bool,
};