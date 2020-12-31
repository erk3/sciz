<!-- TEMPLATE -->
<template>
	<v-row justify="center" align="center" class="fill-height" id="404-view">
		<v-col class="col-6">
      		<v-card-text tile class="transparent text-center">
        		<v-img :src="Image('confused')" contain max-height="300px"></v-img>
				<h1 class="display-2 text-uppercase"> Oups!</h1><br/>
				<h2 class="title">Cette page est introuvable.</h2><br/>
				<h6 class="subheading">Erreur 404</h6>
      		</v-card-text>
		</v-col>
	</v-row>
</template>

<!-- SCRIPT -->
<script>
	export default {
    	name: 'PageNotFoundView'
	}
</script>
