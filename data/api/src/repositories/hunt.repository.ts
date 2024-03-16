import { connection } from '../config/db';
import HuntRecord from '../models/hunt.model';
import { QueryError } from 'mysql2';
import ILibraryRepository from './library.repository';


class HuntRepository implements ILibraryRepository<HuntRecord> {
    getAll = (): Promise<HuntRecord[]> => {
        return new Promise((resolve, reject) => {
            connection.query("select * from hunt", (err: QueryError | null, res: HuntRecord[]) => {
                if (err) {
                    reject(err)
                } else {
                    return resolve(res)
                }
            });
        });
    }

    getSince = (since: string): Promise<HuntRecord[]> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "select * from hunt where record_datetime >= ?",
                [since],
                (err: QueryError | null, res: HuntRecord[]) => {
                    if (err) {
                        reject(err)
                    } else {
                        return resolve(res)
                    }
                }
            );
        });
    }

    getRecent = (limit: number): Promise<HuntRecord[]> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "select * from hunt order by record_datetime desc limit ?",
                [limit],
                (err: QueryError | null, res: HuntRecord[]) => {
                    if (err) {
                        reject(err)
                    } else {
                        return resolve(res)
                    }
                }
            )
        });
    }

    createRecord = (record: HuntRecord): Promise<HuntRecord> => {
        return new Promise((resolve, reject) => {
            connection.query(
                "insert into hunt(record_datetime, active, total_count, total_percent, level2_count, level2_percent, level3_count, level3_percent, level4_count, level4_percent, level5_count, level5_percent) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [record.record_datetime, record.active, record.total_count, record.total_percent, record.level2_count, record.level2_percent, record.level3_count, record.level3_percent, record.level4_count, record.level4_percent, record.level5_count, record.level5_percent],
                (err: QueryError | null, res: HuntRecord) => {
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

export default new HuntRepository();