<template>
    <section id="TitlesPane" :class="{ 'menu_expanded': expand_menu }">
        <span class="menu" @click="expand_menu = !expand_menu">
            <span class="menu-inner"></span>
        </span>

        <div class="content">
            <input type="search" @input="changeQuery" />

            <hr />

            <ul class="titlesList" @click="selectTitle">
                <li v-for="title in filtered_titles" :key="title" :data-title="title"
                    :class="{ 'titlesList-item': true, 'active': title === selectedTitle }">{{ title }}</li>
            </ul>
        </div>
    </section>
</template>

<script>
    import debounce from 'lodash.debounce'

    export default {
        name: 'titles-pane',

        props: ['selectedTitle', 'titles'],

        data () {
            return {
                expand_menu: false,
                query: ''
            }
        },

        computed: {
            filtered_titles: function() {
                if (this.query) {
                    return this.titles.filter(t => t.toLowerCase().indexOf(this.query.toLowerCase()) !== -1)
                } else {
                    return this.titles
                }
            }
        },

        methods: {
            changeQuery: debounce(function(ev) {
                this.query = ev.target.value
            }, 150),

            selectTitle: function(ev) {
                if (undefined !== ev.target.dataset.title) {
                    this.expand_menu = false
                    document.getElementById('TitlesPane').scrollTop = 0

                    this.$emit('selectTitle', ev.target.dataset.title)
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

            &-item
                cursor: pointer
                margin: 0 auto
                padding: 0
                transition: all 0.05s ease

                &.active, &:hover
                    color: #03A9F4

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