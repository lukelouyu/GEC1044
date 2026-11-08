import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "C:/Users/lukel/Downloads/GEC1044 Material/outputs/01a095ac-ebfa-7f03-a388-0bce60b571b2";
const outputPath = `${outputDir}/GEC1044_Survey_Table.xlsx`;
const previewPath = `${outputDir}/GEC1044_Survey_Table_preview.png`;
const fontFamily = "Arial";

const palette = {
  navy: "#1F4E78",
  blue: "#D9EAF7",
  paleBlue: "#EDF4FA",
  yellow: "#FFF2CC",
  gray: "#F2F2F2",
  border: "#B7C9D6",
  text: "#1F1F1F",
  muted: "#666666",
  redFill: "#FCE8E6",
  redText: "#B91C1C",
};

const workbook = Workbook.create();

const sections = [
  {
    sheetName: "4.1 Herbs",
    title: "4.1 Top 8 Best-Selling Herbs by 12-Month Volume",
    instruction: "Required metric: Physical sales volume over the preceding 12 months. Do not substitute revenue without stating the change.",
    headers: ["Rank", "Herb name as sold, Chinese and English if available", "Form or grade", "12-month volume", "Unit", "Main customer use as described by staff", "Evidence code", "Source and notes"],
    rows: 8,
    tableName: "BestSellingHerbsTable",
    numberFormats: { 0: "0", 3: "#,##0.00" },
    questions: [
      "Reference period: start date",
      "Reference period: end date",
      "Ranking supplied by",
      "Exact records, estimate or recollection",
      "Were online and in-store sales combined?",
    ],
  },
  {
    sheetName: "4.2 Products",
    title: "4.2 Top 8 Most Popular Medical Products and Main Uses",
    instruction: "Record the popularity basis and preserve whether each use comes from staff wording, label wording, or both.",
    headers: ["Rank", "Product and brand", "Herbal, non-herbal or mixed", "Manufacturer and country", "Main disease, symptom or use as stated", "Staff wording, label wording or both", "Popularity basis", "Evidence code"],
    rows: 8,
    tableName: "PopularProductsTable",
    numberFormats: { 0: "0" },
    questions: [
      "Reference period",
      "Online and offline ranking differences",
      "Important contraindication or caution mentioned by staff or label",
    ],
  },
  {
    sheetName: "4.3 Local Products",
    title: "4.3 Top 5 Commonly Used Locally Produced Herbs or Products",
    instruction: "A product qualifies only if evidence shows it was grown, formulated, manufactured, or packed in Singapore. A Singapore seller alone does not establish local production.",
    headers: ["Rank", "Herb or product", "Category", "SG grown, manufactured, formulated or packed", "Singapore producer or location", "Main use", "Evidence of local production", "Evidence code"],
    rows: 5,
    tableName: "LocalProductsTable",
    numberFormats: { 0: "0" },
    questions: [
      "Did staff distinguish cultivation from manufacturing?",
      "Why are these products locally produced or preferred?",
    ],
  },
  {
    sheetName: "4.4 Soup Therapies",
    title: "4.4 Top 5 Most Popular Soup Therapies and Main Uses",
    instruction: "Record the staff-stated use, seasonal or TCM association, and whether the therapy was prepacked or assembled in-store.",
    headers: ["Rank", "Soup pack or therapy name", "Main ingredients", "Main use stated by staff", "Health maintenance, recovery or seasonal wellness", "TCM logic or seasonal association", "Prepacked or assembled in-store", "Evidence code"],
    rows: 5,
    tableName: "SoupTherapiesTable",
    numberFormats: { 0: "0" },
    questions: [
      "Are rankings seasonal?",
      "Who commonly buys them and for whom?",
    ],
  },
  {
    sheetName: "4.5 Least Used",
    title: "4.5 Three Least-Used or Least Popular Products",
    instruction: "Rank from least popular and document how low use was determined.",
    headers: ["Rank from least popular", "Product", "Category", "How low use was determined", "Staff explanation for low use", "Seasonal or long-term?", "Evidence code"],
    rows: 3,
    tableName: "LeastUsedProductsTable",
    numberFormats: { 0: "0" },
    questions: ["Were discontinued and out-of-stock products excluded?"],
  },
  {
    sheetName: "4.7 Prescriptions",
    title: "4.7 If Applicable: Top 8 Prescribed Herbs or Prescriptions",
    instruction: "Complete only if section 4.6 confirms an in-house registered physician. Do not obtain customer-level or patient-level records.",
    headers: ["Rank", "Herb or prescription name", "Single herb or formula", "Form", "Common pattern or indication as described", "Frequency or volume basis", "Evidence code", "Notes"],
    rows: 8,
    tableName: "PrescriptionsTable",
    numberFormats: { 0: "0" },
    applicabilityFormula: true,
  },
  {
    sheetName: "4.8 Symptoms",
    title: "4.8 If Applicable: Top 8 Treated Symptoms and Corresponding Remedies",
    instruction: "Complete only if section 4.6 confirms an in-house registered physician. Do not obtain customer-level or patient-level records.",
    headers: ["Rank", "Symptom or complaint", "TCM pattern distinction, if mentioned", "Typical remedy or prescription", "How treatment may be modified for individuals", "Frequency basis", "Evidence code", "Notes"],
    rows: 8,
    tableName: "TreatedSymptomsTable",
    numberFormats: { 0: "0" },
    applicabilityFormula: true,
  },
];

