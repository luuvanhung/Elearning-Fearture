import ExcelJS from "exceljs";
import fs from "file-saver";
import ExcelStyles from "./ExcelStyles";

const CHECK_SYMBOL_UNICODE = "\u2705";
/* parameters:
 * colIndex: the index of column, start from 1 (equivalent  to colum 'A')
 * return the name of column
 */

function getColumnName(colIndex) {
  let quotient = colIndex;
  let remainder = 0;
  let columnName = "";

  // The cellName in reverse other
  do {
    quotient -= 1;
    remainder = quotient % 26;
    columnName = String.fromCharCode(65 + remainder) + columnName;
    quotient = Math.floor(quotient / 26);
  } while (quotient > 0);
  return columnName;
}

/* parameters:
 * colIndex: the index of column, start from 1 (equivalent  to colum 'A')
 * row: the index of row
 */
function getCellName(colIndex, row) {
  return getColumnName(colIndex) + row;
}

export async function generateProbationList(data) {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = "LAB";
  workbook.lastModifiedBy = "LAB";
  workbook.created = new Date(1985, 8, 30);
  workbook.modified = new Date();
  workbook.lastPrinted = new Date(2016, 9, 27);
  workbook.properties.date1904 = true;

  const worksheet = workbook.addWorksheet("Probation List");
  worksheet.properties.defaultColWidth = 25;

  //Probation List header
  let temp_row = 1;
  let temp_col = 1;
  //Full Name header
  const fullNameHeaderCellName = getCellName(temp_col, temp_row);
  const fullNameHeaderCell = worksheet.getCell(fullNameHeaderCellName);
  fullNameHeaderCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Full Name" }],
  };
  fullNameHeaderCell.alignment = ExcelStyles.centerAlignment;
  fullNameHeaderCell.fill = ExcelStyles.headerFill;
  fullNameHeaderCell.border = ExcelStyles.headerBorder;
  temp_col += 1;
  //Team header
  const teamHeaderCellName = getCellName(temp_col, temp_row);
  const teamHeaderCell = worksheet.getCell(teamHeaderCellName);
  teamHeaderCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Team" }],
  };
  teamHeaderCell.alignment = ExcelStyles.centerAlignment;
  teamHeaderCell.fill = ExcelStyles.headerFill;
  teamHeaderCell.border = ExcelStyles.headerBorder;
  temp_col += 1;
  //Position header
  const positionHeaderCellName = getCellName(temp_col, temp_row);
  const positionHeaderCell = worksheet.getCell(positionHeaderCellName);
  positionHeaderCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Position" }],
  };
  positionHeaderCell.alignment = ExcelStyles.centerAlignment;
  positionHeaderCell.fill = ExcelStyles.headerFill;
  positionHeaderCell.border = ExcelStyles.headerBorder;
  temp_col += 1;
  //Join Date header
  const joinDateHeaderCellName = getCellName(temp_col, temp_row);
  const joinDateHeaderCell = worksheet.getCell(joinDateHeaderCellName);
  joinDateHeaderCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Join Date" }],
  };
  joinDateHeaderCell.alignment = ExcelStyles.centerAlignment;
  joinDateHeaderCell.fill = ExcelStyles.headerFill;
  joinDateHeaderCell.border = ExcelStyles.headerBorder;
  temp_col += 1;
  //Probation End Date header
  const endDateHeaderCellName = getCellName(temp_col, temp_row);
  const endDateHeaderCell = worksheet.getCell(endDateHeaderCellName);
  endDateHeaderCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "End Date" }],
  };
  endDateHeaderCell.alignment = ExcelStyles.centerAlignment;
  endDateHeaderCell.fill = ExcelStyles.headerFill;
  endDateHeaderCell.border = ExcelStyles.headerBorder;
  temp_col += 1;
  //Remind header
  const remindHeaderCellName = getCellName(temp_col, temp_row);
  const remindHeaderCell = worksheet.getCell(remindHeaderCellName);
  remindHeaderCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Remind" }],
  };
  remindHeaderCell.alignment = ExcelStyles.centerAlignment;
  remindHeaderCell.fill = ExcelStyles.headerFill;
  remindHeaderCell.border = ExcelStyles.headerBorder;
  temp_col += 1;
  //Type of evaluation
  const typeOfEvaluationCellName = getCellName(temp_col, temp_row);
  const typeOfEvaluationCell = worksheet.getCell(typeOfEvaluationCellName);
  typeOfEvaluationCell.value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Type of Evaluation" }],
  };
  typeOfEvaluationCell.alignment = ExcelStyles.centerAlignment;
  typeOfEvaluationCell.fill = ExcelStyles.headerFill;
  typeOfEvaluationCell.border = ExcelStyles.headerBorder;
  temp_col += 1;

  //Probations List Data
  temp_row += 1;
  temp_col = 1;
  data.multipleSelection.forEach((listProbation) => {
    //fullName data
    let fullNameCell = getCellName(temp_col, temp_row);
    worksheet.getCell(fullNameCell).value = listProbation.employee.profile.name;
    //team data
    let teamCell = getCellName(temp_col + 1, temp_row);
    worksheet.getCell(teamCell).alignment = ExcelStyles.centerAlignment;
    if (listProbation.employee.profile.teams === null) {
      worksheet.getCell(teamCell).value = "........";
    } else {
      listProbation.employee.profile.teams.forEach((team) => {
        worksheet.getCell(teamCell).value = team.name;
      });
    }
    //position data
    let positionCell = getCellName(temp_col + 2, temp_row);
    worksheet.getCell(positionCell).alignment = ExcelStyles.centerAlignment;
    worksheet.getCell(positionCell).value =
      listProbation.title === null
        ? "........."
        : listProbation.employee.title.title;
    //joinDate data
    let joinDateCell = getCellName(temp_col + 3, temp_row);
    worksheet.getCell(joinDateCell).value =
      listProbation.employee.profile.join_date;
    worksheet.getCell(joinDateCell).alignment = ExcelStyles.centerAlignment;
    //endDate data
    let endDateCell = getCellName(temp_col + 4, temp_row);
    worksheet.getCell(endDateCell).value = listProbation.probation_end_date;
    worksheet.getCell(endDateCell).alignment = ExcelStyles.centerAlignment;
    //remain data
    let remainCell = getCellName(temp_col + 5, temp_row);
    let remind = listProbation.remind;
    let result = remind.toString();
    worksheet.getCell(remainCell).value = result;
    //Type of Evaluation
    let typeOfEvaluationCell = getCellName(temp_col + 6, temp_row);
    worksheet.getCell(typeOfEvaluationCell).value = listProbation.type_name;
    worksheet.getCell(typeOfEvaluationCell).alignment =
      ExcelStyles.centerAlignment;
    temp_row++;
  });

  workbook.xlsx.writeBuffer().then((data) => {
    const blob = new Blob([data], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    fs.saveAs(blob, "probationList.xlsx");
  });
}
