export default {
  titles: (state) => {
    let titles = state.titles.reduce((list, x) => {
      list.push(x.title);
      return list;
    }, []);
    return titles;
  },
};
