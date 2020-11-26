import React from "react";
import dataUtils from "../../utils/dataUtils";

const CheckStd = ({ data, checkStd, method }) => {
  const expectedValues = checkStd.expectedValues;
  const tolerance = method.checkStdTolerance;
  const sigFigs = method.sigFigs;

  return (
    <div>
      <br />
      <table className="RMTable">
        <thead>
          <tr>
            <th className="firstCol">Sample Type</th>
            {method.elements.map((e, i) => (
              <th key={e}>{e} (ppb)</th>
            ))}
          </tr>
        </thead>

        <tbody>
          <tr>
            <td className="firstCol">{data.id}</td>
            {data.values.map((v, i) => {
              if (v < 2) {
                v = v * 1000;
              }
              return (
                <td key={v + i}>{dataUtils.roundToSigFigs(v, sigFigs)}</td>
              );
            })}
          </tr>
          <tr>
            <td className="firstCol">Within Range</td>
            {data.values.map((v, i) => {
              if (v < 1) {
                v = v * 1000;
              }
              const limitLow =
                expectedValues[i] - expectedValues[i] * tolerance;
              const limitHigh =
                expectedValues[i] + expectedValues[i] * tolerance;
              const withinRange = v > limitLow && v < limitHigh;
              return (
                <td
                  className={withinRange ? "samplePass" : "sampleFail"}
                  key={v + i}
                >
                  {" "}
                  {withinRange ? "Yes" : "No"}
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
      <br />
    </div>
  );
};

export default CheckStd;
