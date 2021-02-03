require('dotenv').config({ path: './web/.env'});

module.exports = {
    app:{
        port: process.env.PORT || 3000,
        mongoUser: process.env.MONGO_USER,
        mongoSecret: process.env.MONGO_SECRET,
        mongoDB: process.env.MONGO_DB,
        mongoCol: process.env.MONGO_COLLECTION
    },
};