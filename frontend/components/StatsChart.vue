<template>
  <div class="bo-chart-container">
    <div class="bo-chart-title fr-pb-2w">
      {{ title }}
    </div>

    <!-- Toggle Chart Type -->
    <div class="fr-tabs" style="box-shadow: none; margin-bottom: 1.5rem">
      <ul class="fr-tabs__list" role="tablist" style="padding: 0">
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentType === 'line'"
            role="tab"
            style="padding: 0.25rem 1rem"
            @click="currentType = 'line'"
          >
            Évolution (Ligne)
          </button>
        </li>
        <li role="presentation">
          <button
            class="fr-tabs__tab"
            :aria-selected="currentType === 'bar'"
            role="tab"
            style="padding: 0.25rem 1rem"
            @click="currentType = 'bar'"
          >
            Résultats (Barres)
          </button>
        </li>
      </ul>
    </div>

    <!-- ChartJS Area -->
    <div style="position: relative; height: 260px; width: 100%">
      <LineChart v-if="currentType === 'line'" :data="lineChartData" :options="chartOptions" />
      <BarChart v-else :data="barChartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js'
import { computed, ref } from 'vue'
import { Bar as BarChart, Line as LineChart } from 'vue-chartjs'

// Register ChartJS modules
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Filler
)

export default {
  name: 'StatsChart',
  components: {
    LineChart,
    BarChart,
  },
  props: {
    title: {
      type: String,
      default: 'Statistiques des procédures',
    },
    data: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const currentType = ref('line')

    const labels = computed(() => props.data.map((item) => item.date))

    // Line Chart Dataset Config
    const lineChartData = computed(() => ({
      labels: labels.value,
      datasets: [
        {
          label: 'Total procédures actives',
          backgroundColor: 'rgba(0, 0, 145, 0.1)',
          borderColor: '#000091',
          borderWidth: 3,
          pointBackgroundColor: '#000091',
          pointBorderColor: '#fff',
          pointBorderWidth: 1.5,
          pointRadius: 5,
          pointHoverRadius: 7,
          tension: 0.35, // Smooth curves (Bezier)
          fill: true,
          data: props.data.map((item) => item.total),
        },
      ],
    }))

    // Bar Chart Dataset Config
    const barChartData = computed(() => ({
      labels: labels.value,
      datasets: [
        {
          label: 'Procédures avec succès',
          backgroundColor: '#22C55E',
          borderRadius: 4,
          data: props.data.map((item) => item.success),
        },
        {
          label: 'Procédures abandonnées',
          backgroundColor: '#EF4444',
          borderRadius: 4,
          data: props.data.map((item) => item.abandoned),
        },
      ],
    }))

    // Common Chart Options
    const chartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            boxWidth: 12,
            font: {
              family: 'Inter, system-ui, sans-serif',
              size: 11,
              weight: 'bold',
            },
            color: '#4B5563',
          },
        },
        tooltip: {
          backgroundColor: '#0F172A',
          titleColor: '#93C5FD',
          bodyColor: '#F8FAFC',
          padding: 10,
          cornerRadius: 6,
          boxWidth: 8,
          boxPadding: 4,
          font: {
            family: 'Inter, system-ui, sans-serif',
          },
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: '#4B5563',
            font: {
              weight: 'bold',
              size: 10,
            },
          },
        },
        y: {
          border: {
            dash: [4, 4],
          },
          grid: {
            color: '#E5E7EB',
          },
          ticks: {
            color: '#4B5563',
            font: {
              weight: 'bold',
              size: 10,
            },
          },
        },
      },
    }))

    return {
      currentType,
      lineChartData,
      barChartData,
      chartOptions,
    }
  },
}
</script>
