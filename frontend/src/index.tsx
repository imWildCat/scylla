import * as React from "react";
import * as ReactDOM from "react-dom";
import 'react-virtualized/styles.css';
import 'milligram';
import "./index.scss";
import {BrowserRouter as Router, Link, Route} from 'react-router-dom';

import ProxyIPList from "./components/ProxyList";

// import App from "./components/App";


const AppRoute = () => (
    <Router>
        <div>
            <ul>
                <li><Link to="/">ProxyIPList</Link></li>
            </ul>

            <Route exact path="/" component={ProxyIPList}/>
        </div>
    </Router>
);

ReactDOM.render(
    <div className="container">
        <AppRoute/>
    </div>,
    document.getElementById('app')
);