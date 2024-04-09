const formatTime = (num: number): string => {
    if (num < 10) {
        return "0" + num.toString();
    } else {
        return num.toString();
    }
}

function formatRecordDatetime(datetime: Date): string {
    return datetime.getMonth() + 1 + "/" + datetime.getDate() + " at " + formatTime(datetime.getHours()) + ":" + formatTime(datetime.getMinutes());
}

function monthToString(month: number): string {
    month++;

    switch (month) {
        case 1:
            return "January"
        case 2:
            return "February"
        case 3:
            return "March"
        case 4:
            return "April"
        case 5:
            return "May"
        case 6:
            return "June"
        case 7:
            return "July"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "October"
        case 11:
            return "November"
        case 12:
            return "December"
        default:
            return ""
    }
}

const getApiBaseUrl = (): string => {
    let apiHost = process.env.REACT_APP_API_HOST || "";
    let apiPort = process.env.REACT_APP_API_PORT || "";

    return `http://${apiHost}:${apiPort}`;
}

export { formatTime, formatRecordDatetime, monthToString, getApiBaseUrl };