
import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App.vue'
import DetailsPane from './DetailsPane.vue'
import HistoryPane from './HistoryPane.vue'

Vue.use(VueRouter)

const app = new Vue({
    el: '#App',

    router: new VueRouter({
        mode: 'history',

        routes: [
            { path: '/:table/:title', component: DetailsPane },
            { path: '/', component: HistoryPane }
        ]
    }),

    render: h => h(App)
})
