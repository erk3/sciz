<!-- TEMPLATE -->
<template>
	<v-container justify="center" align="center" class="fill-height pa-0 ma-0" id="share-view">
		<!-- SIDEBAR -->
		<v-navigation-drawer app clipped fixed>
			<v-app-bar flat class="pa-0 ma-0">
				<span>Mes calepins</span>
			</v-app-bar>
			<v-divider></v-divider>
			<v-subheader>Coterie personnelle</v-subheader>
			<v-list>
				<template v-for="(coterie, index) in [coterie_perso]">
					<v-list-item :key="index" @click="switchCoterie(coterie); refreshPad()" v-model="coterie_courante.id === coterie.id">
						<v-list-item-avatar>
							<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-list-item-avatar>
						<v-list-item-content>{{ coterie.nom }}</v-list-item-content>
					</v-list-item>
				</template>
			</v-list>
			<v-divider></v-divider>
			<v-subheader v-if="coteries.length > 0">Coterie(s) de groupe</v-subheader>
			<v-list>
				<template v-for="(coterie, index) in coteries">
					<v-list-item :key="index" @click="switchCoterie(coterie); refreshPad()" v-model="coterie_courante.id === coterie.id">
						<v-list-item-avatar>
							<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-list-item-avatar>
						<v-list-item-content>{{ coterie.nom }}</v-list-item-content>
					</v-list-item>
				</template>
			</v-list>
		</v-navigation-drawer>
		<!-- TIPTAP-->
		<v-col class="editor fill-height pa-0 ma-0">
			<!-- MENU BAR -->
			<v-app-bar flat> 
				<editor-menu-bar :editor="editor">
					<div class="menubar grow text-xs-center menububble" slot-scope="{ commands, isActive }">
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.bold() }" @click="commands.bold">
							<v-icon size="16px">fas fa-bold</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.italic() }" @click="commands.italic">
							<v-icon size="16px">fas fa-italic</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.strike() }" @click="commands.strike">
							<v-icon size="16px">fas fa-strikethrough</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.underline() }" @click="commands.underline">
							<v-icon size="16px">fas fa-underline</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.paragraph() }" @click="commands.paragraph">
							<v-icon size="16px">fas fa-paragraph</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.heading({ level: 1 }) }" @click="commands.heading({ level: 1 })">
							H1
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.heading({ level: 2 }) }" @click="commands.heading({ level: 2 })">
							H2
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.heading({ level: 3 }) }" @click="commands.heading({ level: 3 })">
							H3
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.bullet_list() }" @click="commands.bullet_list">
							<v-icon size="16px">fas fa-list</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.ordered_list() }" @click="commands.ordered_list">
							<v-icon size="16px">fas fa-list-ol</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.blockquote() }" @click="commands.blockquote">
							<v-icon size="16px">fas fa-quote-right</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.code() }" @click="commands.code">
							<v-icon size="16px">fas fa-code</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" :class="{ 'is-active': isActive.code_block() }" @click="commands.code_block">
							<v-icon size="16px">fas fa-file-code</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" @click="showImagePrompt(commands.image)">
							<v-icon size="16px">fas fa-image</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" @click="commands.undo">
							<v-icon size="16px">fas fa-undo</v-icon>
						</v-btn>
						<v-btn icon class="menubar__button" @click="commands.redo">
							<v-icon size="16px">fas fa-redo</v-icon>
						</v-btn>
					</div>
				</editor-menu-bar>
			</v-app-bar>
			<!-- EDITOR -->
			<editor-content class="editor__content pa-3 fill-height" :editor="editor"></editor-content>
		</v-col>
	</v-container>
</template>

<!-- SCRIPT -->
<script>
import Vue from 'vue'
import { setGroup, getGroup, getGroups } from '~/src/api.js'
import { Editor, EditorContent, EditorMenuBar, EditorMenuBubble } from 'tiptap'
import { Blockquote, CodeBlock, HardBreak, Heading, OrderedList, BulletList, ListItem, Bold, Code, Italic, Link, Strike, Underline, History, Placeholder, Image } from 'tiptap-extensions'

