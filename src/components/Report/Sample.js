import React from "react";
import dataUtils from "../../utils/dataUtils";

const Sample = ({ data, sigFigs, coloured }) => {
  return (
    <tr className={coloured ? "colouredRow" : ""}>
      <td className="firstCol">{data.id}</td>
      {data.values.map((v, i) => {
        return (
          <td key={data.id + data.values[i]}>
            {v > 1000
              ? parseFloat(dataUtils.roundToSigFigs(v, sigFigs))
              : dataUtils.roundToSigFigs(v, sigFigs)}
          </td>
        );
      })}
    </tr>
  );
};

const Samples = ({ samples, sigFigs }) => {
  return (
    <>
      {samples.map((s, i) => {
        return (
          <Sample key={s.id} data={s} sigFigs={sigFigs} coloured={i % 2} />
        );
      })}
    </>
  );
};

export default Samples;
