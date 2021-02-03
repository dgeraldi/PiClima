'use strict';

const express = require('express');
const router = express.Router();

const temperatura_controller = require('../controllers/temperatura.controller');

router.get('/temp', temperatura_controller.test);

module.exports = router;