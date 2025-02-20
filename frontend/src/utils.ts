import * as process from 'process'

export function getBaseURL(): string {
    return process.env['NODE_ENV'] === 'production' ? prodURL() : 'http://localhost:8899';
}

function prodURL(): string {
    const location = window.location;
    return location.protocol + "//" + location.host;
}

export interface Proxy {
    id: number;
    ip: string;
    port: number;
    is_valid: boolean;
    created_at: number;
    updated_at: number;
    latency: number;
    stability: number;
    is_anonymous: boolean;
    is_https: boolean;
    location: string;
    organization: string;
    region: string;
    country: string;
    city: string;
    asn: string;
    isp: string;
    state: string;
    zipcode: string;
    latitude: number;
    longitude: number;
    timezone: string;
    localtime: string;
    is_mobile: boolean;
    is_vpn: boolean;
    is_tor: boolean;
    is_proxy: boolean;
    is_datacenter: boolean;
    risk_score: number;
}

export interface ResponseJSON {
    proxies: Proxy[];
    count: number;
    per_page: number;
    page: number;
    total_page: number;
}

export interface StatsResponseJSON {
    mean: number;
    median: number;
    total_count: number;
    valid_count: number;
}
