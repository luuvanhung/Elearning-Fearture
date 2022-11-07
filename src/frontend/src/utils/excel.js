import ExcelJS from "exceljs";
import fs from "file-saver";
import ExcelStyles from "./ExcelStyles";
import imageToBase64 from "image-to-base64/browser";

const CHECK_SYMBOL_UNICODE = "\u2611";
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

export async function generateProbationForm(data) {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = "LAB";
  workbook.lastModifiedBy = "LAB";
  workbook.created = new Date(1985, 8, 30);
  workbook.modified = new Date();
  workbook.lastPrinted = new Date(2016, 9, 27);
  workbook.properties.date1904 = true;

  const worksheet = workbook.addWorksheet("Probation");
  worksheet.properties.defaultColWidth = 30;
  worksheet.views = [
    {
      state: "frozen",
      xSplit: 0,
      ySplit: 7,
      activeCell: "A1",
    },
  ];

  const row = worksheet.getRow(1);
  row.height = 25;

  worksheet.mergeCells("A7:M7");

  worksheet.mergeCells("A1:A6");
  worksheet.getCell("A1").border = ExcelStyles.headerBorder;

  //Image to base 64
  let LOGO_PARADOX_URL = "/static/paradox-logo.jpg";
  const check = await imageToBase64(LOGO_PARADOX_URL)
    .then((response) => "data:image/jpg;base64,".concat(new String(response)))
    .catch((error) => console.log(error));
  //End image to base 64

  const logoParadox = workbook.addImage({
    base64: check,
    extension: "png",
  });
  worksheet.addImage(logoParadox, "A1:A6");

  worksheet.getCell("A9").fill = ExcelStyles.headerFill;
  worksheet.getCell("A9").border = ExcelStyles.headerBorder;

  worksheet.getCell("G10").fill = ExcelStyles.headerFill;
  worksheet.getCell("G10").border = ExcelStyles.headerBorder;

  worksheet.getCell("M10").fill = ExcelStyles.headerFills;
  worksheet.getCell("M10").border = ExcelStyles.headerBorder;

  worksheet.mergeCells("B1:M1");
  worksheet.getCell("B1").value = {
    richText: [
      { font: ExcelStyles.headerTitle, text: data.evaluationTemplateTitle },
    ],
  };
  //Employee Name
  worksheet.mergeCells("B2:F2");
  worksheet.getCell("B2").value = {
    richText: [{ font: ExcelStyles.labelFont, text: "Employee name:" }],
  };
  worksheet.getCell("G2").value = data.employeeName;
  //Job Title
  worksheet.mergeCells("B3:F3");
  worksheet.getCell("B3").value = {
    richText: [{ font: ExcelStyles.labelFont, text: "Job title:" }],
  };
  worksheet.getCell("G3").value =
    data.jobTitle === undefined ? "..........." : data.jobTitle;
  //Team
  worksheet.mergeCells("B4:F4");
  worksheet.getCell("B4").value = {
    richText: [{ font: ExcelStyles.labelFont, text: "Team:" }],
  };
  worksheet.getCell("G4").value =
    data.probationDetail.team === null
      ? "..........."
      : data.probationDetail.team.team_name;
  //Line Manager
  worksheet.mergeCells("B5:F5");
  worksheet.getCell("B5").value = {
    richText: [{ font: ExcelStyles.labelFont, text: "Line manager:" }],
  };
  worksheet.getCell("G5").value =
    data.probationDetail.probation_line_manager === null
      ? "..........."
      : data.probationDetail.probation_line_manager.profile.name;
  //Period of Appraisal
  worksheet.mergeCells("B6:F6");
  worksheet.getCell("B6").value = {
    richText: [{ font: ExcelStyles.labelFont, text: "Period of appraisal:" }],
  };
  worksheet.getCell("G6").value =
    "From " + data.startDay + " to " + data.endDay;

  worksheet.getCell("M6").value = {
    richText: [
      { font: ExcelStyles.tips, text: "REMEMBER TO GIVE DETAILED EVALUATION" },
    ],
  };
  worksheet.getCell("M6").alignment = {
    vertical: "middle",
    horizontal: "right",
  };

  worksheet.getCell("A8").value = {
    richText: [
      { font: ExcelStyles.whiteHeaderFont, text: "DETAILED EVALUATIONS" },
    ],
  };
  worksheet.getCell("A8").alignment = {
    vertical: "middle",
    horizontal: "center",
  };
  worksheet.getCell("A8").fill = ExcelStyles.headerFill;
  worksheet.getCell("A8").border = ExcelStyles.headerBorder;

  //Roles headers
  let temp_row = 8;
  let temp_col = 2; // B
  //Competencies
  const competenciesHeaderCellName = getCellName(temp_col - 1, temp_row + 2);
  const competenciesHeaderCell = worksheet.getCell(competenciesHeaderCellName);
  competenciesHeaderCell.value = {
    richText: [{ font: ExcelStyles.whiteHeaderFont, text: "Competencies" }],
  };
  competenciesHeaderCell.alignment = ExcelStyles.centerAlignment;
  competenciesHeaderCell.fill = ExcelStyles.headerFill;
  competenciesHeaderCell.border = ExcelStyles.headerBorder;

  data.competenceAssessorRoles.forEach((role) => {
    // Title
    let titleEndCol = temp_col + 5;
    let titleStartCell = getCellName(temp_col, temp_row);
    let tileEndCell = getCellName(titleEndCol, temp_row);
    let tileMergeRange = titleStartCell + ":" + tileEndCell;
    worksheet.mergeCells(tileMergeRange);
    worksheet.getCell(titleStartCell).value = {
      richText: [{ font: ExcelStyles.headerFont, text: role }],
    };
    worksheet.getCell(titleStartCell).alignment = {
      vertical: "middle",
      horizontal: "center",
    };
    worksheet.getCell(titleStartCell).fill = ExcelStyles.headerFill;
    worksheet.getCell(titleStartCell).border = ExcelStyles.headerBorder;

    // Scoring
    let scoringRow = temp_row + 1;
    let scoringStartCol = temp_col;
    let scoringEndCol = temp_col + 4;
    let scoringStartCell = getCellName(scoringStartCol, scoringRow);
    let scoringEndCell = getCellName(scoringEndCol, scoringRow);
    let scoringMergeRange = scoringStartCell + ":" + scoringEndCell;
    worksheet.mergeCells(scoringMergeRange);
    worksheet.getCell(scoringStartCell).value = {
      richText: [{ font: ExcelStyles.headerFont, text: "Scoring" }],
    };
    worksheet.getCell(scoringStartCell).alignment = {
      vertical: "middle",
      horizontal: "center",
    };
    worksheet.getCell(scoringStartCell).fill = ExcelStyles.headerFill;
    worksheet.getCell(scoringStartCell).border = ExcelStyles.headerBorder;

    //Score
    let scoreRow = scoringRow + 1;
    for (let i = 0; i < 5; i++) {
      const scoreCol = scoringStartCol + i;
      let scoreCell = getCellName(scoreCol, scoreRow);
      worksheet.getCell(scoreCell).value = {
        richText: [{ font: ExcelStyles.headerFont, text: i + 1 }],
      };
      worksheet.getCell(scoreCell).alignment = {
        vertical: "middle",
        horizontal: "center",
      };
      worksheet.getCell(scoreCell).fill = ExcelStyles.headerFill;
      worksheet.getCell(scoreCell).border = ExcelStyles.headerBorder;

      const tempColumnName = getColumnName(scoreCol);
      let scoreColumn = worksheet.getColumn(tempColumnName);
      scoreColumn.width = 5;
    }

    //Detail
    let detailCol = temp_col + 5;
    let detailCell = getCellName(detailCol, scoringRow);
    worksheet.getCell(detailCell).value = {
      richText: [{ font: ExcelStyles.headerFont, text: "Comments" }],
    };
    worksheet.getCell(detailCell).alignment = {
      vertical: "middle",
      horizontal: "center",
    };
    worksheet.getCell(detailCell).fill = ExcelStyles.headerFill;
    worksheet.getCell(detailCell).border = ExcelStyles.headerBorder;
    let detailBlankCell = getCellName(detailCol, scoringRow + 1);
    worksheet.getCell(detailBlankCell).fill = ExcelStyles.headerFill;
    worksheet.getCell(detailBlankCell).border = ExcelStyles.headerBorder;

    temp_col += 6;
  });

  // Competencies
  temp_row += 3;
  temp_col = 1;
  data.competenceData.forEach((competency) => {
    // Name
    let competencyNameCell = getCellName(temp_col, temp_row);
    worksheet.getCell(competencyNameCell).value =
      competency.evaluation_template_competence.competence;
    worksheet.getCell(competencyNameCell).alignment = ExcelStyles.alignment;
    let evaluationStartCol = temp_col;
    data.competenceAssessorRoles.forEach((role) => {
      let evaluation =
        competency.evaluation_template_competence_assessor_role[role];
      if (evaluation) {
        const score = evaluation.score > 0 ? evaluation.score : 1;
        const scoreCellName = getCellName(evaluationStartCol + score, temp_row);
        const scoreCell = worksheet.getCell(scoreCellName);
        scoreCell.value = CHECK_SYMBOL_UNICODE;
        scoreCell.alignment = ExcelStyles.centerAlignment;
        const commentCell = getCellName(evaluationStartCol + 6, temp_row);

        worksheet.getCell(commentCell).value = evaluation.comments;
        worksheet.getCell(commentCell).alignment = ExcelStyles.alignment;
      }
      evaluationStartCol += 6;
    });

    temp_row++;
  });

  //Overall comment Header
  temp_row += 1;
  // Name
  const commentNameHeaderCellName = getCellName(temp_col, temp_row);
  const commentNameHeaderCell = worksheet.getCell(commentNameHeaderCellName);
  commentNameHeaderCell.value = {
    richText: [
      { font: ExcelStyles.whiteHeaderFont, text: "Overall comments:" },
    ],
  };
  commentNameHeaderCell.alignment = {
    vertical: "middle",
    horizontal: "center",
  };
  commentNameHeaderCell.fill = ExcelStyles.headerFill;
  commentNameHeaderCell.border = ExcelStyles.headerBorder;
  // Score
  const scoreHeaderStartCol = 2;
  for (let i = 0; i < 5; i++) {
    const scoreCol = scoreHeaderStartCol + i;
    let scoreCell = getCellName(scoreCol, temp_row);
    worksheet.getCell(scoreCell).value = {
      richText: [{ font: ExcelStyles.headerFont, text: i + 1 }],
    };
    worksheet.getCell(scoreCell).alignment = {
      vertical: "middle",
      horizontal: "center",
    };
    worksheet.getCell(scoreCell).fill = ExcelStyles.headerFill;
    worksheet.getCell(scoreCell).border = ExcelStyles.headerBorder;

    const tempColumnName = getColumnName(scoreCol);
    let scoreColumn = worksheet.getColumn(tempColumnName);
    scoreColumn.width = 5;
  }
  // Comment
  const commentDetailHeaderCell = getCellName(temp_col + 6, temp_row);
  worksheet.getCell(commentDetailHeaderCell).value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Detailed comments" }],
  };
  worksheet.getCell(commentDetailHeaderCell).alignment = {
    vertical: "middle",
    horizontal: "center",
  };
  worksheet.getCell(commentDetailHeaderCell).fill = ExcelStyles.headerFill;
  worksheet.getCell(commentDetailHeaderCell).border = ExcelStyles.headerBorder;
  // Assessor
  let assessorStartCell = getCellName(temp_col + 7, temp_row);
  let assessorEndCell = getCellName(temp_col + 11, temp_row);
  let assessorMergeRange = assessorStartCell + ":" + assessorEndCell;
  worksheet.mergeCells(assessorMergeRange);
  worksheet.getCell(assessorStartCell).value = {
    richText: [{ font: ExcelStyles.headerFont, text: "Assessor" }],
  };
  worksheet.getCell(assessorStartCell).alignment = {
    vertical: "middle",
    horizontal: "center",
  };
  worksheet.getCell(assessorStartCell).fill = ExcelStyles.headerFill;
  worksheet.getCell(assessorStartCell).border = ExcelStyles.headerBorder;
  //Role
  const roleHeaderCell = getCellName(temp_col + 12, temp_row);
  worksheet.getCell(roleHeaderCell).alignment = {
    vertical: "middle",
    horizontal: "center",
  };
  worksheet.getCell(roleHeaderCell).fill = ExcelStyles.headerFill;
  worksheet.getCell(roleHeaderCell).border = ExcelStyles.headerBorder;

  // Overall comments
  temp_row += 1;
  temp_col = 1;
  data.overCmtData.forEach((evaluation) => {
    // Name
    let commentNameCellName = getCellName(temp_col, temp_row);
    worksheet.getCell(commentNameCellName).value =
      evaluation.evaluation_template_overall_comment.term;
    worksheet.getCell(commentNameCellName).alignment = ExcelStyles.alignment;
    //Score
    const score = evaluation.score > 0 ? evaluation.score : 1;
    const scoreCellName = getCellName(temp_col + score, temp_row);
    const scoreCell = worksheet.getCell(scoreCellName);
    scoreCell.value = "\u2611";
    scoreCell.alignment = ExcelStyles.centerAlignment;
    //Comment
    const commentCellName = getCellName(temp_col + 6, temp_row);
    worksheet.getCell(commentCellName).value = evaluation.comments;
    worksheet.getCell(commentCellName).alignment = ExcelStyles.alignment;
    //Assessor
    let assessorStartCellName = getCellName(temp_col + 7, temp_row);
    let assessorEndCellName = getCellName(temp_col + 11, temp_row);
    let assessorMergeRange = assessorStartCellName + ":" + assessorEndCellName;
    worksheet.mergeCells(assessorMergeRange);
    const assessorCell = worksheet.getCell(assessorStartCellName);
    assessorCell.value =
      evaluation.assessor === null
        ? "..............."
        : evaluation.assessor.profile.name;
    //Assessor Role
    let assessorRoleCellName = getCellName(temp_col + 12, temp_row);
    worksheet.getCell(assessorRoleCellName).value =
      evaluation.evaluation_template_overall_comment_assessor_role.overall_comment_role;
    temp_row++;
  });

  // Final
  temp_row += 1;
  temp_col = 1;
  let cellName = getCellName(temp_col, temp_row);
  let cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [
      { font: ExcelStyles.whiteHeaderFont, text: "Outcome(DO NOT WRITE HERE)" },
    ],
  };
  cell.alignment = { vertical: "middle", horizontal: "center" };
  for (let i = 0; i < 12; i++) {
    cellName = getCellName(temp_col + i, temp_row);
    cell = worksheet.getCell(cellName);
    cell.fill = ExcelStyles.headerFill;
    cell.border = ExcelStyles.headerBorder;
  }
  //Signing official labor contract
  temp_row++;
  cellName = getCellName(temp_col, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [
      { font: ExcelStyles.bodyFont, text: "Signing official labor contract:" },
    ],
  };
  if (data.isSignedConstract) {
    cellName = getCellName(temp_col + 1, temp_row);
    cell = worksheet.getCell(cellName);
    cell.value = CHECK_SYMBOL_UNICODE;
    cell.alignment = ExcelStyles.centerAlignment;
  } else {
    cellName = getCellName(temp_col + 3, temp_row);
    cell = worksheet.getCell(cellName);
    cell.value = CHECK_SYMBOL_UNICODE;
    cell.alignment = ExcelStyles.centerAlignment;
  }
  cellName = getCellName(temp_col + 2, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [{ font: ExcelStyles.bodyFont, text: "Yes" }],
  };
  cellName = getCellName(temp_col + 4, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [{ font: ExcelStyles.bodyFont, text: "No" }],
  };
  //Labor contract term:
  temp_row++;
  cellName = getCellName(temp_col, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [{ font: ExcelStyles.bodyFont, text: "Labor contract term:" }],
  };
  let startCellName = getCellName(temp_col + 1, temp_row);
  let endCellName = getCellName(temp_col + 5, temp_row);
  worksheet.mergeCells(startCellName + ":" + endCellName);
  worksheet.getCell(startCellName).value = {
    richText: [{ font: ExcelStyles.bodyFont, text: data.term }],
  };
  //Other actions and updates:
  temp_row++;
  cellName = getCellName(temp_col, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [
      { font: ExcelStyles.bodyFont, text: "Other actions and updates:" },
    ],
  };
  startCellName = getCellName(temp_col + 1, temp_row);
  endCellName = getCellName(temp_col + 5, temp_row);
  worksheet.mergeCells(startCellName + ":" + endCellName);
  worksheet.getCell(startCellName).value = {
    richText: [{ font: ExcelStyles.bodyFont, text: data.otherUpdateAction }],
  };
  //Director’s approval:
  temp_row++;
  cellName = getCellName(temp_col, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [{ font: ExcelStyles.bodyFont, text: "Director’s approval:" }],
  };
  if (data.approved) {
    cellName = getCellName(temp_col + 1, temp_row);
    cell = worksheet.getCell(cellName);
    cell.value = CHECK_SYMBOL_UNICODE;
    cell.alignment = ExcelStyles.centerAlignment;
  } else {
    cellName = getCellName(temp_col + 3, temp_row);
    cell = worksheet.getCell(cellName);
    cell.value = CHECK_SYMBOL_UNICODE;
    cell.alignment = ExcelStyles.centerAlignment;
  }
  cellName = getCellName(temp_col + 2, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [{ font: ExcelStyles.bodyFont, text: "Approve" }],
  };
  cellName = getCellName(temp_col + 4, temp_row);
  cell = worksheet.getCell(cellName);
  cell.value = {
    richText: [{ font: ExcelStyles.bodyFont, text: "Disapprove" }],
  };
  let fileName = "probation.xlsx";
  if (data.employeeName !== null) {
    fileName = data.employeeName;
  }
  workbook.xlsx.writeBuffer().then((data) => {
    const blob = new Blob([data], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    fs.saveAs(blob, fileName);
  });
}