export default {
	name: 'PadView',
	components: {
		EditorContent,
		EditorMenuBar,
		EditorMenuBubble
	},
	data() {
		return {
			editor: new Editor({
				extensions: [
					new Blockquote(),
					new BulletList(),
					new CodeBlock(),
					new HardBreak(),
					new Heading({ levels: [1, 2, 3] }),
					new ListItem(),
					new OrderedList(),
					new Bold(),
					new Code(),
					new Italic(),
					new Link(),
					new Strike(),
					new Underline(),
					new History(),
					new Placeholder({emptyClass: 'is-empty',}),
					new Image()
				],
				onUpdate: this._.debounce(({ getJSON }) => {
					var new_json = getJSON();
					getGroup(this.coterie_courante.id, true)
						.then(res => {
							if (res.status === 200) {
								var remote_json = res.data['coterie'].webpad;
								if (this._.isEqual(this.old_json, remote_json)) {
									this.old_json = new_json;
									setGroup(this.coterie_courante.id, {'webpad': new_json});
								} else {
									this.old_json = remote_json;
									this.editor.setContent(remote_json);
								}
							}
						}
						); 	
				}, 1000),
				content: ''
			}),
			linkUrl: null,
			linkMenuIsActive: false,
			coterie_courante: {},
			coterie_perso: {},
			coteries: [],
			old_json: {}
		}
	},
	beforeMount() {
		getGroups(true, false, false)
			.then(res => {
				if (res.status === 200) {
					this.coterie_perso = res.data['coterie_perso'];
					this.coterie_courante = this.coterie_perso;
					this.coteries = res.data['coteries'];
					// Try to set the current coterie to the last one stored in local storage
					var lastCoterieID = this.$store.getters.coterieID;
					this.coteries.forEach(coterie => {
						if (coterie.id === lastCoterieID) {
							this.coterie_courante = coterie;
						}
					}); 
					// Update webpad
					this.old_json = this.coterie_courante.webpad;
					this.editor.setContent(this.coterie_courante.webpad);
					window.addEventListener('focus', this.refreshPad);
				}
			}
			);
	},
	beforeDestroy() {
		this.editor.destroy();
	},
	methods: {
		switchCoterie(coterie) {
			this.coterie_courante = coterie;
			this.$store.commit('setCoterieID', coterie.id);
			this.$store.commit('setCoterieName', coterie.nom);
		},
		showImagePrompt(command) {
			const src = prompt('URI de l\'image ?');
			if (src !== null) {
				command({ src });
			}
		},
		showLinkMenu(attrs) {
			this.linkUrl = attrs.href
			this.linkMenuIsActive = true
			this.$nextTick(() => {
				this.$refs.linkInput.focus()
			})
		},
		hideLinkMenu() {
			this.linkUrl = null
			this.linkMenuIsActive = false
		},
		setLinkUrl(command, url) {
			command({ href: url })
			this.hideLinkMenu()
			this.editor.focus()
		},
		refreshPad() {
			getGroup(this.coterie_courante.id, true)
				.then(res => {
					if (res.status === 200) {
						var remote_json = res.data['coterie'].webpad;
						this.old_json = remote_json;
						if (this.editor) {
							this.editor.setContent(remote_json);
						}
					}
				}
				); 
		}
	}
}
</script>

<!-- STYLE -->
<style lang="scss">
// The following is TipTap related
// For main editor
.ProseMirror {
	height: 100%;
}
.ProseMirror:focus {
	outline: 0;
}
// For placeholder (empty editor message)
.editor p.is-empty:first-child::after {
	content: "Vous pouvez commencez à écrire dans ce calepin ! \A\A Un calepin est lié à une côterie et permet de partager toutes sortes d'informations. \A\A Vous pouvez mettre en forme votre calepin à l'aide du menu ou utiliser des raccourcis Markdown classiques.\A(Taper '#' suivi d'un espace mettra par exemple en forme un titre principal)";
	white-space: pre;
	color: #aaa;
	pointer-events: none;
	font-style: italic;
}
// blockquote
.editor blockquote {
	margin: 20px 0;
	padding-left: 1.5rem;
	border-left: 5px solid rgba(189,189,189, 0.8);
}
</style>
