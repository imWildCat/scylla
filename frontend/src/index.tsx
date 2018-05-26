import * as React from "react";
import * as ReactDOM from "react-dom";
import 'milligram';
import "./index.scss";
import { HashRouter as Router, NavLink, Route } from 'react-router-dom';
import ScyllaBannerImage from './images/scylla_banner.png';

import ProxyIPList from "./components/ProxyList";
import GeoDistribution from "./components/GeoDistribution";
import Statistics from "./components/Statistics";


const AppRoute = () => (
    <Router>
        <div>
            <div className="banner">
                <img src={ScyllaBannerImage} alt="banner" />
            </div>
            <ul className="navigation">
                <li><NavLink exact={true} to="/">Proxy IP List</NavLink></li>
                <li><NavLink to="/geo">Geometric Distribution</NavLink></li>
                <li><NavLink to="/stats">Statistics</NavLink></li>
            </ul>

            <Route exact path="/" component={ProxyIPList} />
            <Route path="/geo" component={GeoDistribution} />
            <Route path="/stats" component={Statistics} />
            <footer>
                <div>
                    All rights reserved. Project <a href="https://github.com/imWildCat/scylla" target="_blank">Scylla</a>.
                </div>
            </footer>
        </div>
    </Router>
);

ReactDOM.render(
    <div className="container">
        <AppRoute />
    </div>,
    document.getElementById('app')
);