<template>
  <div style="height: 315px">
   <v-text-field
         v-model="this.searchTerm"
         hide-details
         label="Filter IPs"
          dense
></v-text-field>
  <VueTableLite
    :max-height="210"
    :columns="this.table.columns"
    :rows="this.table.rows"
    :total="this.table.totalRecordCount"
    :sortable="this.table.sortable"
    :messages="this.table.messages"
    :hide-default-footer="true"
  ></VueTableLite>
    </div>
</template>

<script>
import {reactive, computed, ref} from "vue";
import VueTableLite from 'vue3-table-lite';

export default {
  name: "IPFrequencyGraph",
  props: {graph_title: String, data: Object, colors: Object},
  components: { VueTableLite },
  setup(props) {
    const searchTerm = ref(""); // Search text
    // Fake data
    const table_data = reactive([]);
    for (const [key, value] of Object.entries(props.data)) {
      table_data.push({
        id: key,
        healthy_src: value["healthy_src"],
        healthy_dst: value["healthy_dst"],
        infected_dst: value["infected_dst"],
        infected_src: value["infected_src"],
      });
    }

    // Table config
    const table = reactive({
      columns: [
        {
          label: "IP Address",
          field: "id",
          width: "10%",
          sortable: true,
          isKey: true,
        },
        {
          columnStyles: { background: '#b5f3dd'},
          label: "H Src",
          field: "healthy_src",
          width: "2%",
          sortable: true,
        },
        {
          columnStyles: { background: '#b5f3dd'},
          label: "H Dst",
          field: "healthy_dst",
          width: "2%",
          sortable: true,
        },

        {
          columnStyles: { background: '#ea9ec6'},
          label: "I Src",
          field: "infected_src",
          width: "52%",
          sortable: true,
        },
                  {
                    columnStyles: { background: '#ea9ec6'},
          label: "I Dst",
          field: "infected_dst",
          width: "5%",
          sortable: true,
        },
      ],
      rows: computed(() => {
        return table_data.filter(
          (x) => String(x["id"]).includes(searchTerm.value.toLowerCase()));
      }),
            messages: {
        pagingInfo: "Total {2}",
        pageSizeChangeLabel: "Rows ",
        gotoPageLabel: "Page ",
        noDataAvailable: "No Data Available",
      },
      totalRecordCount: computed(() => {
        return table.rows.length;
      }),
      sortable: {
        order: "IP address",
        sort: "asc",
      },

    });
    return {
      searchTerm,
      table,
    };
  },
  methods: {},
}
</script>

<style scoped>

</style>