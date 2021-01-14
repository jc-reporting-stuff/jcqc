import React from "react";

const Method = ({ method }) => {
  if (method && method.name) {
    return (
      <div className="centeredContainerParent">
        <div
          className="centeredContainerChild"
          style={{ textAlign: "left", paddingTop: "15px" }}
        >
          <h2>
            {method.name}
            {": "}
            {method.description}{" "}
          </h2>

          <p>Percent RPD for duplicates: {method.duplicateTolerance}</p>
          <p>Number of significant figures on report: {method.sigFigs}</p>

          <p>
            Calibration Standard concentrations:{" "}
            {method.calStandards.join(", ")}
          </p>

          <table className="methodTable stripedTable">
            <thead>
              <tr>
                <th className="firstCol">Elements</th>
                {method.elements.map((e) => (
                  <th key={e}>{e}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              <tr style={{ borderTop: "1px solid grey" }}>
                <td className="firstCol">Units</td>
                {method.units.map((u, i) => (
                  <td key={u + i}>{u}</td>
                ))}
              </tr>

              {method.blanks.map((b, i) => (
                <tr
                  key={b.name + i}
                  style={i === 0 ? { borderTop: "1px solid grey" } : null}
                >
                  <td className="firstCol">{b.name} LOQs</td>
                  {b.LOQs.map((loq, i) => (
                    <td key={i}>{loq || "- -"}</td>
                  ))}
                </tr>
              ))}

              {method.checkStds.map((c, i) => (
                <tr
                  key={c.name + i}
                  style={i === 0 ? { borderTop: "1px solid grey" } : null}
                >
                  <td className="firstCol">{c.name}</td>
                  {c.expectedValues.map((e, i) => (
                    <td key={i}>{e}</td>
                  ))}
                </tr>
              ))}

              {method.referenceMaterials.map((r, i) => (
                <React.Fragment key={r.name}>
                  <tr style={{ borderTop: "1px solid grey" }}>
                    <td className="firstCol">{r.name} Low</td>
                    {r.rangesLow.map((e, i) => (
                      <td key={i}>{e || "- -"}</td>
                    ))}
                  </tr>
                  <tr style={{ borderBottom: "1px solid grey" }}>
                    <td className="firstCol">{r.name} High</td>
                    {r.rangesHigh.map((e, i) => (
                      <td key={i}>{e || "- -"}</td>
                    ))}
                  </tr>
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  } else {
    return null;
  }
};

export default Method;
