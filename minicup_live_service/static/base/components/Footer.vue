<template>
    <div class="footer">
        <b-container>
            <b-row>
                <b-col>
                    <slot></slot>
                </b-col>
                <b-col class="text-right">
                    2018 © Josef Kolář
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    export default {
        name: "Footer"
    }
</script>

<style scoped>
    .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        /* Set the fixed height of the footer here */
        height: 60px;
        line-height: 60px; /* Vertically center the text there */
        background-color: #f5f5f5;
    }
</style>