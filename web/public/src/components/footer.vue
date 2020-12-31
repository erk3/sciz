<!-- TEMPLATE -->
<template>
	<v-footer app fixed>
		<!-- FOOTER -->
		<v-row>
			<v-col wrap>
				<v-btn v-for="link in links" :key="link.img" :href="link.href" class="ma-0" icon target="_blank">
					<v-img :src="Image(link.img)" alt="" contain max-width="25px" max-height="20px"></v-img>
				</v-btn>
    		</v-col>
			<v-col>
				<v-layout fill-height align-center justify-center caption>
					2019-2021 © SCIZ
				</v-layout>
			</v-col>
			<v-col>
				<v-layout fill-height align-center justify-end caption>
					<p class="mb-0">From Põm³ with love <v-icon size="14px">fas fa-heart</v-icon></p>
				</v-layout>
			</v-col>
		</v-row>
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
				{ img: 'logo-github', href: 'https://github.com/erk3/sciz' }
			]
		}),
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