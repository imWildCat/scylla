import * as React from "react";
import * as ReactDOM from "react-dom";
import 'react-virtualized/styles.css';
import 'milligram';
import "./index.scss";

import ProxyIPList from "./components/ProxyList";

// import App from "./components/App";

ReactDOM.render(
    <div className="container">
        <ProxyIPList/>
    </div>,
    document.getElementById('app')
);