const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');
// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect(database_to_use) {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: '06ai-P7sXy6ktpM90glcn2q8IleSHKTaZ7x1whp7TQP4' } }, // Replace with your IAM API key
            url: 'https://apikey-v2-1idq9ptiz6fqglizwpenj74deckaon8rb07ljcc4y29r:65356efd3cc57ded83d59bf9c98f8dcb@448de67d-c72d-4a8f-971b-30303d11b3b7-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });
        const db = cloudant.use(database_to_use);
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}
let db;
(async () => {
    db = await dbCloudantConnect("dealerships");
})();

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get('/api/dealerships/get', (req, res) => {
    const { state, id } = req.query;
    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }
    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };
    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            
            if (body.docs.length==0)
                res.status(404).json({ 404: 'Dealer does not exist' });
            else{
                const dealerships = body.docs;
                res.json(dealerships);
            }
        }
    });
});

let db_review;
(async () => {
    db_review = await dbCloudantConnect("reviews");
})();

app.get('/api/reviews', (req, res) => {
    const { dealerId } = req.query;
    // Create a selector object based on query parameters
    const selector = {};
    if (dealerId) {
        selector.dealership = parseInt(dealerId); // Filter by "id" with a value of 1
    }
    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };
    db_review.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching reviews:', err);
            res.status(500).json({ error: 'An error occurred while fetching reviews.' });
        } else {
            
            if (body.docs.length==0)
                res.status(404).json({ 404: 'Reviews does not exist' });
            else{
                const reviews = body.docs;
                res.json(reviews);
            }
        }
    });
});

app.post("/review", function (request, response) {
    myDocument = request.body;     
    db_review.insert(myDocument, function(err, myDocument){
        if (err) {
            response.status(500).json({ error: 'An error occurred while posting review.' });
          }
          response.status(200).json({ msg: 'Review posted!' });
    })
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});