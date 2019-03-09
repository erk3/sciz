<!-- TEMPLATE -->
<template>
	<!-- FOOTER -->
	<v-footer app fixed>
		<v-container fluid pa-0>
    	<v-layout v-bind="binding" wrap mr-5 ml-5>
				<v-flex text-xs-left pl-5>
					<v-btn v-for="link in links" :key="link.icon" v-bind:href="link.href" v-bind:class="{'ma-0': true}" icon target="_blank">
						<v-img :src="Image(link.img)" alt="" contain max-height="20px"></v-img>
					</v-btn>
    		</v-flex>
				<v-flex text-xs-center align-center>
					<v-layout fill-height align-center justify-center caption>
						2019 © SCIZ
					</v-layout>
				</v-flex>
				<v-flex text-xs-right pr-5>
					<v-layout fill-height align-center justify-end caption>
						<p class="mb-0">From Põm³ with love <v-icon size="14px">fas fa-heart</v-icon></p>
					</v-layout>
				</v-flex>
			</v-layout>
  	</v-container>
		<!-- BACK TO TOP -->
		<v-btn v-scroll="onScroll" v-show="displayScrollToTop" fab fixed bottom right @click="toTop">	
			<v-icon size="16px">fas fa-arrow-up</v-icon>
		</v-btn>
	</v-footer>
</template>

<!-- SCRIPT -->
<script>
  export default {
    name: 'FooterView',
		data: () => ({
      displayScrollToTop: false,
			links: [
				{ img: 'logo-104126', href: 'http://games.mountyhall.com/mountyhall/View/PJView.php?ai_IDPJ=104126'},
				{ img: 'logo-mh', href: 'http://www.mountyhall.com/Forum/display_topic_threads.php?ForumID=21&TopicID=173262' },
				{ img: 'logo-miaou', href: 'https://miaou.dystroy.org/2603?SCIZ' },
				{ img: 'logo-github', href: 'https://github.com/erk3/sciz' },
				{ img: 'logo-spreadshirt', href: 'https://shop.spreadshirt.fr/sciz'},
			]
		}),
		computed: {
      binding () {
        const binding = {}
        if (this.$vuetify.breakpoint.xs) binding.column = true
        return binding
      }
    },
		methods: {
	    onScroll(e) {
	      if (typeof window === 'undefined') return;
	      const top = window.pageYOffset || e.target.scrollTop || 0;
	      this.displayScrollToTop = top > 20;
	    },
	    toTop () {
	      this.$vuetify.goTo(0);
    	}
  	}
	}
</script>

<!-- STYLE -->
<style scoped>
a {
  text-decoration: none;
}
</style>
