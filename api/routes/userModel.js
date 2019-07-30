var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var userSchema = new mongoose.Schema({
    First: String,
    Last: String,
    Email: String,
    Birthday: String
});

module.exports = mongoose.model('users', userSchema);
