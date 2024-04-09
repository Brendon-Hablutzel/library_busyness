import { useCallback, useEffect, useState } from "react"
import { Prediction } from "./models"
import { formatRecordDatetime } from "./util"

interface PredictionsTableProps extends React.HTMLProps<HTMLDivElement> {
    predictions: Prediction[]
    setLoadedState: (isLoaded: boolean) => void
    setDomain: (domain: { min: number, max: number }) => void
    selectedRow: Date | null
}

const PredictionsTable = ({ predictions, setLoadedState, setDomain, selectedRow }: PredictionsTableProps) => {
    const [recordElement, setRecordElement] = useState<HTMLDivElement>();
    const [containerElement, setContainerElement] = useState<HTMLDivElement>();

    const handleContainer = useCallback((node: HTMLDivElement | null) => { if (node != null) { setContainerElement(node) } }, []);
    const handleRecord = useCallback((node: HTMLDivElement | null) => { if (node != null) { setRecordElement(node) } }, []);

    const updateDomain = useCallback((containerElement: HTMLDivElement, recordElement: HTMLDivElement) => {
        let firstVisibleRecordIdx = containerElement.scrollTop / recordElement.clientHeight;
        firstVisibleRecordIdx = Math.floor(firstVisibleRecordIdx);

        let numVisibleRecords = containerElement.clientHeight / recordElement.clientHeight;
        numVisibleRecords = Math.ceil(numVisibleRecords);

        setDomain({ min: firstVisibleRecordIdx, max: firstVisibleRecordIdx + numVisibleRecords });
    }, [setDomain]);

    useEffect(() => {
        if (recordElement != null && containerElement != null) {
            updateDomain(containerElement, recordElement);
            setLoadedState(true);
        }
    }, [recordElement, containerElement, setLoadedState, updateDomain]);

    return <div
        className="table"
        style={{
            overflowY: "scroll",
            border: "1px solid #ccc",
        }}
        ref={handleContainer}
        onScroll={() => {
            if (containerElement != null && recordElement != null) {
                updateDomain(containerElement, recordElement);
            }
        }}
    >
        {predictions.map((prediction, idx) => {
            let className = "predict-record" + (selectedRow === prediction.record_datetime ? " selected-record" : "");
            return <div ref={idx === 0 ? handleRecord : null} key={prediction.record_datetime.valueOf()} className={className}>
                <span>{formatRecordDatetime(prediction.record_datetime)}</span>
                <span>{prediction.total_percent}</span>
            </div>;
        })}
    </div >
}

export default PredictionsTable;