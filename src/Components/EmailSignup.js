/*
*   Author: Joeri Nicolaes
*   version: alpha
*/

import jquery from 'jquery';
import React from 'react';
import { Button, Input } from 'react-bootstrap';
import moment from 'moment';

/**
 * React Component: EmailSignup
 */
export default class EmailSignup extends React.Component {

    /**
     * Standard ES6 method
     */
    constructor(props) {

        super(props);

        // init state
        this.state = {
            invalidSignupEmail: false,
            askPasswordConfirmation: false,
            wrongSignupPassword: false,
            signupPasswordMatch: false,
            showSignupPassword: false,
            signupSuccess: false,
            toschecked: false,
            forgottochecktos: false,
        };

        // catch bindings for click
        this.newUserWithEmail = this.newUserWithEmail.bind(this);
        this.setemail = this.setemail.bind(this);
        this.confirmpassword = this.confirmpassword.bind(this);
        this.passwordVisibilitySignup = this.passwordVisibilitySignup.bind(this);
        this.setToscheckbox = this.setToscheckbox.bind(this);

        if (this.props.config.debug==true) { console.log("in EmailSignup/constructor"); }

    }

    /**
    * Method:
    *  - POST to server new user for registration/signup
    */
    newUserWithEmail() {

        if (this.props.config.debug==true) { console.log("in EmailSignup/newUserWithEmail"); }

        //reset some variables
        this.setState({ signupPasswordMatch: false });
        this.setState({ invalidSignupEmail: false });
        this.setState({ signupSuccess: false });
        this.setState({ forgottochecktos: false });

        if (this.state.toschecked) {
            if (!this.state.wrongSignupPassword) {
              jquery.ajax({
                  //Step1: (conform REST API) POST method -> server will send to home or login screen
                  url: "/auth/email-signup",
                  method: "POST",
                  data: { firstname: this.state.firstname, lastname: this.state.lastname, email: this.state.email, password: this.refs.pw.getValue(), birthdate: '' },
                  dataType: "json",
                  //Step2: update UI
                  success: function(data) {
                    if (data == "invalid email") {
                        this.setState({ invalidSignupEmail: true });
                    } else {
                        this.setState({ signupSuccess: true });
                        console.log(data);
                        this.props.setUserProps(data);
                    }
                  }.bind(this),
                  error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                  }.bind(this)
              });
            }
        } else {
            this.setState({ forgottochecktos: true });
        }
    }

    /**
    * Method:
    *  - confirm user password entered second time during signup
    * Return: true if user entered twice the same password, false else
    * TODO: add checks for intelligent pw
    */
    confirmpassword(){

        if (this.props.config.debug==true) { console.log("in EmailSignup/confirmpassword"); }

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

      if (this.props.config.debug==true) { console.log("in EmailSignup/setemail"); }

      // check valid email
      // var re1 = /[A-Z0-9]+@[A-Z0-9.-]+.[A-Z]{2,4}/igm;
      // var re2 = /[A-Z0-9._%+-]+@gmail.com/igm;
      // if (re2.test(this.refs.em.getValue())) { alert("why don't you use Google signup?"); }

      this.setState( {email: this.refs.em.getValue()} );

    }

    /**
    * Method:
    *  - change password visibility during signup based on clicks on eye-glyph
    */
    passwordVisibilitySignup(event) {

        if (this.props.config.debug==true) { console.log("in EmailSignup/passwordVisibilitySignup"); }

        if (event.type == "mousedown") { this.setState( {showSignupPassword: true} ); }
        if (event.type == "mouseup") { this.setState( {showSignupPassword: false} ); }
        if (event.type == "mouseout") { this.setState( {showSignupPassword: false} ); }
    }

    /**
    * Method:
    *  - change toscheckbox setting
    */
    setToscheckbox() {

        if (this.props.config.debug==true) { console.log("in EmailSignup/setToscheckbox"); }

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

    /**
     * Standard React method: render
     */
    render() {

        if (this.props.config.debug==true) { console.log("in EmailSignup/render"); }

        let setfirstname = () => this.setState( {firstname: this.refs.fname.getValue()} );
        let setlastname = () => this.setState( {lastname: this.refs.lname.getValue()} );
        let setemail = () => this.setState( {email: this.refs.em.getValue()} );

        return (
            <div>
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
                        <div className="ownermodal">
                            <Button onClick={this.newUserWithEmail}>Sign Up</Button>
                        </div>
                    </form>
                :
                    <div>
                        { this.state.signupSuccess ?
                        <div>
                            <div className="row ownermodal">
                                Thanks for signing up with Parking Plaza!
                            </div>
                            <div className="row ownermodal">
                                You will receive an email shortly to activate your account.
                            </div>
                            <div className="row ownermodal">
                                The activation is required once for security reasons as it allows us to make sure that your email address is used properly.
                            </div>
                        </div>
                        :
                        <div>
                            <div className="row ownermodal">
                                    Please sign up with your email address.
                            </div>
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
                                { this.state.forgottochecktos ?
                                    <div className="alertmessage">
                                        Please tick Terms of Service checkbox!
                                    </div>
                                : null }
                                <div className="ownermodal">
                                    <div className="checkbox">
                                        <label>
                                          <input type="checkbox" ref="toscheckbox" className="tosbox" checked={this.state.toschecked} onChange={this.setToscheckbox} /> I accept the <a href="/tos"> Terms of Service</a>.
                                        </label>
                                    </div>
                                </div>
                                <div className="ownermodal">
                                    <Button onClick={this.newUserWithEmail}>Sign Up</Button>
                                </div>
                            </form>
                        </div>
                        }
                    </div>
                }
            </div>
        );
    }
}

EmailSignup.propTypes = {
    config: React.PropTypes.object,
};