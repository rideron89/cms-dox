<template>
    <div id="HistoryPane">
        <div class="inner">
            <h1>cms-dox</h1>

            <hr />

            <p>Welcome to <strong>cms-dox</strong>, a web app for browsing various CMS library documentation, much like the incredible <a href="http://devdocs.io/" target="_blank">DevDocs</a>. Currently, we only support <em>actions</em> and <em>functions</em> of WordPress.</p>

            <h3>Recently Viewed Items</h3>

            <ul class="historyList">
                <li v-for="(item, index) in sorted_history" :key="index">
                    <router-link :to="'/' + item.table + '/' + item.title">{{ item.title }}</router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import store from 'store'

    export default {
        name: 'history-pane',

        data () {
            return {
                history: store.get('history') || []
            }
        },

        computed: {
            sorted_history: function() {
                return this.history.sort((a, b) => {
                    if (a.time === b.time) {
                        return 0
                    }

                    return a.time < b.time
                })
            }
        }
    }
</script>

<style lang="sass">
    #HistoryPane
        background: #f3f4f4
        color: #2c2c2c
        padding: 25px 25px 25px 15px

        .inner
            background: #fefefe
            border-radius: 4px
            box-shadow: 0px 0px 5px 0px #e4e4e4
            overflow: auto
            padding: 25px

        .historyList
            list-style: none
            margin: 0 auto
            padding: 0
</style>