function styleBase(sheet, lastColumnLetter, lastRow) {
  sheet.showGridLines = false;
  sheet.tabColor = palette.navy;
  const used = sheet.getRange(`A1:${lastColumnLetter}${lastRow}`);
  used.format.font = { name: fontFamily, size: 10, color: palette.text };
  used.format.verticalAlignment = "center";
  sheet.getRange(`A2:${lastColumnLetter}2`).format.rowHeight = 24;
  sheet.getRange("A2").format.font = { name: fontFamily, size: 14, bold: true, color: palette.navy };
  sheet.getRange(`A4:${lastColumnLetter}4`).format = {
    fill: palette.paleBlue,
    font: { name: fontFamily, size: 10, italic: true, color: palette.text },
    wrapText: true,
    borders: { preset: "outside", style: "thin", color: palette.border },
  };
  sheet.getRange(`A4:${lastColumnLetter}4`).format.rowHeight = 40;
}

function formatDataSheet(section) {
  const sheet = workbook.worksheets.add(section.sheetName);
  const colCount = section.headers.length;
  const lastCol = String.fromCharCode(64 + colCount);
  const headerRow = 7;
  const dataStart = headerRow + 1;
  const dataEnd = headerRow + section.rows;
  const questionHeaderRow = dataEnd + 2;
  const questionEnd = section.questions?.length ? questionHeaderRow + section.questions.length : questionHeaderRow;
  const lastRow = Math.max(dataEnd, questionEnd);

  sheet.getRange("A2").values = [[section.title]];
  sheet.getRange("A4").values = [[section.instruction]];
  if (section.sheetName === "4.1 Herbs") {
    sheet.getRange("A5").values = [["Source: Obsidian note — 01 Modules/GEC1044/Course Notes/Tutorials/Survey Table"]];
    sheet.getRange(`A5:${lastCol}5`).format.font = { name: fontFamily, size: 9, italic: true, color: palette.muted };
  }

  if (section.applicabilityFormula) {
    sheet.getRange("A5").formulas = [["=IF('4.6 Physician'!B8=\"No\",\"Not applicable — retail medicine hall without an in-house registered physician\",\"\")"]];
    sheet.getRange(`A5:${lastCol}5`).format = {
      fill: palette.redFill,
      font: { name: fontFamily, size: 10, bold: true, color: palette.redText },
    };
    sheet.getRange(`A5:${lastCol}5`).conditionalFormats.addCustom("=$A$5=\"\"", { fill: "#FFFFFF", font: { color: "#FFFFFF" } });
  }

  styleBase(sheet, lastCol, lastRow);
  sheet.mergeCells(`A4:${lastCol}4`);
  if (section.sheetName === "4.1 Herbs" || section.applicabilityFormula) {
    sheet.mergeCells(`A5:${lastCol}5`);
  }

  const headerRange = sheet.getRange(`A${headerRow}:${lastCol}${headerRow}`);
  headerRange.values = [section.headers];
  const rows = Array.from({ length: section.rows }, (_, i) => [i + 1, ...Array(colCount - 1).fill(null)]);
  sheet.getRange(`A${dataStart}:${lastCol}${dataEnd}`).values = rows;
  const table = sheet.tables.add(`A${headerRow}:${lastCol}${dataEnd}`, true, section.tableName);
  table.style = "TableStyleMedium2";
  table.showBandedColumns = false;
  table.showFilterButton = true;

  headerRange.format = {
    fill: palette.navy,
    font: { name: fontFamily, size: 10, bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "all", style: "thin", color: "#FFFFFF" },
  };
  headerRange.format.rowHeight = 48;
  const body = sheet.getRange(`A${dataStart}:${lastCol}${dataEnd}`);
  body.format.verticalAlignment = "top";
  body.format.wrapText = true;
  body.format.rowHeight = 36;
  sheet.getRange(`A${dataStart}:A${dataEnd}`).format = {
    fill: palette.gray,
    font: { name: fontFamily, size: 10, bold: true, color: palette.text },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    numberFormat: "0",
  };
  if (colCount > 1) {
    sheet.getRange(`B${dataStart}:${lastCol}${dataEnd}`).format.fill = palette.yellow;
  }
  for (const [columnIndex, numberFormat] of Object.entries(section.numberFormats ?? {})) {
    const col = String.fromCharCode(65 + Number(columnIndex));
    sheet.getRange(`${col}${dataStart}:${col}${dataEnd}`).format.numberFormat = numberFormat;
  }

  if (section.questions?.length) {
    sheet.getRange(`B${questionHeaderRow}:F${questionHeaderRow}`).format = {
      fill: palette.blue,
      font: { name: fontFamily, size: 10, bold: true, color: palette.navy },
      borders: { preset: "outside", style: "thin", color: palette.border },
    };
    sheet.getRange(`B${questionHeaderRow}`).values = [["Additional details"]];
    section.questions.forEach((question, index) => {
      const row = questionHeaderRow + 1 + index;
      sheet.getRange(`B${row}`).values = [[question]];
      sheet.getRange(`B${row}`).format = { wrapText: true, verticalAlignment: "center" };
      sheet.getRange(`F${row}`).values = [[null]];
      sheet.getRange(`F${row}`).format = {
        fill: palette.yellow,
        borders: { preset: "outside", style: "thin", color: palette.border },
        wrapText: true,
      };
      sheet.getRange(`B${row}:F${row}`).format.rowHeight = 30;
    });
    if (section.sheetName === "4.1 Herbs") {
      sheet.getRange(`F${questionHeaderRow + 1}:F${questionHeaderRow + 2}`).format.numberFormat = "yyyy-mm-dd";
    }
  }

  const widths = [9, 34, 24, 25, 22, 32, 18, 30];
  widths.slice(0, colCount).forEach((width, i) => {
    sheet.getRange(`${String.fromCharCode(65 + i)}:${String.fromCharCode(65 + i)}`).format.columnWidth = width;
  });
  sheet.freezePanes.freezeRows(headerRow);
  return sheet;
}

