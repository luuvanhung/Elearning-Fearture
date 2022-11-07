<script>
import { Bar } from "vue-chartjs";

export default {
  extends: Bar,
  props: {
    chartData: {
      type: Array,
      require: true,
    },
    uniqueLevels: {
      type: Array,
      require: true,
    },
  },
  data() {
    return {
      options: {
        title: {
          display: true,
          text: "Level by Skill",
          fontColor: "#707070",
          fontFamily: "Times New Roman",
          fontSize: 26,
          padding: 20,
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              stacked: true,
              ticks: {
                fontSize: 18,
                fontStyle: "bold",
              },
            },
          ],
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontSize: 16,
              },
              stacked: true,
            },
          ],
        },
      },
    };
  },
  mounted() {
    const skill = this.chartData.map((e) => e.name);
    this.uniqueLevels.forEach((level) => {
      level.result = [];
      for (let i = 0; i < this.chartData.length; i++) {
        let levelCount = this.chartData[i].level[level.name];
        level.result[i] = levelCount === undefined ? 0 : levelCount.count;
      }
    });
    let colors = {};
    this.uniqueLevels.forEach((element) => {
      colors[element.name] =
        "#" + Math.floor(Math.random() * 16777215).toString(16);
    });
    let datasets = this.uniqueLevels.map((element) => {
      return {
        label: element.name,
        backgroundColor: colors[element.name],
        data: element.result,
      };
    });
    this.renderChart(
      {
        labels: skill,
        datasets,
      },
      this.options
    );
  },
};
</script>
