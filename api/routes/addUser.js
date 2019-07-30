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
    res.send('API is working properly');
});

router.post('/', function(req, res, next) {

    var firstName = req.body.first;
    var lastName = req.body.last;
    var email = req.body.email;

    var connectionString = 'mongodb://' + loginData.user + ':' + loginData.password + '@' + loginData.host;

    mongoose.connect(connectionString, {useNewUrlParser: true});
    var db = mongoose.connection;

    db.on('error', console.error.bind(console, 'connection error:'));
    db.once('open', function() {

        /*var userSchema = new mongoose.Schema({
            First: String,
            Last: String,
            Email: String,
            Birthday: String
        });

        var User = mongoose.model('User', userSchema);*/

        var currentUser = new User({
            First: firstName,
            Last: lastName,
            Email: email,
            Birthday: ''
        });

        User.find({ Email: email }, function (err, matches) {
            console.log(matches);
            console.log('matches.length: ' + matches.length);

            if (matches.length > 0) {
                res.send('repeat');
                db.close();
                return;
            }
        });

        currentUser.save(function (err, event) {
            if (err) {
		        res.send('failure');
                db.close();
                return console.error(err);10
            } else {
                db.close();
                res.send('success');
            }
        })
    });

});

module.exports = router;
