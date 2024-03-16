import { ResultSetHeader, RowDataPacket } from "mysql2"

export default interface HuntRecord extends ResultSetHeader {
    record_datetime: Date;
    active: boolean;
    total_count: number;
    total_percent: number;
    level2_count: number;
    level2_percent: number;
    level3_count: number;
    level3_percent: number;
    level4_count: number;
    level4_percent: number;
    level5_count: number;
    level5_percent: number;
}