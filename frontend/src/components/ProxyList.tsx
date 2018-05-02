import * as React from "react";
import axios from 'axios';
import {AutoSizer, Column, Table} from 'react-virtualized';

// import * as moment from 'moment';
const moment = require('moment')['default'];

export interface AppState {
    proxies: Array<any>,
}

export default class ProxyIPList extends React.Component<{}, AppState> {
    private initialState: AppState = {proxies: []};

    constructor(props: {}) {
        super(props);
        this.state = this.initialState;
    }

    render(): JSX.Element {
        // const { timesClicked, on } = this.state;
        return (
            <div>
                proxy ip list

                {this.renderList()}
            </div>
        );
    }

    renderList(): JSX.Element {

        const list = this.state.proxies;

        return (
            <AutoSizer disableHeight={true}>
                {({width}) => (
                    <Table
                        width={width}
                        height={500}
                        headerHeight={20}
                        rowHeight={30}
                        rowCount={list.length}
                        rowGetter={({index}) => list[index]}
                    >
                        <Column
                            label='IP'
                            dataKey='ip'
                            width={200}
                        />
                        <Column
                            width={50}
                            label='Port'
                            dataKey='port'
                        />
                        <Column
                            width={150}
                            label='Anonymous'
                            dataKey='is_anonymous'
                        />
                        <Column
                            width={100}
                            label='Latency'
                            dataKey='latency'
                            cellRenderer={({cellData}) => {
                                const d = Math.round(cellData);
                                return d + ' ms';
                            }}
                        />
                        <Column
                            width={150}
                            label='Time'
                            dataKey='updated_at'
                            cellRenderer={({cellData}) => {
                                const d = moment.unix(cellData).format('YYYYMMDD HH:mm:ss');
                                return d;
                            }}
                        />
                    </Table>
                )}
            </AutoSizer>
        );
    }

    componentDidMount() {
        this.loadData();
    }

    async loadData() {
        const response = await axios.get('http://localhost:8000/api/v1/proxies');
        const proxies: [any] = response.data.proxies;
        console.log(proxies);
        this.setState({proxies: proxies})
    }

}