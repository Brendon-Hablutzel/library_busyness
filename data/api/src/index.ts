import express from 'express';
import bodyParser from 'body-parser';
import routes from './routes';

const app = express();

// automatically parses json bodies
app.use(bodyParser.json());

// automatically parses url arguments
app.use(bodyParser.urlencoded({ extended: false }));

app.use('/api', routes);

const port = process.env.API_PORT || 3000;

app.listen(port, () => {
    console.log(`Listening on http://localhost:${port}`)
})
