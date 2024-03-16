import { Router } from 'express';
import hillRouter from './hill.route';
import huntRouter from './hunt.route';

// base router
const routes = Router();

routes.use('/hill', hillRouter);
routes.use('/hunt', huntRouter);

export default routes;