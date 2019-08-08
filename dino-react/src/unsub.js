import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';

function Information(props) {
    return (
        <div className="row justify-content-md-center">
            <div className="jumbotron mx-4 my-4 col-xl-4 col-lg-8 col-md-10 col-sm-10 col-xs-10">

                <h1 className="display-3"> Unsubscribe </h1>

                <hr className="my-4" ></hr>

                <p className="lead">
                    Hi there! We're sorry to see you go, but we hope your future is filled with many fun times learning about dinosaurs and receiving newsletters!
                </p>
            </div>
        </div>
    );
}

class UnSubForm extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            user: {
                email: ''
            },
            apiResponse: ''
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(propertyName, event) {

        const user = this.state.user;
        user[propertyName] = event.target.value;

        this.setState({
            user: user
        });
    }

    handleSubmit(event) {

        event.preventDefault();

        var postData = {
            email: this.state.user.email
        }

        var userURL = 'https://dinogram.org:9010/removeUser';

        fetch(userURL, {
            method: 'POST',
            body: JSON.stringify(postData),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.text())
            .then(res => this.setState({
                apiResponse: res
            }))
            .catch(err => err);
    }

    render() {
        return (

            <div className="row justify-content-md-center">
                <div className="jumbotron mx-4 my-4 col-xl-4 col-lg-8 col-md-10 col-sm-10 col-xs-10">

                    <h1 className="display-3"> Leave the Mailing List </h1>

                    <hr className="my-4"></hr>

                    <div className="form-group">
                        <form onSubmit={this.handleSubmit}>

                            <label
                                className="justify-left"
                                htmlFor="email"
                            >Email</label>
                            <input
                                type="text"
                                value={this.state.email}
                                onChange={this.handleChange.bind(this, 'email')}
                                className="form-control"
                                placeholder="Enter Email"
                            />

                            <button type="submit" className="btn btn-primary my-4">Submit</button>

                            {this.state.apiResponse === "success" &&
                                <div className="alert alert-primary" role="alert">
                                    You've been successfully removed from the mailing list!
                                </div>
                            }
                            {this.state.apiResponse === "notfound" &&
                                <div className="alert alert-danger" role="alert">
                                    You don't appear to be on the mailing list.
                                </div>
                            }
                            
                        </form>
                    </div>

                </div>
            </div>
        );
    }
}

class UnSub extends React.Component {
    render() {
        return (
            <div>
                {/*<NavBar />*/}
                <Information />
                <UnSubForm />
            </div>
        );
    }
}

export default UnSub
