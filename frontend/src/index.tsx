import * as React from "react";
import * as ReactDOM from "react-dom";
import 'react-virtualized/styles.css';
import 'milligram';
import "./index.scss";
import {BrowserRouter as Router, NavLink, Route} from 'react-router-dom';

import ProxyIPList from "./components/ProxyList";
import GeoDistribution from "./components/GeoDistribution";

// import App from "./components/App";


const AppRoute = () => (
    <Router>
        <div>
            <ul className="navigation">
                <li><NavLink exact={true} to="/">Proxy IP List</NavLink></li>
                <li><NavLink to="/geo">Geometric Distribution</NavLink></li>
            </ul>

            <Route exact path="/" component={ProxyIPList}/>
            <Route path="/geo" component={GeoDistribution}/>
        </div>
    </Router>
);

ReactDOM.render(
    <div className="container">
        <AppRoute/>
    </div>,
    document.getElementById('app')
);