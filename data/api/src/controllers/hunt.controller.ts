import { Request, Response } from 'express';
import HuntRepository from '../repositories/hunt.repository';

const getAll = (req: Request, res: Response) => {
    HuntRepository.getAll().then(records => {
        res.status(200).send({
            success: true,
            result: records
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: null
        })
    })
}

const getSince = (req: Request, res: Response) => {
    HuntRepository.getSince(req.params['since']).then(records => {
        res.status(200).send({
            success: true,
            result: records
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: null
        })
    })
}

const getRecent = (req: Request, res: Response) => {
    HuntRepository.getRecent(parseInt(req.params['limit'])).then(records => {
        res.status(200).send({
            success: true,
            result: records
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: null
        })
    })
}

const createRecord = (req: Request, res: Response) => {
    HuntRepository.createRecord(req.body).then(record => {
        res.status(200).send({
            success: true,
            result: record.affectedRows
        })
    }).catch(err => {
        res.status(500).send({
            success: false,
            error: "DATABASE ERROR",
            result: null
        })
    })
}

export { getAll, getSince, createRecord, getRecent }