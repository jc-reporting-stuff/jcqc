import React from "react";
import { Helmet } from "react-helmet";
import { Link } from "react-router-dom";

import Blank from "./Blank";
import Samples from "./Sample";
import Duplicate from "./Duplicate";
import Calibration from "./Calibration";
import SampleBlock from "./SampleBlock";
import HeaderInfo from "./HeaderInfo";
import CheckStd from "./CheckStd";
import ReferenceMaterial from "./ReferenceMaterial";

const Report = ({ data, method }) => {
  if (!data) {
    return (
      <div style={{ textAlign: "center" }}>
        Loading data. If your report doesn't load soon, &nbsp;
        <Link to="/">click here</Link> to restart.
      </div>
    );
  }

  return (
    <div>
      <Helmet>
        <meta charSet="utf-8" />
        <title>JCQC Reporting Application</title>
      </Helmet>

      {method && method.elements.length !== data[0].values.length && (
        <div style={{ color: "red" }}>
          Warning: expected {method.elements.length} element
          {method.elements.length === 1 ? "" : "s"}, found{" "}
          {data[0].values.length}. Possible method mismatch.
        </div>
      )}

      <HeaderInfo method={method} />
      {data[0].id &&
        data.map((d, idx) => {
          const sampleBlank = method.blanks.find((b) => b.name === d.id);
          const checkStd = method.checkStds.find((c) => c.name === d.id);
          const referenceMaterial = method.referenceMaterials.find(
            (r) => r.name === d.id
          );
          // const duplicate = d.id.match(sampleIdRegEx) && d.dupValues
          const duplicate = d.dupValues;

          const sampleIdRegEx = new RegExp("^[0-9]{2}-[0-9]{6}-[0-9]{4}");
          const sample = d.id.match(sampleIdRegEx);

          if (d.id === "Cal Blank") {
            const calData = data.slice(
              idx,
              idx + method.calStandards.length + 1
            );
            return <Calibration data={calData} key={idx} method={method} />;
          } else if (sampleBlank) {
            const LOQs = method.blanks.find((b) => b.type === sampleBlank.type)
              .LOQs;
            return (
              <Blank
                data={d}
                key={idx}
                blank={sampleBlank}
                method={method}
                LOQs={LOQs}
              />
            );
          } else if (checkStd) {
            return (
              <CheckStd
                data={d}
                key={idx}
                checkStd={checkStd}
                method={method}
              />
            );
          } else if (referenceMaterial) {
            const LOQs = method.blanks.find(
              (b) => b.type === referenceMaterial.type
            );
            if (!duplicate) {
              return (
                <ReferenceMaterial
                  data={d}
                  key={d.id + idx}
                  method={method}
                  material={referenceMaterial}
                  LOQs={LOQs}
                />
              );
            } else {
              return (
                <div key={d.id + idx}>
                  <ReferenceMaterial
                    data={d}
                    method={method}
                    material={referenceMaterial}
                    LOQs={LOQs}
                  />
                  <Duplicate data={d} method={method} />
                </div>
              );
            }
          } else if (duplicate) {
            return (
              <Duplicate
                data={d}
                key={d.dupValues.length + idx}
                method={method}
              />
            );
          } else if (sample) {
            const prevSampleExists = data[idx - 1];
            const prevSampleIsSample = data[idx - 1].id.match(sampleIdRegEx);
            const prevSampleIsDup = data[idx - 1].dupValues;

            // If this is the first sample of a block of samples,
            // we'll start a new block with headers and such.
            if (prevSampleExists && (!prevSampleIsSample || prevSampleIsDup)) {
              // start a list of the samples in this block
              let sampleList = [d];
              let stillASample = true;
              let j = idx + 1;

              // This loop will stay true until the end of the sample
              // block is reached, or we hit a duplicate
              while (stillASample) {
                const isASample = data[j].id.match(sampleIdRegEx);
                const isADup = data[j].dupValues;
                stillASample = isASample && !isADup;
                if (stillASample) sampleList.push(data[j]);
                ++j;
              }

              // If it's not the first sample of a new block,
              // we can safely skip it because we will pass
              // all of the samples in the block to this component
              return (
                <div key={d.id + idx}>
                  <SampleBlock
                    elements={method.elements}
                    data={d}
                    key={Date.now()}
                    units={method.units}
                  >
                    <Samples
                      samples={sampleList}
                      key={idx}
                      sigFigs={method.sigFigs}
                    />
                  </SampleBlock>
                </div>
              );
            }
          }
          return null;
        })}
    </div>
  );
};

export default Report;
