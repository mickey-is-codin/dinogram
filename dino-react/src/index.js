import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'

import App from './App';
import UnSub from './unsub';

import './index.css';

//var https = require('https');

const routing = (
    <Router>
        <div>
            <Route exact path="/" component={App} />
            <Route path="/unsub" component={UnSub} />
        </div>
    </Router>
)

ReactDOM.render(routing, document.getElementById('root'))
