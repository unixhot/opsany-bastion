'use strict';

Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.RouteMenuProps = undefined;

var _extends2 = require('babel-runtime/helpers/extends');

var _extends3 = _interopRequireDefault(_extends2);

var _vueTypes = require('ant-design-vue/es/_util/vue-types');

var _vueTypes2 = _interopRequireDefault(_vueTypes);

var _antDesignVue = require('ant-design-vue');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var MenuItem = _antDesignVue.Menu.Item,
	SubMenu = _antDesignVue.Menu.SubMenu,
	ItemGroup = _antDesignVue.Menu.ItemGroup
var RouteMenuProps = exports.RouteMenuProps = {
	menus: _vueTypes2['default'].array,
	theme: _vueTypes2['default'].string.def('dark'),
	mode: _vueTypes2['default'].string.def('inline'),
	collapsed: _vueTypes2['default'].bool.def(false),
	i18nRender: _vueTypes2['default'].oneOfType([_vueTypes2['default'].func, _vueTypes2['default'].bool]).def(false)
};

var renderMenu = function renderMenu(h, item, i18nRender, collapsed) {
	if (item && !item.hidden) {
		var bool = item.children && !item.hideChildrenInMenu;
		return bool ? renderSubMenu(h, item, i18nRender) : renderMenuItem(h, item, i18nRender, collapsed);
	}
	return null;
};

var renderSubMenu = function renderSubMenu(h, item, i18nRender) {
	return h(
		SubMenu, {
		key: item.path,
		attrs: { title: h('span', [renderIcon(h, item.meta.icon), h('span', [renderTitle(h, item.meta.title, i18nRender)])]) }
	},
		[!item.hideChildrenInMenu && item.children.map(function (cd) {
			return renderMenu(h, cd, i18nRender);
		})]
	);
};

var renderMenuItem = (h, item, i18nRender, collapsed) => {
	var meta = (0, _extends3['default'])({}, item.meta);
	var target = meta.target || null;
	var CustomTag = target && 'a' || 'router-link';
	var props = { to: { name: item.name } };
	var attrs = { href: item.path, target: target };
	if (item.children && item.hideChildrenInMenu) {
		// 把有子菜单的 并且 父菜单是要隐藏子菜单的
		// 都给子菜单增加一个 hidden 属性
		// 用来给刷新页面时， selectedKeys 做控制用
		item.children.forEach(function (cd) {
			cd.meta = (0, _extends3['default'])(cd.meta, { hidden: true });
		});
	}
	if (item.name) {
		return h(
			MenuItem, { key: item.path, },
			[h(
				CustomTag, { props: props, attrs: attrs },
				[renderIcon(h, meta.icon), renderTitle(h, meta.title, i18nRender)]
			)]
		);
	} else {
		var collapsedTitle = meta.title.slice(0, 2)
		return h(
			ItemGroup, {
			props: {
				title: collapsed ? collapsedTitle : meta.title
			},
			style: {
				textAlign: collapsed ? 'center' : 'left'
			}
		},
		);
	}

};

var renderIcon = function renderIcon(h, icon) {
	if (icon === undefined || icon === 'none' || icon === null) {
		return null;
	}
	var props = {};
	typeof icon === 'object' ? props.component = icon : props.type = icon;
	return h(_antDesignVue.Icon, { props: props });
};

var renderTitle = function renderTitle(h, title, i18nRender) {
	return h('span', [i18nRender && i18nRender(title) || title]);
};

var RouteMenu = {
	name: 'RouteMenu',
	props: RouteMenuProps,
	data: function data() {
		return {
			openKeys: [],
			selectedKeys: [],
			cachedOpenKeys: []
		};
	},
	render: function render(h) {
		var _this = this;

		var mode = this.mode,
			theme = this.theme,
			menus = this.menus,
			i18nRender = this.i18nRender;

		var handleOpenChange = function handleOpenChange(openKeys) {
			// 在水平模式下时，不再执行后续
			if (mode === 'horizontal') {
				_this.openKeys = openKeys;
				return;
			}
			var latestOpenKey = openKeys.find(function (key) {
				return !_this.openKeys.includes(key);
			});
			if (!_this.rootSubmenuKeys.includes(latestOpenKey)) {
				_this.openKeys = openKeys;
			} else {
				_this.openKeys = latestOpenKey ? [latestOpenKey] : [];
			}
		};

		var dynamicProps = {
			props: {
				mode: mode,
				theme: theme,
				openKeys: this.openKeys,
				selectedKeys: this.selectedKeys
			},
			on: {
				select: function select(menu, e) {
					_this.selectedKeys = menu.selectedKeys;
					_this.$emit('select', menu);
				},
				openChange: handleOpenChange
			},
		};

		var menuItems = menus.map(function (item) {
			if (item.hidden) {
				return null;
			}
			return renderMenu(h, item, i18nRender, _this.collapsed);
		});
		return h(
			_antDesignVue.Menu,
			dynamicProps,
			[menuItems]
		);
	},

	methods: {
		updateMenu: function updateMenu() {
			var routes = this.$route.matched.concat();
			var hidden = this.$route.meta.hidden;

			if (routes.length >= 3 && hidden) {
				routes.pop();
				this.selectedKeys = [routes[routes.length - 1].path];
			} else {
				this.selectedKeys = [routes.pop().path];
			}
			var openKeys = [];
			if (this.mode === 'inline') {
				routes.forEach(function (item) {
					item.path && openKeys.push(item.path);
				});
			}

			this.collapsed ? this.cachedOpenKeys = openKeys : this.openKeys = openKeys;
		}
	},
	computed: {
		rootSubmenuKeys: function rootSubmenuKeys(vm) {
			var keys = [];
			vm.menus.forEach(function (item) {
				return keys.push(item.path);
			});
			return keys;
		}
	},
	created: function created() {
		var _this2 = this;

		this.$watch('$route', function () {
			_this2.updateMenu();
		});
		this.$watch('collapsed', function (val) {
			if (val) {
				_this2.cachedOpenKeys = _this2.openKeys.concat();
				_this2.openKeys = [];
			} else {
				_this2.openKeys = _this2.cachedOpenKeys;
			}
		});
	},
	mounted: function mounted() {
		this.updateMenu();
	}
};

exports['default'] = RouteMenu;