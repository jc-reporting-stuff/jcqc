import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Helmet from "react-helmet";

import methods from "./methods";

import MethodSelect from "./components/MethodSelect";
import Report from "./components/Report/index";
import Method from "./components/Method";

const App = () => {
  const [error, setError] = useState(null);
  const [data, setData] = useState();
  const [method, setMethod] = useState();

  return (
    <div>
      <Helmet>
        <meta charSet="utf-8" />
        <title>Agilent 7900 Reporting Application</title>
      </Helmet>

      <Router>
        <Switch>
          <Route path="/method">
            <Method method={method} />
          </Route>

          <Route path="/report">
            <Report method={method} data={data} setError={setError} />
          </Route>

          <Route path="/:name">
            <MethodSelect
              error={error}
              method={method}
              methods={methods}
              setMethod={setMethod}
              setError={setError}
              setData={setData}
            />
          </Route>

          <Route path="/">
            <MethodSelect
              method={method}
              methods={methods}
              setMethod={setMethod}
              error={error}
            />
          </Route>
        </Switch>
      </Router>
    </div>
  );
};
export default App;
