import Vue from 'vue'
import VueRouter from 'vue-router'
import aHeader from "@/components/aHeader";
import actionTable from '@/components/myTable'
import All_Activity from "@/components/All_Activity.vue";
import MyVolunteers from '@/components/MyVolunteers'
import referralTable from "@/components/referralTable"
import MyOrganisations from './components/myOrganisation'
import residentPage from '@/components/residentPage'
import MyResident from '@/component/MyResident'
import Router from 'vue-router'
import Start_Call from "@/components/Start_Call";
import action_page from "@/components/action_page";
import referral_page from "@/components/referral_page";
import volunteer_page from '@/components/volunteer_page'
import UpdateResidentForm from "@/components/UpdateResidentForm.vue";


Vue.use(Router)

const routes = [
    //localhost:8080/header means you are going to Header page(probably case sensitive)
    {
        path: '/static-built/src/vue/dist/',
        component: aHeader,
        children: [
            {
                path: '/AllActivity',
                name: "All_Activity",
                component: All_Activity,
            },
            {
                path: '/Actions',
                name: 'Actions',
                component: actionTable
            },
            {
                path: '/Referrals',
                name: 'Referrals',
                component: referralTable
            },
            {
                path: '/Start_Call',
                name: ' Start_call',
                component: Start_Call,
                children: [
                    {
                        path: '/add/:id',
                        name: 'add',
                        component: residentPage
                    }
                ]
            },
            {
                path: '/Residents',
                name: 'Residents',
                component: MyResident
            },
            {
                path: '/Volunteers',
                name: 'Volunteers',
                component: MyVolunteers
            },
            {
                path: '/Organisations',
                name: 'Organisations',
                component: MyOrganisations
            },
            {
                path: './action_page/:id',
                name: 'action_page',
                component: action_page
            },
            {
                path: './referral_page/:id',
                name: 'referral_page',
                component: referral_page
            },
            {
                path: './volunteer_page/:id',
                name: 'volunteer_page',
                component: volunteer_page
            },
            { path: '/updateResident/:id',
                component: UpdateResidentForm,
                name: 'UpdateResidentForm'},
        ]
    }


]

const router = new VueRouter({
    mode: 'history',
    routes
})


