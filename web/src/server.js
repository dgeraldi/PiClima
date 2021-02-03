'use strict';

const config = require('./config/env.config');
const app = require('./index');

async function startServer()
{
    app.listen(config.app.port,(err)=>{
        if(err){
            return console.log('Erro ao iniciar o server!');
        }
    console.log(`Servidor iniciado com sucesso na porta ${config.app.port}`);
    });

};
startServer();