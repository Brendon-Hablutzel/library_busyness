import { ResultSetHeader } from "mysql2"
import Predictions from "./predictions";

export default interface HillPred extends ResultSetHeader {
    record_datetime: Date;
    predictions: Predictions
}