<script setup lang="ts">
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import {
  TooltipComponent,
  LegendComponent,
  TitleComponent,
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  PieChart,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
]);

const props = defineProps<{
  data: Array<{ aqi_level: string }>;
}>();


const aqiColors: Record<string, string> = {
  'good': '#00e400',
  'moderate': '#ffff00',
  'mild pollution': '#ff7e00',
  'moderate pollution': '#ff0000',
  'severe pollution': '#99004c',
  // Fallback
  'Unknown': '#ccc'
};

const option = computed(() => {
  // Count occurrences of each AQI Level
  const counts: Record<string, number> = {};
  props.data.forEach((item) => {
    const level = item.aqi_level || 'Unknown';
    counts[level] = (counts[level] || 0) + 1;
  });

  // Format for ECharts
  const chartData = Object.keys(counts).map((level) => ({
    value: counts[level],
    name: level,
    itemStyle: { color: aqiColors[level] || '#999' }
  }));

  return {
    title: {
      text: 'AQI Level Distribution',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: 'AQI Level',
        type: 'pie',
        radius: '50%',
        data: chartData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };
});
</script>

<template>
  <div class="chart-container">
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<style scoped>
.chart-container {
  height: 300px;
  width: 100%;
}
.chart {
  height: 100%;
  width: 100%;
}
</style>
