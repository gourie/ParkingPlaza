/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import React from 'react';
import {Button, Input} from 'react-bootstrap';
import jquery from 'jquery';

/**
 * React Component: TestApp
 */

export default class TestApp extends React.Component {

  /**
   * Standard ES6 method
   */
  constructor(props) {
    super(props);
    // init state
    this.state = {
        field1: "",
        field2: "",
        field3: "",
        field4: "",
        field5: "",
        field6: "",
    };
    // catch bindings for click
    this.send = this.send.bind(this);
  }

  /**
   * Standard React method: runs after initial render
   */
  componentDidMount() {
    console.log("in TestApp/componentDidMount");
  }

  /**
   * Method:
   *  - send form
   */
  send() {
     jquery.ajax({
          url: "/payment",
          method: "POST",
          data: { id1: this.state.field1, id2: this.state.field2, id3: this.state.field3, id4: this.state.field4, id5: this.state.field5, id6: this.state.field6 },
          dataType: "json",
          //Step2: update UI
          success: function(data) {
            console.log("send(),jquery.ajax --- followed by the data")
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
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
     });
  }

  /**
   * Standard React method: render app (JSX code --> converted offline in JS using Babel in Webpack)
   */
  render() {
    let setfield1 = () => this.setState( {field1: this.refs.id1.getValue()} );
    let setfield2 = () => this.setState( {field2: this.refs.id2.getValue()} );
    let setfield3 = () => this.setState( {field3: this.refs.id3.getValue()} );
    let setfield4 = () => this.setState( {field4: this.refs.id4.getValue()} );
    let setfield5 = () => this.setState( {field5: this.refs.id5.getValue()} );
    let setfield6 = () => this.setState( {field6: this.refs.id6.getValue()} );

    return (
        <div>
            <form>
                <span className="input-group-addon span-color">StartTime</span>
                <Input className="form-control" type="text" value="2016-02-26 10:00:00+01" ref="id1" onChange={setfield1}/>
                <span className="input-group-addon span-color">End Time</span>
                <Input className="form-control" type="text" value="2016-02-26 12:00:00+01" ref="id2" onChange={setfield2}/>
                <span className="input-group-addon span-color">Unit ID</span>
                <Input className="form-control" type="text" placeholder="3" ref="id3" onChange={setfield3}/>
                <span className="input-group-addon span-color">Useruuid</span>
                <Input className="form-control" type="text" value="2577527d-f2b7-4469-91d2-f91663906577" ref="id4" onChange={setfield4}/>
                <span className="input-group-addon span-color">Id5</span>
                <Input className="form-control" type="text" placeholder="Enter field5" ref="id5" onChange={setfield5}/>
                <span className="input-group-addon span-color">Id6</span>
                <Input className="form-control" type="text" placeholder="Enter field6" ref="id6" onChange={setfield6}/>
                <Button className="confirmbutton" onClick={this.send}>Send</Button>
            </form>
        </div>
    );
  }
}