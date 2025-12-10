<script setup lang="ts">
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';

// Register ECharts components
use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
]);

// Define Props
const props = defineProps<{
  data: Array<{ recorded_time: string; value: number }>; // Data from API
  pollutant: string; // e.g., 'pm25', 'pm10'
  color?: string; // Optional chart color
}>();

// Chart Configuration (Reactive)
const option = computed(() => {
  const dates = props.data.map(item => {
    // Format date to MM-DD
    const date = new Date(item.recorded_time);
    return `${date.getMonth() + 1}-${date.getDate()}`;
  });
  const values = props.data.map(item => item.value);

  return {
    title: {
      text: `${props.pollutant.toUpperCase()} Trend`,
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisTick: { alignWithLabel: true },
    },
    yAxis: {
      type: 'value',
      name: 'Concentration (µg/m³)',
    },
    series: [
      {
        name: props.pollutant.toUpperCase(),
        type: 'bar',
        barWidth: '60%',
        data: values,
        itemStyle: {
          color: props.color || '#5470c6',
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
