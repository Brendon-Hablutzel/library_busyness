import { connection } from '../config/db';
import HuntPred from '../models/hunt_pred.model';
import { QueryError } from 'mysql2';
import ILibraryPredRepository from './library_pred.repository';

class HuntPredRepository implements ILibraryPredRepository<HuntPred> {
    updatePredictions = (predictions: HuntPred[]): Promise<HuntPred[]> => {
        let insertablePredictions = predictions.map(pred => {
            return [
                pred.record_datetime,
                pred.predictions.total_percent,
                pred.predictions.total_percent_lower,
                pred.predictions.total_percent_upper
            ]
        });
        return new Promise((resolve, reject) => {
            connection.query(
                "insert into hunt_pred (record_datetime, total_percent, total_percent_lower, total_percent_upper) values ? on duplicate key update record_datetime = values(record_datetime), total_percent = values(total_percent), total_percent_lower = values(total_percent_lower), total_percent_upper = values(total_percent_upper)",
                [insertablePredictions],
                (err: QueryError | null, res: HuntPred[]) => {
                    if (err) {
                        reject(err);
                    } else {
                        return resolve(res);
                    }
                });
        });
    }

    getPredictions = (): Promise<HuntPred[]> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "select * from hunt_pred where record_datetime >= NOW()",
                (err: QueryError | null, res: HuntPred[]) => {
                    if (err) {
                        reject(err);
                    } else {
                        console.log(res);
                        return resolve(res);
                    }
                });
        });
    }
}

export default new HuntPredRepository();