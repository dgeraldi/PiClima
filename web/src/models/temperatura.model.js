const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const schema = new Schema({
  log_temperatura: {
    datahora: String,
    temperatura: Number,
    pressao: Number,
    pressao_abs: Number,
    altitude: Number
  }
});

module.exports = mongoose.model('logTemperatura', schema);