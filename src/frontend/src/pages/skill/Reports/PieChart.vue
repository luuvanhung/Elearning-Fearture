<script>
import { Pie } from "vue-chartjs";

export default {
  extends: Pie,
  props: {
    skills: {
      type: Array,
      require: true,
    },
  },
  data() {
    return {
      options: {
        title: {
          display: true,
          text: "Skills Ratio",
          fontColor: "#707070",
          fontFamily: "Times New Roman",
          fontSize: 26,
          padding: 20,
        },
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          callbacks: {
            label: function (tooltipItem, data) {
              let dataset = data.datasets[tooltipItem.datasetIndex];
              let total = dataset.data.reduce((previousValue, currentValue) => {
                return previousValue + currentValue;
              });
              let currentValue = dataset.data[tooltipItem.index];
              let percentage = Math.floor((currentValue / total) * 100 + 0.5);
              return (
                data["labels"][tooltipItem["index"]] + ": " + percentage + "%"
              );
            },
          },
        },
      },
    };
  },
  mounted() {
    let colors = [];
    for (let i = 0; i < this.skills.length; i++) {
      colors.push("#" + Math.floor(Math.random() * 16777215).toString(16));
    }
    let datasets = [
      {
        label: "Skill Ratio",
        data: this.skills.map((skill) => skill.count),
        backgroundColor: colors,
        hoverOffset: 4,
      },
    ];
    this.renderChart(
      {
        labels: this.skills.map((skill) => skill.name),
        datasets,
      },
      this.options
    );
  },
};
</script>
