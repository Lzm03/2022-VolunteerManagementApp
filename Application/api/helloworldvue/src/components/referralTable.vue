<template>

  <div class="grid-container">
    <div class="action_container"><table class="referral_table">
              <thead style="background-color: rgba(247, 247, 247, 1)">

              <tr style="font-size: 1rem;">
                <td rowspan="4" style="font-size: 1rem;font-weight:bold;">Referrals</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>

              </thead>
              <tbody>
              <tr style="background-color: rgba(223, 226, 230, 1); height: 1.5rem;">
                <th @click="sortTable('id')">ID<span class="sortable1" :class="{ active: activeButton === 0 }"></span></th>
                <th @click="sortTable('type')">Referral Type<span class="sortable1" :class="{ active: activeButton === 1 }"></span></th>
                <th @click="sortTable('resident')">Resident<span class="sortable1" :class="{ active: activeButton === 2 }"></span></th>
                <th @click="sortTable('created')">Created<span class="sortable1" :class="{ active: activeButton === 3 }"></span></th>
                <th @click="sortTable('status')">Status<span class="sortable1" :class="{ active: activeButton === 4 }"></span></th>
                <th @click="sortTable('organisation')">Organisation<span class="sortable1" :class="{ active: activeButton === 5 }"></span></th>
                <th @click="sortTable('completed')">Completed<span class="sortable1" :class="{ active: activeButton === 6 }"></span></th>
              </tr>

              <tr v-for="(item, index) in filteredData" :class="'tr-color-' + index % 2" :key="index" @click="handleClick(item.id)">
                <td class="table_hover">{{item.id}}</td>
                <td class="table_hover">{{item.type}}</td>
                <td class="table_hover">{{item.resident}}</td>
                <td class="table_hover">{{item.created}}</td>
                <td class="table_hover">{{item.status}}</td>
                <td class="table_hover">{{item.organisation}}</td>
                <td class="table_hover">{{item.completed}}</td>
              </tr>
              </tbody>
            </table></div>

    <div class="FilterComponent_container"><FilterComponent :selected-values="selectedValues1" @update="handleUpdate" class="referral_filterComponent"></FilterComponent></div>
  </div>


</template>

<script>
import $ from 'jquery';
import FilterComponent from '@/components/filter component/Referrals-filter.vue'

