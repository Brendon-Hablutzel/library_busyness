import { useEffect, useState } from "react";
import { formatTime, monthToString } from "./util";

const CurrentDate = () => {
    const [currentDate, setCurrentDate] = useState(new Date());

    useEffect(() => {
        setInterval(() => setCurrentDate(new Date()), 1000)
    }, []);

    let formattedDate = monthToString(currentDate.getMonth()) + " " +
        currentDate.getDate() + " at " + formatTime(currentDate.getHours()) + ":" + formatTime(currentDate.getMinutes());

    return <div id="current-date"><h2 id="current-date-text">{formattedDate}</h2></div>;
}

export default CurrentDate;