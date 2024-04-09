import express from 'express';
import bodyParser from 'body-parser';
import routes from './routes';
import cors from 'cors';

const app = express();

app.use(cors());

// automatically parses json bodies
app.use(bodyParser.json());

// automatically parses url arguments
app.use(bodyParser.urlencoded({ extended: false }));

// logging
app.use((req, res, next) => {
    let currentDateTime = new Date();
    // prints in UTC time
    console.log(currentDateTime.toISOString(), req.ip, req.method, req.hostname, req.path);
    next();
})

app.use('/api', routes);

const port = process.env.API_PORT || 3000;

app.listen(port, () => {
    console.log(`Listening on http://localhost:${port}`)
})
