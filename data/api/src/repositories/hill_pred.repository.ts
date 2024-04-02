import { connection } from '../config/db';
import HillPred from '../models/hill_pred.model';
import { QueryError } from 'mysql2';
import ILibraryPredRepository from './library_pred.repository';

class HillPredRepository implements ILibraryPredRepository<HillPred> {
    updatePredictions = (predictions: HillPred[]): Promise<HillPred[]> => {
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
                "insert into hill_pred (record_datetime, total_percent, total_percent_lower, total_percent_upper) values ? on duplicate key update record_datetime = values(record_datetime), total_percent = values(total_percent), total_percent_lower = values(total_percent_lower), total_percent_upper = values(total_percent_upper)",
                [insertablePredictions],
                (err: QueryError | null, res: HillPred[]) => {
                    if (err) {
                        reject(err);
                    } else {
                        return resolve(res);
                    }
                });
        });
    }

    getPredictions = (): Promise<HillPred[]> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "select * from hill_pred where record_datetime >= NOW()",
                (err: QueryError | null, res: HillPred[]) => {
                    if (err) {
                        reject(err);
                    } else {
                        return resolve(res);
                    }
                });
        });
    }
}

export default new HillPredRepository();