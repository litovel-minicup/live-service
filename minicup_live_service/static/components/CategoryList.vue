<template>
    <b-container>
        <b-row class="mt-2">
            <template v-for="cat in categories">
                <b-col :key="cat.id" cols="6">
                    <b-btn
                            variant="primary"
                            block class="btn-score"
                            @click="setCategory(cat.id)"
                    >
                        {{ cat.name }}
                    </b-btn>
                </b-col>
            </template>
        </b-row>
        <hr>
        <h1>Zápis online výsledků</h1>
        <p class="lead">
            Zdravím,<br>
            právě jsi v administraci živých přenosů na letošním turnaji Litovel MINICUP 2018. <br>
            Věnuj prosím chvíli následujícím pokynům:
        </p>
        <ul>
            <li>
                Veškeré zadané výsledky jdou zcela živě na webové stránky turnaje, jeho Facebook a někdy i přímo do video přenosů.
            </li>

            <li>
                Před začátkem zápasu si vyber kategorii a konkrétní zápas k zápisu.
                <strong>Tento výběr prosím ještě jednou zkontroluj.</strong>
            </li>
            <li>
                Se spuštěním časomíry na začátku obou poločasů zapni i časovač zde.
            </li>
            <li>
                Během zápasu se staráš o dvě věci:
                <ul>
                    <li>Spuštění času na začátku obou poločasů - poté je vše autonomní až do přestávky.</li>
                    <li>Zápis gólů dle jednotlivých střelců.</li>
                </ul>
            </li>
            <li>
                Když se spleteš ve střelci, nevadí, poslední branku je možné smazat do minuty od jejího zadání. Správného střelce poté zadáš standardní cestou.
            </li>
            <li>
                V případě, že jsi neviděl střelce/není na soupisce, použij výchozího střelce s názvem <i>Neznámý hráč</i>.
            </li>
            <li>
                <strong>Jestliže vypadne internet, zapisuj dále - ikonka v pravém horním rohu Ti ukáže, kdy dojde ke znovupřipojení. V případě, že internet nejde delší dobu (více jak poločas), přejdi na záložní papírové soupisky a dej o tom vědět organizátorům.</strong>
            </li>
            <li>
                Po každém zápase samozřejmě i nadále platí potvrzení výsledku na samostatný papírek a podpisy vedoucích jako jejich souhlas s výsledkem.
            </li>

            <li>
                V případě problémů či nesrovnalostí neváhej kontaktovat tvůrce P. Koláře (<a href="tel:420777951637">+420 777 951 637</a>, <a href="https://www.facebook.com/kolar.joe">FB Joe Kolář</a>) pohybujícího se volně po turnaji, nejčastěji u stolku na hale.
            </li>
        </ul>
    </b-container>
</template>

<script>
    import {mapActions, mapState} from 'vuex'

    export default {
        name: "category-list",
        computed: mapState(['categories']),
        methods: {
            setCategory(id) {
                this.$router.push({name: 'category', params: {category: id}});
            },
            ...mapActions(['loadCategories'])
        },
        created() {
            this.loadCategories()
        }
    }
</script>

<style scoped>
</style>