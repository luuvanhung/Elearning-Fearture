export default {
  GET_TYPE_OFF_GROUP(state, data) {
    state.typeOffGroup = data;
  },

  UPDATE_TYPE_OFF_GROUP(state, data) {
    let payTypeEdit = state.typeOffGroup.find((item) => item.id === data.id);
    if (!payTypeEdit) {
      state.typeOffGroup.push(data);
    } else {
      payTypeEdit.name = data.name;
      payTypeEdit.is_company_pay = data.is_company_pay;
      payTypeEdit.is_insurance_pay = data.is_insurance_pay;
    }
  },

  DELETE_TYPE_OFF_GROUP(state, data) {
    const index = state.typeOffGroup.indexOf(
      state.typeOffGroup.find((item) => item.id === data.id)
    );
    state.typeOffGroup = [
      ...state.typeOffGroup.slice(0, index),
      ...state.typeOffGroup.slice(index + 1),
    ];
  },
};
