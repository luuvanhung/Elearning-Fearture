export default {
  GET_TYPE_OFF(state, data) {
    state.typeOff = data;
  },

  UPDATE_LIST_TYPE_OFF(state, payLoad) {
    const offTypeEdit = state.typeOff.find(
      (item) => item.id === payLoad.dataUpdate.id
    );
    const indexOffTypeGroup = payLoad.rootState.offTypeGroup.typeOffGroup.find(
      (item) => item.id === payLoad.dataUpdate.leave_type_group
    );
    const indexTitle = payLoad.rootState.title.titles.find(
      (item) => item.id === payLoad.dataUpdate.approval_title
    );
    const data = {
      id: payLoad.dataUpdate.id,
      name: payLoad.dataUpdate.name,
      leave_type_group: payLoad.dataUpdate.leave_type_group,
      days: payLoad.dataUpdate.days,
      is_count: payLoad.dataUpdate.is_count,
      descriptions: payLoad.dataUpdate.descriptions,
      approval_title: payLoad.dataUpdate.approval_title,
      approval_title_name: indexTitle.title,
      is_active: payLoad.dataUpdate.is_active,
      name_type: indexOffTypeGroup.name,
    };
    if (offTypeEdit) {
      offTypeEdit.name = data.name;
      offTypeEdit.is_count = data.is_count;
      offTypeEdit.days = data.days;
      offTypeEdit.name_type = data.name_type;
      offTypeEdit.leave_type_group = data.leave_type_group;
      offTypeEdit.descriptions = data.descriptions;
      offTypeEdit.approval_title = data.approval_title;
      offTypeEdit.approval_title_name = data.approval_title_name;
    } else {
      const index = state.typeOff.findIndex(
        (item) => item.name_type === data.name_type
      );
      state.typeOff.splice(index, 0, data);
    }
  },
  DELETE_TYPE_OFF(state, data) {
    const index = state.typeOff.findIndex((item) => item.id === data.id);
    state.typeOff = [
      ...state.typeOff.slice(0, index),
      ...state.typeOff.slice(index + 1),
    ];
  },
};
