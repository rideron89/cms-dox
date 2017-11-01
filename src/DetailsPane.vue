<template>
    <div id="DetailsPane">
        <div class="inner">
            <h1>{{ title }}</h1>

            <div v-html="content"></div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'details-pane',

        props: ['content', 'title'],

        data () {
            return {}
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
            padding: 25px
</style>