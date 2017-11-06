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
                content: '<div>Nothing</div>',
                title: null
            }
        },

        mounted () {
            if (this.$route.params && this.$route.params.table && this.$route.params.title) {
                this.loadTitle(this.$route.params.table, this.$route.params.title)
            }
        },

        watch: {
            '$route': function(to, from) {
                if (to.params && to.params.table && to.params.title) {
                    this.loadTitle(to.params.table, to.params.title)
                }
            }
        },

        methods: {
            addToCached: function(table, title, content) {
                let cached = (store.get('cached') || []).filter(r => title !== r.title)

                cached.push({ table: table, title: title, content: content })

                store.set('cached', cached.slice(0, 30))
            },

            addToHistory: function(table, title) {
                let history = (store.get('history') || []).filter(h => {
                    return !(h.title === title && h.table === table)
                })

                history.unshift({ table: table, title: title, time: Date.now() / 1000 })
                store.set('history', history.slice(0, 20))
            },

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