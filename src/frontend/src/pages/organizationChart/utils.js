import { TOTAL_WIDTH_BLOCK, TOTAL_HEIGHT_BLOCK } from "./static/constantValue";

function getTotalX(entityList) {
  return entityList.map((entity) => entity.x).reduce((a, b) => a + b, 0);
}

function retriveEntityList(level, entityDataArray, retriveFunction) {
  let entityList = [];
  entityDataArray.forEach((entityData) => {
    entityData.level = level;
    entityList.push(retriveFunction(entityData));
  });

  return entityList;
}

function getChildList(
  parent,
  childField,
  childListData,
  childLevel,
  retriveChildFunction
) {
  let totalChildWidth = 0,
    numberChild = 0;
  if (childListData !== null && childListData.length !== 0) {
    let childList = retriveEntityList(
      childLevel,
      childListData,
      retriveChildFunction
    );
    parent[childField] = childList;
    totalChildWidth = getTotalX(childList);
    numberChild = childList.length;
  }

  return {
    totalChildWidth,
    numberChild,
  };
}

function setCenterCoordinate(entity, x, y) {
  entity.setXY(x, y);
  entity.setCenter(TOTAL_WIDTH_BLOCK, TOTAL_HEIGHT_BLOCK);
}

function calculateWidth(childList) {
  let totalChildWidth = getTotalX(childList);
  let numberChild = childList.length;

  return totalChildWidth / numberChild;
}

export {
  getTotalX,
  retriveEntityList,
  setCenterCoordinate,
  calculateWidth,
  getChildList,
};
