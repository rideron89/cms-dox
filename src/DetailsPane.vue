<template>
    <div id="DetailsPane">
        <div class="inner">
            <router-link to="/">Home</router-link>

            <h1>{{ title }}</h1>

            <hr />

            <div v-html="content"></div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import store from 'store'

    export default {
        name: 'details-pane',

        data () {
            return {
                // string: HTML for the action/function content section
                content: '<div>Nothing</div>',

                // string: string for the action/function title
                title: ''
            }
        },

        /**
        * When the component is mounted, load the data for the title if the table and title is
        * found in the URL path.
        */
        mounted () {
            if (this.$route.params && this.$route.params.table && this.$route.params.title) {
                this.loadTitle(this.$route.params.table, this.$route.params.title)
            }
        },

        /**
        * When the component is updated, force scroll the pane back to the top.
        */
        updated () {
            document.getElementById('DetailsPane').scrollTop = 0
        },

        watch: {
            /**
            * When the `$route` object is changed, load a title if it is in the URL path.
            *
            * @param to: route object
            * @param from: route object
            */
            '$route': function(to, from) {
                if (to.params && to.params.table && to.params.title) {
                    this.loadTitle(to.params.table, to.params.title)
                }
            }
        },

        methods: {
            /**
            * Add the title and its content to the cache.
            *
            * @param table: string
            * @param title: string
            * @param content: string
            */
            addToCached: function(table, title, content) {
                let cached = (store.get('cached') || []).filter(r => title !== r.title)

                cached.push({ table: table, title: title, content: content })

                store.set('cached', cached.slice(0, 30))
            },

            /**
            * Add the title to the history list.
            *
            * @param table: string
            * @param title: string
            */
            addToHistory: function(table, title) {
                let history = (store.get('history') || []).filter(h => {
                    return !(h.title === title && h.table === table)
                })

                history.unshift({ table: table, title: title, time: Date.now() / 1000 })
                store.set('history', history.slice(0, 20))
            },

            /**
            * Try loading the content for a title by checking the cache. If the title wasn't found
            * then request the content from the server, and then add it to the cache. Add the
            * title to the history list.
            *
            * @param table: string
            * @param title: string
            */
            loadTitle: function(table, title) {
                let cached  = (store.get('cached') || []).filter(r => {
                    return (title === r.title) && (table === r.table)
                })[0]

                if (cached) {
                    this.content = cached.content
                    this.title   = cached.title
                } else {
                    axios(`/api/${table}/${title}`).then(response => {
                        this.content = response.data.data.content
                        this.title   = title

                        this.addToCached(table, title, response.data.data.content)
                    })
                }

                this.addToHistory(table, title)
            }
        }
    }
</script>

<style lang="sass">
    #DetailsPane
        background: #f3f4f4
        color: #2c2c2c
        padding: 25px 25px 25px 15px

        .inner
            background: #fefefe
            border-radius: 4px
            box-shadow: 0px 0px 5px 0px #e4e4e4
            overflow: auto
            padding: 25px
</style>