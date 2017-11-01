<template>
    <section id="TitlesPane">
        <input type="search" @input="changeQuery" />

            <hr />

            <ul class="titlesList" @click="selectTitle">
                <li v-for="title in filtered_titles" :key="title" :data-title="title"
                    :class="{ 'titlesList-item': true, 'active': title === selectedTitle }">{{ title }}</li>
            </ul>
    </section>
</template>

<script>
    import debounce from 'lodash.debounce'

    export default {
        name: 'titles-pane',

        props: ['selectedTitle', 'titles'],

        data () {
            return {
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

        updated () {
            let $pane = document.getElementById('TitlesPane')

            $pane.style.width = $pane.offsetWidth + 'px'
        },

        methods: {
            changeQuery: debounce(function(ev) {
                this.query = ev.target.value
            }, 150),

            selectTitle: function(ev) {
                if (undefined !== ev.target.dataset.title) {
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
        padding: 15px 20px

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
</style>