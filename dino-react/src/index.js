import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';

function NavBar(props) {
    return (
    <nav className="navbar navbar-expand-lg navbar-light">
        <a className="navbar-brand" href="{null}">
            <img src={require("./img/egg.svg")} width="30" height="30" alt="" className="d-inline-block align-top nav-nail"/>
            Dino of the Day
        </a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
                <li className="nav-item active">
                    <a className="nav-link" href="{null}"> Home </a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" href="{null}"> About </a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" href="{null}"> Subscribe </a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" href="{null}"> Contact </a>
                </li>
                <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="{null}" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Media</a>
                    <div className="dropdown-menu dropdown-menu-lg-left" aria-labelledby="navbarDropdown">
                        <a className="dropdown-item" href="{null}">Instagram</a>
                        <a className="dropdown-item" href="{null}">Twitter</a>
                    </div>
                </li>
            </ul>

            <span className="navbar-text mr-auto">
                Heading tagline would go here
            </span>

            <form className="form-inline my-2 my-lg-0">
                <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                <button className="btn btn-outline-dark my-2 my-sm-0" type="submit">Search</button>
            </form>

        </div>
    </nav>
    );
}

function Introduction(props) {
    return (
        <div className="row justify-content-md-center">
            <div className="jumbotron mx-4 my-4 col-xl-4 col-lg-8 col-md-10 col-sm-10 col-xs-10">

                <h1 className="display-3"> Dino of the Day </h1>

                <hr className="my-4" ></hr>

                <p className="lead">
                    Welcome to Dino of the Day, the only website that brings you a different dino every single day!
                </p>
            </div>
        </div>
    );
}

class SignupForm extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            user: {
                firstName: '',
                lastName: '',
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
        var alertMessage = 'First: ' + this.state.user.firstName +
                       '\nLast: ' + this.state.user.lastName +
                       '\nEmail: ' + this.state.user.email;
        alert(alertMessage);
        event.preventDefault();

        var postData = {
            first: this.state.user.firstName,
            last: this.state.user.lastName,
            email: this.state.user.email
        }

        var userURL = 'http://localhost:9000/addUser';

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

                    <h1 className="display-3"> Join the Mailing List </h1>

                    <hr className="my-4"></hr>

                    <div className="form-group">
                        <form onSubmit={this.handleSubmit}>

                            <label
                                className="justify-left"
                                htmlFor="firstName"
                            >First Name</label>
                            <input
                                type="text"
                                value={this.state.firstName}
                                onChange={this.handleChange.bind(this, 'firstName')}
                                className="form-control"
                                placeholder="Enter First Name"
                            />

                            <label
                                className="justify-left"
                                htmlFor="lastName"
                            >Last Name</label>
                            <input
                                type="text"
                                value={this.state.lastName}
                                onChange={this.handleChange.bind(this, 'lastName')}
                                className="form-control"
                                placeholder="Enter Last Name"
                            />

                            <label
                                className="justify-left"
                                htmlFor="lastName"
                            >Email</label>
                            <input
                                type="text"
                                value={this.state.email}
                                onChange={this.handleChange.bind(this, 'email')}
                                className="form-control"
                                placeholder="Enter Email"
                            />

                            <button type="submit" className="btn btn-primary my-4">Submit</button>

                            <p>
                                {this.state.apiResponse}
                            </p>

                        </form>
                    </div>

                </div>
            </div>
        );
    }
}

class App extends React.Component {
    render() {
        return (
            <div>
                <NavBar />
                <Introduction />
                <SignupForm />
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);
