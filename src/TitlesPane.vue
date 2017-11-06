<template>
    <section id="TitlesPane" :class="{ 'menu_expanded': expand_menu }">
        <span class="menu" @click="expand_menu = !expand_menu">
            <span class="menu-inner"></span>
        </span>

        <div class="content">
            <input type="search" :value="query" @input="changeQuery" />

            <hr />

            <label class="titlesList-label">Actions</label>
            <ul class="titlesList" @click="selectTitle">
                <li v-for="action in filtered_actions" :key="action"
                    :class="{ 'titlesList-item': true, 'active': ('actions' === route_table) && (action === selected_title) }">
                    <a :href="'/actions/' + action" data-table="actions" :data-title="action">{{ action }}</a>
                </li>
            </ul>

            <br />

            <label class="titlesList-label">Functions</label>
            <ul class="titlesList" @click="selectTitle">
                <li v-for="func in filtered_functions" :key="func"
                    :class="{ 'titlesList-item': true, 'active': ('functions' === route_table) && (func === selected_title) }">
                    <a :href="'/functions/' + func"  data-table="functions" :data-title="func">{{ func }}</a>
                </li>
            </ul>
        </div>
    </section>
</template>

<script>
    import debounce from 'lodash.debounce'

    export default {
        name: 'titles-pane',

        props: ['titles'],

        data () {
            return {
                // boolean: true if the mobile menu should be shown, false otherwise
                expand_menu: false,

                // string: table name found in the URL path
                route_table: (this.$route.params) ? this.$route.params.table : null,

                // string: title found in the URL path
                selected_title: (this.$route.params) ? this.$route.params.title : null,

                // string: search query
                query: ''
            }
        },

        computed: {
            /**
            * Return a list of action titles that match the search query.
            *
            * @return array
            */
            filtered_actions: function() {
                return this.titles.actions.filter(a => {
                    return a.toLowerCase().indexOf(this.query.toLowerCase()) !== -1
                }) || this.titles.actions
            },

            /**
            * Return a list of function titles that match the search query.
            *
            * @return array
            */
            filtered_functions: function() {
                return this.titles.functions.filter(a => {
                    return a.toLowerCase().indexOf(this.query.toLowerCase()) !== -1
                }) || this.titles.functions
            }
        },

        watch: {
            /**
            * When the `$route` object changes, set the selected table and title.
            *
            * @param to: route object
            * @param from: route object
            */
            '$route': function(to, from) {
                let params = to.params || {}

                this.route_table = params.table

                this.selected_title = params.title
            }
        },

        methods: {
            /**
            * A debounced function that updates the component `query`.
            *
            * @param ev: EventObject
            */
            changeQuery: debounce(function(ev) {
                this.query = ev.target.value
            }, 150),

            /**
            * Update the URL when a title is selected.
            *
            * @param ev: EventObject
            */
            selectTitle: function(ev) {
                ev.preventDefault()

                let table = ev.target.dataset.table
                let title = encodeURIComponent(ev.target.dataset.title)

                if (table && title) {
                    this.expand_menu = false

                    document.getElementById('TitlesPane').scrollTop = 0

                    this.$router.push({ path: `/${table}/${title}` })
                }
            }
        }
    }
</script>

<style lang="sass">
    #TitlesPane
        background: #2b2d2e
        color: #dddede
        font-size: 14px
        margin-right: 0
        padding: 15px 20px
        position: relative
        left: 0
        top: 0
        width: 355px

        .menu
            display: none
            height: 24px
            margin-bottom: 15px
            margin-left: auto
            margin-right: 0
            overflow: hidden
            position: relative
            width: 25px

            &-inner
                background: #dddede
                border-radius: 4px
                display: block
                height: 3px
                position: absolute
                top: 3px
                transition: transform 0.15s ease
                width: 24px

                &:before, &:after
                    background: #dddede
                    border-radius: 4px
                    content: ""
                    display: block
                    height: 3px
                    position: absolute
                    transition: all 0.15s ease
                    width: 24px

                &:before
                    top: 8px

                &:after
                    top: 16px

        .titlesList
            list-style: none
            margin: 0 auto
            padding: 0

            &-label
                color: #888
                display: block
                font-weight: 700
                letter-spacing: 0.015em
                margin: 0 0 5px
                text-transform: uppercase

            &-item
                cursor: pointer
                margin: 0 auto
                padding: 0
                transition: all 0.05s ease

                &.active, &:hover
                    color: #03A9F4

                a, a:active, a:focus, a:hover
                    box-shadow: none
                    color: inherit
                    display: block
                    text-decoration: inherit

        @media (max-width: 1023px)
            overflow: hidden
            transition: all 0.15s ease
            width: 65px !important

            &.menu_expanded
                margin-right: calc(-100% + 65px)
                max-width: calc(90vw - 20px)
                overflow: auto
                width: 350px !important

                .content
                    left: 0

            .menu
                display: block

            .content
                position: relative
                left: 80px
                transition: all 0.15s ease
</style>