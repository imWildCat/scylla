import * as process from 'process'

export function getBaseURL(): string {
    return process.env['NODE_ENV'] === 'production' ? '/' : 'http://localhost:8000/';
}