// Add physician sheet before the two formula-linked sheets exist.
for (const section of sections.slice(0, 5)) formatDataSheet(section);

const physician = workbook.worksheets.add("4.6 Physician");
physician.getRange("A2").values = [["4.6 In-House Registered Physician Screening"]];
physician.getRange("A4").values = [["If No, write “Not applicable — retail medicine hall without an in-house registered physician” across sections 4.7 and 4.8. Do not obtain customer-level or patient-level records."]];
styleBase(physician, "C", 11);
physician.mergeCells("A4:C4");
physician.getRange("A7:C7").values = [["Question", "Response", "Guidance"]];
physician.getRange("A8:C11").values = [
  ["Does this outlet have an in-house registered physician?", null, "Select Yes, No, or Unclear"],
  ["Is the physician regularly based here or only visiting?", null, "Describe the arrangement"],
  ["Does the physician provide consultations or only general product advice?", null, "Record the staff description"],
  ["Basis for classification", null, "State the evidence used"],
];
const physicianTable = physician.tables.add("A7:C11", true, "PhysicianScreeningTable");
physicianTable.style = "TableStyleMedium2";
physicianTable.showFilterButton = false;
physician.getRange("A7:C7").format = {
  fill: palette.navy,
  font: { name: fontFamily, size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#FFFFFF" },
};
physician.getRange("A7:C7").format.rowHeight = 36;
physician.getRange("A8:C11").format = { wrapText: true, verticalAlignment: "top" };
physician.getRange("A8:C11").format.rowHeight = 42;
physician.getRange("B8:B11").format.fill = palette.yellow;
physician.getRange("B8").dataValidation = { rule: { type: "list", values: ["Yes", "No", "Unclear"] } };
physician.getRange("A:A").format.columnWidth = 48;
physician.getRange("B:B").format.columnWidth = 24;
physician.getRange("C:C").format.columnWidth = 32;
physician.freezePanes.freezeRows(7);

for (const section of sections.slice(5)) formatDataSheet(section);

// Verify the physician screening drives both applicable sections, then restore the input.
physician.getRange("B8").values = [["No"]];
workbook.recalculate();
const expectedNotApplicable = "Not applicable — retail medicine hall without an in-house registered physician";
for (const targetSheet of ["4.7 Prescriptions", "4.8 Symptoms"]) {
  const actual = workbook.worksheets.getItem(targetSheet).getRange("A5").values[0][0];
  if (actual !== expectedNotApplicable) {
    throw new Error(`Applicability formula test failed on ${targetSheet}: ${actual}`);
  }
}
physician.getRange("B8").values = [[null]];
workbook.recalculate();

const overview = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 9000,
  tableMaxRows: 4,
  tableMaxCols: 8,
  tableMaxCellChars: 80,
});
console.log("OVERVIEW\n" + overview.ndjson);

const keyCheck = await workbook.inspect({
  kind: "table",
  range: "4.1 Herbs!A2:H15",
  include: "values,formulas",
  tableMaxRows: 15,
  tableMaxCols: 8,
  maxChars: 9000,
});
console.log("KEY_CHECK\n" + keyCheck.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log("ERROR_SCAN\n" + errors.ndjson);

await fs.mkdir(outputDir, { recursive: true });
const preview = await workbook.render({ sheetName: "4.1 Herbs", range: "A1:H22", scale: 1.2, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
for (const [index, sheetName] of [
  "4.2 Products",
  "4.3 Local Products",
  "4.4 Soup Therapies",
  "4.5 Least Used",
  "4.6 Physician",
  "4.7 Prescriptions",
  "4.8 Symptoms",
].entries()) {
  const rendered = await workbook.render({ sheetName, autoCrop: "all", scale: 0.8, format: "png" });
  await fs.writeFile(`${outputDir}/preview_${index + 2}.png`, new Uint8Array(await rendered.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`OUTPUT=${outputPath}`);
console.log(`PREVIEW=${previewPath}`);
