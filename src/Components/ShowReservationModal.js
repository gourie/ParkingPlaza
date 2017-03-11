/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import { Button, Modal } from 'react-bootstrap';

/**
 * React Component: ShowReservationModal
 */
export default class ShowReservationModal extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        if (this.props.config.debug==true) { console.log("in ShowReservationModal/constructor"); }

    }

    /**
     * Standard React method: render
     */
    render() {
        return (
            <Modal
                show={this.props.show}
                onHide={this.props.hide.bind(null, 'reservation')}
              >
                <Modal.Header closeButton>
                  <Modal.Title>Reservation confirmed</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div>
                        <p>Thanks for your reservation. You will receive an invoice via email soon.</p>
                        <a href={this.props.linktodirections} target="_blank"> Walking directions from your parking </a>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                  <Button onClick={this.props.hide.bind(null, 'reservation')}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

ShowReservationModal.propTypes = {
    config: React.PropTypes.object,
    show: React.PropTypes.bool,
    linktodirections: React.PropTypes.string,
};