export default {
  data() {
    return {
      toggle: false,
      list: [
        {id:'1',type:'Dog Walking', resident:'John',created:'Fri, Feb 3, 2023 - 10:15am',status:'Complete',organisation:'Fliwood Food Centre',completed:'Mon, Feb 6, 2023 - 09:15am'},
        {id:'9',type:'Food Bank', resident:'Liu',created:'Mon, Jan 15, 2023 - 10:15am',status:'Complete',organisation:'Surgery',completed:'Mon, Feb 6, 2023 - 09:15am'},
        {id:'11',type:'Shopping', resident:'Bob',created:'Mon, Jan 8, 2023 - 10:15am',status:'Contacted',organisation:'Fliwood Food Centre',completed:'Mon, Jan 15, 2023 - 10:15am'},
        {id:'27',type:'Prescription', resident:'Ally',created:'Sun, Feb19 , 2023 - 10:15am',status:'Chosen',organisation:'Fliwood Food Centre',completed:'Sun, Feb19 , 2023 - 10:15am'},
        {id:'3',type:'Volunteer Assigned', resident:'Bill',created:'Sun, Feb12 , 2023 - 10:15am',status:'Complete',organisation:'Surgery',completed:'Sun, Feb12 , 2023 - 10:15am'},
        {id:'15',type:'Volunteer Assigned', resident:'Alice',created:'Wed, Aug 11, 2023 - 5:30pm',status:'Contacted',organisation:'Surgery'},
        {id:'17',type:'Dog Walking', resident:'Sid',created:'Mon, Jan 1, 2023 - 10:15am',status:'Pending',organisation:'Chosen'},
      ],
      referralStatus: [
          { id: 1, name: "Chosen" },
          { id: 2, name: "Contacted" },
          { id: 3, name: "Complete"},
        ],
      sortOrder:'',
      activeButton: -1,
      selectedValues1: [],
    }
  },
  props: {
    containerSize: {
      type: Number,
      required: true
    },
    left: {
      type: Number,
      required: false
    },
    top: {
      type: Number,
      required: false
    }
  },
  created() {
    this.tableData = this.$store.state.tableData
  },
  components: {
    FilterComponent,
  },
  computed:{
    filteredData() {
      if (this.selectedValues1.length === 0) {
        return this.list
      } else {
        return this.list.filter(item => {
          return this.selectedValues1.includes(item.type) ||
              this.selectedValues1.includes(item.status) ||
              this.selectedValues1.includes(item.organisation)
        })
      }
    },
  },
  methods: {
    handleUpdate(newValues) {
      this.selectedValues1 = newValues
    },
    toggleActive(index) {
      if (this.activeButton === index) {
        this.activeButton = -1;
      } else {
        this.activeButton = index;
      }
    },
    handleClick(id) {
      this.$router.push(`/referral_page/${id}`)
    },
    sortTable(sortKey) {
      if (this.sortOrder === sortKey) {
        this.list.reverse();
      } else {
        if (sortKey === 'id') {
          this.toggleActive(0);
          this.list.sort((a, b) => a[sortKey] - b[sortKey]);
        } else if (sortKey === 'type') {
          this.toggleActive(1);
          this.list.sort((a, b) => a[sortKey].localeCompare(b[sortKey]));
        } else if (sortKey === 'resident') {
          this.toggleActive(2);
          this.list.sort((a, b) => a[sortKey].localeCompare(b[sortKey]));
        } else if (sortKey === 'created') {
          this.toggleActive(3);
          this.list.sort((a, b) => new Date(a[sortKey]) - new Date(b[sortKey]));
        } else if (sortKey === 'status'){
          this.toggleActive(4);
          this.list.sort((a, b) => a[sortKey].localeCompare(b[sortKey]));
        } else if (sortKey === 'organisation'){
          this.toggleActive(5);
          this.list.sort((a, b) => a[sortKey] - b[sortKey]);
        }else if (sortKey === 'completed'){
          this.toggleActive(6);
          this.list.sort((a, b) => new Date(a[sortKey]) - new Date(b[sortKey]));
        }
        this.sortOrder = sortKey;
      }
    },
    baseURL: function(){
        return window.location.origin
      },
    toggleHide() {
      this.toggle = !this.toggle;
    },
    getReferrals: async function () {
      const csrftoken = this.getCookie('csrftoken')
      const json = await $.ajax({
        url: this.baseURL() + "/api/referrals/",
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken)
        },
        method: "GET",
        type: "GET",
        contentType: 'application/json',
        success: () => {
          //this.$emit('removed-action', response)
          console.log("success")
        },
        error: (err) => {
          console.error(JSON.stringify(err))
        }
      }).catch((err) => {
        console.err(JSON.stringify(err))
      })
      console.log(JSON.stringify(json))
      return json;
    },
    getCookie: function (name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    getResidentByID: async function(id){
      const csrftoken = this.getCookie('csrftoken')
      const json = await $.ajax({
        url: this.baseURL() + '/api/residents/',
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken)
        },
        method: "GET",
        type: "GET",
        contentType: 'application/json',
        success: () => {
          //this.$emit('removed-action', response)
          console.log("success")
        },
        error: (err) => {
          console.error(JSON.stringify(err))
        }
      }).catch((err) => {
        console.err(JSON.stringify(err))
      })
      console.log('GETRESIDENTBYIDCALL RETURN VALUE: ' + json.results.find(obj => obj.id === id).first_name)
      return json.results.find(obj => obj.id === id).first_name;
    },
    getOrganisationById: async function(id){
        const csrftoken = this.getCookie('csrftoken')
             const json = await $.ajax({
                 url: this.baseURL() + '/api/organisations/',
                 beforeSend: function (xhr) {
                 xhr.setRequestHeader('X-CSRFToken', csrftoken)
                 },
                 method: "GET",
                 type: "GET",
                 contentType: 'application/json',
                 success: () => {
                 //this.$emit('removed-action', response)
                 console.log("success")
                 },
                 error: (err) => {
                 console.error(JSON.stringify(err))
                 }
             }).catch((err) => {
                 console.err(JSON.stringify(err))
             })
             console.log('GETRESIDENTBYIDCALL RETURN VALUE: ' + json.results.find(obj => obj.id === id).name)
             if(json.results.find(obj => obj.id === id).name === null)
                return "None"
            else
                return json.results.find(obj => obj.id === id).name;
     },
    getReferralTypeByID: async function(id){
      const csrftoken = this.getCookie('csrftoken')
      const json = await $.ajax({
        url: this.baseURL() + '/api/referraltypes/',
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken)
        },
        method: "GET",
        type: "GET",
        contentType: 'application/json',
        success: () => {
          //this.$emit('removed-action', response)
          console.log("success")
        },
        error: (err) => {
          console.error(JSON.stringify(err))
        }
      }).catch((err) => {
        console.err(JSON.stringify(err))
      })
      console.log('GETRESIDENTBYIDCALL RETURN VALUE: ' + json.results.find(obj => obj.id === id).name)
      return json.results.find(obj => obj.id === id).name;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = date.toLocaleString('default', { month: 'long' });
      const day = date.getDate();
      return `${month} ${day}, ${year}`;
  },
    getStatusByID_referral: function (id) {
      return this.referralStatus[id - 1]
    },
  },
  async mounted(){
    let response = await this.getReferrals();
    response = response.results;
    console.log("GETREFERRALS RESPONSE: " + JSON.stringify(response));
    this.list = await Promise.all(response.map(async (result) => {
    return {
      id: result.id,
      resident: await this.getResidentByID(result.resident),
      type: await this.getReferralTypeByID(result.referral_type),
      created: this.formatDate(result.created_datetime),
      status: this.getStatusByID_referral(result.referral_status).name,
      organisation: await this.getOrganisationById(result.referral_organisation),
      completed: this.formatDate(result.completed_date)
    };
    }));
    
  },
}
</script>

