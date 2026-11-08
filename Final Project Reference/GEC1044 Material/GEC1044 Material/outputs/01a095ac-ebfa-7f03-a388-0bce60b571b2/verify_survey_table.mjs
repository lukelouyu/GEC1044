import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const base = "C:/Users/lukel/Downloads/GEC1044 Material/outputs/01a095ac-ebfa-7f03-a388-0bce60b571b2";
const input = await FileBlob.load(`${base}/GEC1044_Survey_Table.xlsx`);
const workbook = await SpreadsheetFile.importXlsx(input);

const sheets = await workbook.inspect({ kind: "sheet", include: "id,name", maxChars: 4000 });
console.log("SAVED_SHEETS\n" + sheets.ndjson);
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "saved workbook formula error scan",
});
console.log("SAVED_ERROR_SCAN\n" + errors.ndjson);
const physician = await workbook.inspect({
  kind: "table",
  range: "4.6 Physician!A7:C11",
  include: "values,formulas",
  tableMaxRows: 10,
  tableMaxCols: 4,
  maxChars: 4000,
});
console.log("SAVED_PHYSICIAN\n" + physician.ndjson);
const preview = await workbook.render({ sheetName: "4.6 Physician", autoCrop: "all", scale: 1, format: "png" });
await fs.writeFile(`${base}/postexport_physician.png`, new Uint8Array(await preview.arrayBuffer()));

