import React from "react";

const SampleBlock = props => {
  const elements = props.elements;
  const units = props.units;

  return (
    <>
      <br />
      <table className="sampleTable">
        <thead>
          <tr>
            <th className="firstCol">Sample ID</th>
            {elements.map((e, i) => (
              <th key={e}>{e + " (" + units[i] + ")"}</th>
            ))}
          </tr>
        </thead>
        <tbody>{props.children}</tbody>
      </table>
    </>
  );
};

export default SampleBlock;
