var mongoose = require('mongoose');
var express = require('express');
var router = express.Router();

var options = require('../config/options');
var User = require('./userModel.js');

var loginData = {
    host: options.storageConfig.host,
    user: options.storageConfig.user,
    password: options.storageConfig.password
};

router.get('/', function(req, res, next) {
    res.send('Make a post request here to remove a user');
});

router.post('/', function(req, res, next) {

    var email = req.body.email;

    var connectionString = 'mongodb://' + loginData.user + ':' + loginData.password + '@' + loginData.host;

    mongoose.connect(connectionString, {useNewUrlParser: true});
    var db = mongoose.connection;

    db.on('error', console.error.bind(console, 'connection error:'));
    db.once('open', function() {

        User.remove({ Email: email }, function (err, matches) {
            console.log(matches);
            console.log('matches.length: ' + matches.length);

            if (!err) {
                res.send('success');
            } else {
                res.send('notfound');
            }

        });

    });

});

module.exports = router;
