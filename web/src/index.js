'use strict';

const path = require('path');
const express = require("express");
const app = express();

//Rotas
const index = require('./routes/index');
const temperatura = require('./routes/temperatura');

app.use(express.static(path.join(__dirname, '../public')));
app.use('/',index);
app.use('/temp', temperatura);

module.exports = app;