import * as React from "react";
import * as ReactDOM from "react-dom";
import 'milligram';
import "./index.scss";
import ScyllaBannerImage from './assets/scylla_banner.png';

import ProxyIPList from "./components/ProxyList";
import GeoDistribution from "./components/GeoDistribution";
import Statistics from "./components/Statistics";

import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';

export const AppRoute = () => (
    <Router>
        <div>
            <div className="banner">
                <img src={ScyllaBannerImage.replace('..', '')} alt="banner" />
            </div>
            <ul className="navigation">
                <li><NavLink to="/">Proxy IP List</NavLink></li>
                <li><NavLink to="/geo">Geometric Distribution</NavLink></li>
                <li><NavLink to="/stats">Statistics</NavLink></li>
            </ul>

            <Routes>
                <Route path="/" element={<ProxyIPList location={"fixme"} />} />
                <Route path="/geo" element={<GeoDistribution />} />
                <Route path="/stats" element={<Statistics />} />
            </Routes>

            <footer>
                <div>
                    All rights reserved. Project <a href="https://github.com/imWildCat/scylla" target="_blank">Scylla</a>.
                </div>
            </footer>
        </div>
    </Router>
);
