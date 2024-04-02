import { Router } from 'express';
import { createRecord, getAll, getSince, getRecent } from '../controllers/hunt.controller';
import { getPredictions, updatePredictions } from '../controllers/hunt_pred.controller';

const huntRouter = Router();

huntRouter.get('/', getAll);
huntRouter.get('/since/:since', getSince);
huntRouter.get('/recent/:limit', getRecent);
huntRouter.post('/', createRecord);

huntRouter.get('/predictions', getPredictions);
huntRouter.post('/predictions', updatePredictions);

export default huntRouter;