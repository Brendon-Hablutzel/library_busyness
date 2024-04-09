import { useEffect, useState } from 'react';
import './App.css';
import Chart from './Chart';
import { Library, Prediction, PredictionRaw } from './models';
import Description from './Description';
import PredictionsTable from './PredictionsTable';
import LibrarySelector from './LibrarySelector';
import CurrentDate from './CurrentDate';
import { getApiBaseUrl } from './util';

function parseApiResponse(predictions: PredictionRaw[]): Prediction[] {
    return predictions.map((prediction: PredictionRaw) => {
        return {
            record_datetime: new Date(prediction.record_datetime),
            total_percent: prediction.total_percent,
            total_percent_lower: prediction.total_percent_lower,
            total_percent_upper: prediction.total_percent_upper,
        }
    });
}

const App = () => {
    const [hillPredictions, setHillPredictions] = useState<Prediction[]>([]);
    const [huntPredictions, setHuntPredictions] = useState<Prediction[]>([]);
    const [domain, setDomain] = useState<{ min: number, max: number }>({ min: 0, max: 0 });
    const [tableRendered, setTableRendered] = useState(false);
    const [currentLibrary, setCurrentLibrary] = useState<Library>("hunt");
    const [selectedRow, setSelectedRow] = useState<Date | null>(null);

    function getCurrentPredictions(): Prediction[] {
        if (currentLibrary === "hunt") {
            return huntPredictions;
        } else if (currentLibrary === "hill") {
            return hillPredictions;
        } else {
            return [];
        }
    }

    useEffect(() => {
        fetch(getApiBaseUrl() + "/api/hunt/predictions").then(res => {
            return res.json();
        }).then(data => {
            let parsed = parseApiResponse(data['result']);
            setHuntPredictions(parsed);
        })
    }, []);

    useEffect(() => {
        fetch(getApiBaseUrl() + "/api/hill/predictions").then(res => {
            return res.json();
        }).then(data => {
            let parsed = parseApiResponse(data['result']);
            setHillPredictions(parsed);
        })
    }, []);

    return (
        <div className="app">
            <div className="left-container">
                <LibrarySelector setCurrentLibrary={setCurrentLibrary} />
                <CurrentDate />
                <PredictionsTable selectedRow={selectedRow} setLoadedState={setTableRendered} predictions={getCurrentPredictions()} setDomain={setDomain} />
                <Description />
            </div>

            {!tableRendered ? <div className="graph-container">Loading...</div> : <Chart setSelectedRow={setSelectedRow} className="graph-container" predictions={getCurrentPredictions().slice(domain.min, domain.max)}></Chart>}
        </div>
    );
}

export default App;