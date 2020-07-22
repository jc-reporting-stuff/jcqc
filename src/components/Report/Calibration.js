import React from "react";

import dataUtils from "../../utils/dataUtils";

const Duplicate = ({ data, elements, method }) => {
  return (
    <div>
      <h1>Calibration Data</h1>

      <table className="calTable">
        <thead>
          <tr>
            <th className="firstCol">Concentration</th>
            {method.elements.map((e, i) => (
              <th key={e}>
                {e} ({method.units[i]})
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((std, i) => {
            return (
              <tr key={std.id + i}>
                <td className="firstCol">{std.id}</td>
                {std.values.map((v, i) => {
                  return (
                    <td key={v + i}>
                      {v < 0.001 && std.name !== "Hg"
                        ? "0.00"
                        : dataUtils.roundToSigFigs(v, method.sigFigs)}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
      <br />

      <h1>Sample Data</h1>
    </div>
  );
};

export default Duplicate;
