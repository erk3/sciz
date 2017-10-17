/* DEPENDENCIES */
const express = require('express'),
      bodyParser = require('body-parser'),
      methodOverride = require('method-override'),
      morgan = require('morgan'),
      sequelize = require('sequelize'),
      passport = require('passport'),
      jwt = require('jsonwebtoken'),
      path = require('path');


/* CONF LOADING */

try {
    config = require('./config.js')
} catch (err) {
    console.error('config.js loading failed')
    throw err;
}

/* MAIN STARTUP */

const app = express();

// Set server capabilities
app.use(bodyParser.urlencoded({'extended': 'true'}));
app.use(bodyParser.json({type: 'application/vnd.api+json'}));
app.use(bodyParser.json());
app.use(methodOverride('X-HTTP-Method-Override'));

// Hook up the HTTP logger
app.use(morgan('dev'));

// Hook the passport JWT strategy
var hookJWTStrategy = require('./private/services/passportStrategy.js');
hookJWTStrategy(passport);

// Set the API routes
app.use('/api', require('./private/routes/api.js')(passport));

// Set AngularJS app path
app.use(express.static('./dist-public'));

// Catch all non-api routes and send them to AngularJS app
app.get('*', function (req, res) {
    res.sendFile(path.join(__dirname, './dist-public/', 'index.html'));
});

// Start the server
app.listen(config.server.port_server);

console.log("App listening on port " + config.server.port_server);
