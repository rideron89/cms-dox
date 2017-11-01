<template>
    <div id="App">
        <titles-pane :selected-title="selected_title" :titles="titles" @selectTitle="(title) => selected_title = title"></titles-pane>

        <details-pane :title="selected_title" :content="selected_content"></details-pane>
    </div>
</template>

<script>
    import axios from 'axios'
    import store from 'store'

    import DetailsPane from './DetailsPane.vue'
    import TitlesPane from './TitlesPane.vue'

    export default {
        name: 'app',

        components: {
            DetailsPane,
            TitlesPane
        },

        data () {
            return {
                query: '',
                selected_content: null,
                selected_title: null,
                titles: []
            }
        },

        watch: {
            selected_title: function(title) {
                let cached = store.get('cached')
                let cached_item = cached.filter(row => row.title === title)

                // if the requested title is in the cache, load it from there
                if (cached_item.length) {
                    return this.selected_content = cached_item[0].content
                }

                axios('/api/title/' + encodeURIComponent(title)).then(response => {
                    if (!response.data.error) {
                        this.selected_content = response.data.data.content

                        // update the cached data
                        cached.push({ title: title, content: response.data.data.content })
                        store.set('cached', cached.slice(0, 20))
                    }
                })
            }
        },

        mounted () {
            // setup cached titles storage
            if (undefined == store.get('cached_titles')) {
                store.set('cached_titles', {})
            }

            // setup cached data storage
            if (undefined === store.get('cached')) {
                store.set('cached', [])
            }

            this.loadTitles()
        },

        methods: {
            loadTitles: function() {
                let cached_titles = store.get('cached_titles')
                let age = (Date.now() - parseInt(cached_titles.last_updated)) / 1000

                if (isNaN(age) || (age > 3600)) {
                    axios('/api/titles').then(response => {
                        if (!response.data.error) {
                            this.titles = response.data.data

                            this.selected_title = this.titles[0]

                            cached_titles = {
                                last_updated: Date.now(),
                                titles: this.titles
                            }

                            store.set('cached_titles', cached_titles)
                        }
                    })
                } else {
                    this.titles = cached_titles.titles

                    this.selected_title = this.titles[0]
                }
            }
        }
    }
</script>

<style lang="sass">
    @import url('https://fonts.googleapis.com/css?family=Merriweather:700|Nunito:400,700|Source+Code+Pro')

    *, *:before, *:after
        box-sizing: border-box

    html, body, button, input, select, textarea
        font-family: 'Nunito', Helvetica, Arial, sans-serif
        font-size: 16px
        line-height: 1.6

    html, body
        margin: 0 auto
        padding: 0

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

    tt
        font-family: 'Source Code Pro'
        font-size: inherit
        line-height: inherit

    #App
        display: flex
        height: 100vh

    #DetailsPane
        flex: auto
        overflow: auto

    #TitlesPane
        flex: 0 0 auto
        overflow: auto
</style>