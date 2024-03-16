import { Router } from 'express';
import { getAll, getSince, createRecord, getRecent } from '../controllers/hill.controller';

const hillRouter = Router();

hillRouter.get('/', getAll);
hillRouter.get('/since/:since', getSince);
hillRouter.get('/recent/:limit', getRecent);
hillRouter.post('/', createRecord);

export default hillRouter;