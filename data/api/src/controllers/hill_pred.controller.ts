import { Request, Response } from 'express';
import HillPredRepository from '../repositories/hill_pred.repository';

const updatePredictions = (req: Request, res: Response) => {
    HillPredRepository.updatePredictions(req.body).then(records => {
        res.status(200).send({
            success: true,
            result: records
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: err
        })
    })
}

const getPredictions = (req: Request, res: Response) => {
    HillPredRepository.getPredictions().then(records => {
        res.status(200).send({
            success: true,
            result: records
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: err
        })
    })
}

export { updatePredictions, getPredictions }