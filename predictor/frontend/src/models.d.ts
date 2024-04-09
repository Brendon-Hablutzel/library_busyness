interface PredictionRaw {
    record_datetime: string
    total_percent: string
    total_percent_lower: string
    total_percent_upper: string
}

interface Prediction {
    record_datetime: Date
    total_percent: string
    total_percent_lower: string
    total_percent_upper: string
}

type Library = "hunt" | "hill";

export { PredictionRaw, Prediction, Library }