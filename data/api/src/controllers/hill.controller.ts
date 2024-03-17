import { Request, Response } from 'express';
import HillRepository from '../repositories/hill.repository';

const getAll = (req: Request, res: Response) => {
    HillRepository.getAll().then(records => {
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

const getSince = (req: Request, res: Response) => {
    HillRepository.getSince(req.params['since']).then(records => {
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

const getRecent = (req: Request, res: Response) => {
    HillRepository.getRecent(parseInt(req.params['limit'])).then(records => {
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


const createRecord = (req: Request, res: Response) => {
    HillRepository.createRecord(req.body).then(record => {
        res.status(200).send({
            success: true,
            result: record.affectedRows
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: err
        })
    })
}

export { getAll, getSince, createRecord, getRecent }
