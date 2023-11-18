import * as React from 'react';
import axios from "axios";
import {getBaseURL, StatsResponseJSON} from "../utils";

export interface StatisticsProps {
}

export interface StatisticsState {
    mean: number;
    median: number;
    total_count: number;
    valid_count: number;
}

export default class Statistics extends React.Component<StatisticsProps, StatisticsState> {
    constructor(props: StatisticsProps) {
        super(props);

        this.state = {
            mean: 0,
            median: 0,
            total_count: 0,
            valid_count: 0,
        }
    }

    render() {
        const {mean, median, total_count, valid_count} = this.state;

        return (
            <div>
                At present, the system has crawled:
                <ul>
                    <li>
                        <b>{total_count}</b> proxy ips in total,
                    </li>
                    <li>
                        <b>{valid_count}</b> of them are valid.
                    </li>
                    <li>The mean latency of them is: <b>{mean.toFixed(2)}</b> ms</li>
                    <li>The median latency of them is: <b>{median.toFixed(2)}</b> ms</li>
                </ul>
            </div>
        );
    }

    componentDidMount() {
        this.loadData()
    }

    async loadData() {
        const response = await axios.get(`${getBaseURL()}/api/v1/stats`);
        const res: StatsResponseJSON = response.data;
        this.setState({
            mean: res.mean,
            median: res.median,
            total_count: res.total_count,
            valid_count: res.valid_count,
        });
    }
}
