var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
    res.send('API is working properly');
});

router.post('/', function(req, res, next) {

    var firstName = req.body.first;
    var lastName = req.body.last;
    var email = req.body.email;

    var responseString = 'Backend response: ' +
                         '\nFirst: ' + firstName +
                         '\nLast:  ' + lastName +
                         '\nEmail: ' + email;

    // This is where we would send this data to the MongoDB

    res.send(responseString);
});

module.exports = router;
