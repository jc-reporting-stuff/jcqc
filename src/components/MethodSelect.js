import React, { useEffect } from "react";
import { Link, useParams } from "react-router-dom";

import Method from "./Method";
import FileSelector from "./FileSelector";

const MethodSelect = ({
  error,
  method,
  methods,
  setData,
  setError,
  setMethod
}) => {
  const nameFromUrl = useParams().name;
  useEffect(() => {
    if (nameFromUrl && methods) {
      setMethod(methods.find((m) => m.name === nameFromUrl));
    }
  }, [methods, nameFromUrl, setMethod]);

  if (!methods) {
    return <div>Loading...</div>;
  }

  const flexContainer = {
    display: "flex",
    flexWrap: "wrap",
    lineHeight: "2rem",
    justifyContent: "center"
  };

  return (
    <div className="methodButtons">
      <div>
        <h1 style={{ textAlign: "center" }}>JCQC Reporting Application</h1>
        {error && <span style={{ color: "red" }}>Error: {error}</span>}
        <hr style={{ width: "36rem", marginBottom: "1rem" }} />
        <div style={flexContainer}>
          {methods.map((m) => {
            return (
              <div key={m.name}>
                <Link
                  to={`/${m.name}`}
                  className="methodButton"
                  onClick={() => setMethod(m)}
                  style={{ margin: "8px" }}
                >
                  {m.name}
                </Link>
              </div>
            );
          })}

          <div>
            <Link to="/" className="methodButton" onClick={() => setMethod()}>
              Clear
            </Link>
          </div>
        </div>
        {method && (
          <>
            <br />
            <br />
          </>
        )}

        {method && (
          <div>
            <FileSelector
              setError={setError}
              method={method}
              setData={setData}
            />
            <Method method={method} />
          </div>
        )}
      </div>
    </div>
  );
};

export default MethodSelect;
