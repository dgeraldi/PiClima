const MongoClient = require("mongodb").MongoClient;
const config = require('../config/env.config');


const uri = `mongodb+srv://${config.app.mongoUser}:${config.app.mongoSecret}@cluster0.tdpte.mongodb.net/${config.app.mongoDB}?retryWrites=true&w=majority`;

// Create a new MongoClient
const client = new MongoClient(uri,{ useUnifiedTopology: true });

async function connectMongo(){
  try {
    // Connect the client to the server
    await client.connect();
    
    // Establish and verify connection
    await client.db(config.app.mongoDB).command({ ping: 1 });
    console.log("Connected successfully to server");

    const collection = client.db().collection(config.app.mongoCol);
    // Query for a movie that has the title 'Back to the Future'
    const query = {altitude: 800};
    
    const result = await collection.findOne(query);
    console.log(result);

    collection.find(query,{limit:10}).toArray(function (err, items) {
          if (err)
              throw err;
          console.log(items);
      });

  }finally{
    await client.close();
    }
};

connectMongo().catch(console.dir);