<style>
.referral_table {
  table-layout: fixed;
  border-collapse: collapse;
  border-spacing: 50px;
  font-size: 12px;
  width: 100%;
  margin-left: 10px;
  background-color: #f8f8f8;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
@media (max-width: 900px) {
  .referral_table{
    width: 100%;
    margin-left: 0px;
  }
}

 th,td{
  border: none;
}

 th {
  background-color: rgba(234, 236, 239, 1);
  color: black;
  font-weight: bold;
  text-align: left;
   padding: 0.75rem 1rem;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
}

td {
  padding: 0.75rem 2rem;
  border-bottom: 1px solid #ddd;
  color: #333;
}

.referral_filterComponent{
  position: static;
  background: #ebecf0;
  color: rgba(31, 31, 31, 0.7);
  border-radius: 0.5rem;
  width: 12rem;
  border: 0.1rem solid #f7f7f7;
  top: 400px;
}

/*.table-container {*/
/*    box-sizing: border-box;*/
/*    position: absolute;*/
/*    width: 1229px;*/
/*    height: 854px;*/
/*    left: 20px;*/
/*    top: 194px;*/
/*    background: rgb(212, 215, 211);*/
/*    border: 1px solid #DFDFDF;*/
/*    border-radius: 5px;*/
/*  }*/

/*.table {*/
/*  border: 1px solid #f5f5f5;*/
/*  border-radius: 5px;*/
/*  margin: 0 auto;*/
/*  border-spacing: 0px;*/
/*  width: 100%;*/
/*  max-width: 100%;*/
/*  margin: 0;*/
/*}*/

/*.table1 {*/
/*  background: #ebecf0;*/
/*  color: rgba(31, 31, 31, 0.7);*/
/*  border-radius: 5px;*/
/*  margin: 0 auto;*/
/*  border: 1px solid #f7f7f7;*/
/*  width: 200px;*/
/*  position: absolute;*/
/*  right: -220px;*/
/*  top: 0;*/
/*}*/

/*select {*/

/*  !* styling *!*/
/*  background-color: white;*/
/*  border: black;*/
/*  border-radius: 4px;*/
/*  display: inline-block;*/
/*  font: inherit;*/
/*  line-height: 1.5em;*/
/*  padding: 0.5em 0.1em 0.5em 0.5em;*/
/*}*/


/*th {*/
/*  background-color: #ebecf0;*/
/*  color: rgba(31, 31, 31, 0.7);*/
/*  cursor: pointer;*/
/*  text-align: left;*/
/*}*/


/*td {*/
/*  font-size: 13px;*/
/*  height: 30px;*/
/*}*/

/*th,*/
/*td {*/
/*  min-width: 90px;*/
/*  padding: 10px 10px;*/

/*}*/

/*!* 定义余数为 0 的行颜色 *!*/

/*.tr-color-0 {*/
/*  background: #f2f2f2;*/
/*}*/

/*!* 定义余数为 1 的行颜色 *!*/

/*.tr-color-1 {*/
/*  background: #fff;*/
/*}*/

/*.arrow {*/
/*  display: inline-block;*/
/*  vertical-align: middle;*/
/*  width: 0;*/
/*  height: 0;*/
/*  margin-left: 5px;*/
/*  opacity: 0.66;*/
/*}*/

/*.arrow.asc {*/
/*  border-left: 4px solid transparent;*/
/*  border-right: 4px solid transparent;*/
/*  border-bottom: 4px solid #4c4b50;*/
/*}*/

/*.arrow.dsc {*/
/*  border-left: 4px solid transparent;*/
/*  border-right: 4px solid transparent;*/
/*  border-top: 4px solid #4c4b50;*/
/*}*/
</style>