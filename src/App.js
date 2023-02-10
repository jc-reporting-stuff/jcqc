import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Helmet from "react-helmet";

import methods from "./methods";
import instruments from "./instruments";

import MethodSelect from "./components/MethodSelect";
import Report from "./components/Report/index";
import Method from "./components/Method";

const App = () => {
  const [error, setError] = useState(null);
  const [data, setData] = useState();
  const [method, setMethod] = useState();
  // const savedInstrument = instruments.find(
  //   (inst) => inst.name === localStorage.getItem("instrument")
  // );
  const savedInstrument = undefined;
  const [instrument, setInstrument] = useState(
    savedInstrument || instruments[0]
  );

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
            <Report
              method={method}
              data={data}
              setError={setError}
              instrument={instrument}
            />
          </Route>

          <Route path="/:name">
            <MethodSelect
              error={error}
              method={method}
              methods={methods}
              setMethod={setMethod}
              setError={setError}
              setData={setData}
              instrument={instrument}
              instruments={instruments}
              setInstrument={setInstrument}
            />
          </Route>

          <Route path="/">
            <MethodSelect
              method={method}
              methods={methods}
              setMethod={setMethod}
              error={error}
              instrument={instrument}
              instruments={instruments}
              setInstrument={setInstrument}
            />
          </Route>
        </Switch>
      </Router>
    </div>
  );
};
export default App;
