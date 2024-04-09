import { NameType, ValueType } from 'recharts/types/component/DefaultTooltipContent';
import { Prediction } from './models';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, TooltipProps } from 'recharts';
import { formatRecordDatetime, formatTime } from './util';
import { useEffect } from 'react';

const tickFormatter = (tick: Date): string => {
    return (tick.getMonth() + 1).toString() +
        "/" +
        tick.getDate() +
        "T" +
        formatTime(tick.getHours()) +
        ":" +
        formatTime(tick.getMinutes())
}

interface Props extends TooltipProps<ValueType, NameType> {
    setSelectedRow: (selectedRow: Date | null) => void
}

const CustomTooltip = ({ active, payload, label, setSelectedRow }: Props) => {
    useEffect(() => {
        if (active && payload !== undefined) {
            setSelectedRow(payload[0].payload?.record_datetime);
        } else {
            setSelectedRow(null);
        }


    }, [setSelectedRow, active, payload]);

    if (active && payload && payload[0]) {
        let data = payload[0].payload;
        return (
            <div className="custom-tooltip">
                {formatRecordDatetime(data.record_datetime)}: {data.total_percent * 100}%
            </div>
        );
    }

    return null;
};

interface ChartProps {
    predictions: Prediction[]
    className: string
    setSelectedRow: (selectedRow: Date | null) => void
}

const Chart: React.FC<ChartProps> = ({ predictions, className, setSelectedRow }) => {
    return <div className={className}>
        <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={predictions}>
                <Tooltip content={<CustomTooltip setSelectedRow={setSelectedRow} />} />
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="record_datetime" tickFormatter={tickFormatter} />
                <YAxis domain={[0, 8]} />
                <Area type="monotone" dataKey="total_percent" isAnimationActive={false} />
            </AreaChart>
        </ResponsiveContainer>
    </div >
}

export default Chart;