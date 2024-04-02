import { Router } from 'express';
import { getAll, getSince, createRecord, getRecent } from '../controllers/hill.controller';
import { getPredictions, updatePredictions } from '../controllers/hill_pred.controller';

const hillRouter = Router();

hillRouter.get('/', getAll);
hillRouter.get('/since/:since', getSince);
hillRouter.get('/recent/:limit', getRecent);
hillRouter.post('/', createRecord);

hillRouter.get('/predictions', getPredictions);
hillRouter.post('/predictions', updatePredictions);

export default hillRouter;