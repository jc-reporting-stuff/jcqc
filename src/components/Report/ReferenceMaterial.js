import React from "react";
import dataUtils from "../../utils/dataUtils";

const ReferenceMaterial = ({ data, material, method }) => {
  const rangesLow = material.rangesLow;
  const rangesHigh = material.rangesHigh;

  return (
    <div>
      <br />
      <table className="RMTable">
        <thead>
          <tr>
            <th className="firstCol">Sample Type</th>
            {method.elements.map((e, i) => (
              <th key={e}>{e + " (" + method.units[i] + ")"}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          <tr>
            <td className="firstCol">{data.id}</td>
            {data.values.map((v, i) => (
              <td key={v + i}>
                {parseFloat(dataUtils.roundToSigFigs(v, method.sigFigs))}
              </td>
            ))}
          </tr>
          <tr>
            <td className="firstCol">Within Range</td>
            {data.values.map((v, i) => {
              const hasRange = material.rangesHigh[i];
              const withinRange = v > rangesLow[i] && v < rangesHigh[i];
              return (
                <td
                  className={
                    withinRange
                      ? "samplePass"
                      : hasRange
                      ? "sampleFail"
                      : "sampleNeutral"
                  }
                  key={v + i}
                >
                  {" "}
                  {withinRange ? "Yes" : hasRange ? "No" : "- - -"}
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

export default ReferenceMaterial;
