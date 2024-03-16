import { connection } from '../config/db';
import HillRecord from '../models/hill.model';
import { QueryError } from 'mysql2';
import ILibraryRepository from './library.repository';


class HillRepository implements ILibraryRepository<HillRecord> {
    getAll = (): Promise<HillRecord[]> => {
        return new Promise((resolve, reject) => {
            connection.query("select * from hill", (err: QueryError | null, res: HillRecord[]) => {
                if (err) {
                    reject(err)
                } else {
                    return resolve(res)
                }
            });
        });
    }

    getSince = (since: string): Promise<HillRecord[]> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "select * from hill where record_datetime >= ?",
                [since],
                (err: QueryError | null, res: HillRecord[]) => {
                    if (err) {
                        reject(err)
                    } else {
                        return resolve(res)
                    }
                }
            )
        });
    }

    getRecent = (limit: number): Promise<HillRecord[]> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "select * from hill order by record_datetime desc limit ?",
                [limit],
                (err: QueryError | null, res: HillRecord[]) => {
                    if (err) {
                        reject(err)
                    } else {
                        return resolve(res)
                    }
                }
            )
        });
    }

    createRecord = (record: HillRecord): Promise<HillRecord> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "insert into hill(record_datetime, active, total_count, total_percent, east_count, east_percent, tower_count, tower_percent, west_count, west_percent) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [record.record_datetime, record.active, record.total_count, record.total_percent, record.east_count, record.east_percent, record.tower_count, record.tower_percent, record.west_count, record.west_percent],
                (err: QueryError | null, res: HillRecord) => {
                    if (err) {
                        reject(err)
                    } else {
                        return resolve(res)
                    }
                }
            )
        })
    }
}



export default new HillRepository();