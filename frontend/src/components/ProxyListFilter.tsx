import * as React from 'react';
import {Link} from "react-router-dom";
import queryString from "query-string";

export interface ProxyListFilterProps {
    location: any;
}

export interface ProxyListFilterState {
    https: boolean | null;
    anonymous: boolean | null;
}

export default class ProxyListFilter extends React.Component<ProxyListFilterProps, ProxyListFilterState> {
    constructor(props: ProxyListFilterProps) {
        super(props);

        this.state = {
            https: null,
            anonymous: null,
        }
    }

    render() {
        return (
            <div className="filter">
                <Link to={this.genLink('HTTPS')} className={this.genClassName('HTTPS')}>HTTPS</Link>
                <Link to={this.genLink('ANONYMOUS')} className={this.genClassName('ANONYMOUS')}>ANONYMOUS</Link>
            </div>
        );
    }

    componentDidMount() {
        this.handleProps(this.props);
    }

    componentWillReceiveProps(nextProps: ProxyListFilterProps) {
        this.handleProps(nextProps);
    }

    handleProps(props: ProxyListFilterProps) {
        const parsed = queryString.parse(props.location.search);

        const https = parsed['https'] == 'true' ? true : null;
        const anonymous = parsed['anonymous'] == 'true' ? true : null;

        this.setState({https: https, anonymous: anonymous})
    }

    genLink(key: string): string {

        const {anonymous, https} = this.state;
        let params: any = {
            anonymous,
            https,
        };

        if (key === 'HTTPS') {
            params['https'] = https == true ? null : true;
        } else if (key === 'ANONYMOUS') {
            params['anonymous'] = anonymous == true ? null : true;
        }


        return `/?${queryString.stringify(params)}`;
    }


    genClassName(key: string): string {
        const {anonymous, https} = this.state;

        let baseClassName = 'button';

        if (key === 'HTTPS') {
            if (!https) {
                baseClassName += ' button-outline'
            }
        } else if (key === 'ANONYMOUS') {
            if (!anonymous) {
                baseClassName += ' button-outline'
            }
        }
        return baseClassName;
    }

}
