<template>
    <div id="App">
        <titles-pane :titles="titles"></titles-pane>

        <router-view></router-view>
    </div>
</template>

<script>
    import axios from 'axios'
    import store from 'store'

    import TitlesPane from './TitlesPane.vue'

    export default {
        name: 'app',

        components: {
            TitlesPane
        },

        data () {
            return {
                titles: { actions: [], functions: [] }
            }
        },

        mounted () {
            this.loadTitles()
        },

        methods: {
            loadTitles: function() {
                let cached_titles = store.get('cached_titles') || {}
                let age = (Date.now() - parseInt(cached_titles.last_updated)) / 1000

                if (isNaN(age) || age > 3600) {
                    axios('/api/titles').then(response => {
                        if (response.data.error) {
                            return console.log(response.data.data)
                        }

                        cached_titles = { load_updated: Date.now(), titles: response.data.data }

                        store.set('cached_titles', cached_titles)

                        this.titles = cached_titles.titles
                    })
                } else {
                    this.titles = cached_titles
                }
            }
        }
    }
</script>

<style lang="sass">
    @import url('https://fonts.googleapis.com/css?family=Merriweather:700|Nunito:400,700|Source+Code+Pro')

    *, *:before, *:after
        box-sizing: border-box

    html, body
        font-family: 'Nunito', Helvetica, Arial, sans-serif
        font-size: 16px
        line-height: 1.6
        margin: 0 auto
        padding: 0

    a
        box-shadow: inset 0px -1px 0px 0px currentColor
        color: #03A9F4
        text-decoration: none
        transition: all 0.125s ease

        &:hover
            box-shadow: inset 0px 0px 0px 0px currentColor

    button, input, select, textarea
        font: inherit
        line-height: inherit

    h1, h2, h3, h4, h5, p, ol, ul
        margin: 20px auto 15px

        pre &
            display: inline
            font: inherit

        &:first-child
            margin-top: 0

        &:last-child
            margin-bottom: 0

    h1, h2, h3, h4, h5
        font-family: 'Merriweather'

    hr
        background: #03A9F4
        border-radius: 3px
        border: 0
        height: 2px
        margin: 20px 0

    input
        background: #fefefe
        border-radius: 2px
        border: 0
        font-size: 14px
        line-height: 1
        margin: 0 auto
        padding: 6px 8px
        width: 100%

    pre, tt
        font-family: 'Source Code Pro'
        font-size: 12px
        line-height: inherit
        white-space: pre-wrap

    #App
        display: flex
        height: 100vh

    #HistoryPane,
    #DetailsPane
        flex: auto
        overflow: auto

    #TitlesPane
        flex: 0 0 auto
        overflow: auto

    @media (max-width: 1024px)
        pre
            white-space: normal

    @media (max-width: 768px)
        html, body
            font-size: 14px
</style>