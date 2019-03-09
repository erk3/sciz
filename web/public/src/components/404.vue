<!-- TEMPLATE -->
<template>
	<v-layout justify-center align-center fill-height id="404-view">
		<v-flex xs6 text-xs-center>
      <v-card flat tile class="transparent">
        <v-img :src="Image('confused')" contain max-height="300px"></v-img>
				<h1 class="display-2 text-uppercase"> Oups ! </h1><br/>
				<h2 class="title"> Cette page est introuvable. </h2><br/>
				<h6 class="subheading"> Erreur 404 </h6>
      </v-card>
    </v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	export default {
    name: 'PageNotFoundView'
  }
</script>
