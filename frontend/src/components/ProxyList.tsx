import * as React from "react";
import axios from 'axios';
import {Link} from 'react-router-dom';

import {getBaseURL, Proxy, ResponseJSON} from '../utils';
import * as queryString from "query-string";
import ProxyListFilter from "./ProxyListFilter";

import moment from 'moment'

export interface AppState {
    proxies: Proxy[];
    count: number;
    per_page: number;
    page: number;
    total_page: number;
}

export interface Props {
    location: any;
}

export default class ProxyIPList extends React.Component<Props, AppState> {
    private initialState: AppState = {
        proxies: [],
        count: 0,
        per_page: 0,
        page: 0,
        total_page: 0,
    };

    constructor(props: Props) {
        super(props);
        this.state = this.initialState;
    }

    render(): JSX.Element {
        // const { timesClicked, on } = this.state;
        return (
            <div>
                {this.renderPagination()}
                {this.renderList()}
                {this.renderPagination()}
            </div>
        );
    }

    renderList(): JSX.Element {
        const list = this.state.proxies;
        return (
            <div>
                <ProxyListFilter location={this.props.location}/>
                <table>
                    <thead>
                    <tr>
                        <th>IP</th>
                        <th>Port</th>
                        <th>Anonymous</th>
                        <th>Protocol</th>
                        <th>Latency</th>
                        <th>Updated at</th>
                    </tr>
                    </thead>
                    <tbody>
                    {list.map(r =>
                        <tr key={`ip-` + r.ip}>
                            <td>{r.ip}</td>
                            <td>{r.port}</td>
                            <td>{r.is_anonymous ? 'Yes' : 'No'}</td>
                            <td>{r.is_https ? 'HTTPS' : 'HTTP'}</td>
                            <td>{r.latency.toFixed(0)} ms</td>
                            <td>{moment(r.updated_at).format('YYYYMMDD HH:mm:ss')}</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        );
    }

    componentDidMount() {
        this.loadData(this.props);
    }

    componentWillReceiveProps(nextProp: any) {
        this.loadData(nextProp)
    }

    async loadData(props: any) {
        const parsed = queryString.parse(props.location.search);

        const page = parsed['page'] || 1;
        const https = parsed['https'] || null;
        const anonymous = parsed['anonymous'] || null;

        const params: any = {};

        if (page) {
            params['page'] = page;
        }

        if (https) {
            params['https'] = https;
        }

        if (anonymous) {
            params['anonymous'] = anonymous;
        }

        const response = await axios.get(`${getBaseURL()}/api/v1/proxies?${queryString.stringify(params)}`);
        const res: ResponseJSON = response.data;
        const proxies: Proxy[] = res.proxies;
        this.setState({
            proxies: proxies,
            count: res.count,
            per_page: res.per_page,
            page: res.page,
            total_page: res.total_page,
        });
    }

    renderPagination(): JSX.Element {
        const {total_page, page} = this.state;

        const pagination = [];

        if (page !== 1) {
            pagination.push(this.renderPageLink(page - 1, 'Previous page'))
        }

        if (page !== total_page) {
            pagination.push(this.renderPageLink(page + 1, 'Next page'))
        }

        return (
            <ul className="pagination">
                {pagination.map(e => e)}
            </ul>
        )
    }

    private renderPageLink(pageNumber: number, label: string): JSX.Element {
        const parsed = queryString.parse(this.props.location.search);

        parsed['page'] = pageNumber;

        return (
            <li key={`page-nav-${pageNumber}`}><Link to={`/?${queryString.stringify(parsed)}`}>{label}</Link></li>
        );
    }

}