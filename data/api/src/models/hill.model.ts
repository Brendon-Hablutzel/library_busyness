import { ResultSetHeader, RowDataPacket } from "mysql2"

export default interface HillRecord extends ResultSetHeader {
    record_datetime: Date;
    active: boolean;
    total_count: number;
    total_percent: number;
    east_count: number;
    east_percent: number;
    tower_count: number;
    tower_percent: number;
    west_count: number;
    west_percent: number;
}