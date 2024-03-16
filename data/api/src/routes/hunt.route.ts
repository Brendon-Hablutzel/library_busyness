import { Router } from 'express';
import { createRecord, getAll, getSince, getRecent } from '../controllers/hunt.controller';

const huntRouter = Router();

huntRouter.get('/', getAll);
huntRouter.get('/since/:since', getSince);
huntRouter.get('/recent/:limit', getRecent);
huntRouter.post('/', createRecord);

export default huntRouter;