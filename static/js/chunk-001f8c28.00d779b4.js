(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-001f8c28"],{14661:function(t,a,e){},"8e49":function(t,a,e){"use strict";e.r(a);var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"auditHistory_main"},[e("ContentHeader",[e("div",{attrs:{slot:"docs"},slot:"docs"},[t._v(" 记录所有危险命令的执行情况，用于进行规范化管理和快速查询。 ")])]),e("a-card",[e("div",{staticClass:"search_box"},[e("a-input-search",{staticStyle:{width:"300px"},attrs:{placeholder:"请输入关键字搜索",allowClear:""},on:{search:t.searchTable},model:{value:t.pagination.search_data,callback:function(a){t.$set(t.pagination,"search_data",a)},expression:"pagination.search_data"}},[e("a-select",{staticStyle:{width:"100px"},attrs:{slot:"addonBefore"},slot:"addonBefore",model:{value:t.pagination.search_type,callback:function(a){t.$set(t.pagination,"search_type",a)},expression:"pagination.search_type"}},t._l(t.searchList,(function(a){return e("a-select-option",{key:a.key},[t._v(t._s(a.name))])})),1)],1),e("a-button",{staticStyle:{float:"right"},attrs:{icon:"reload"},on:{click:t.refresh}},[t._v("刷新")])],1),e("a-table",{attrs:{loading:t.tableLoading,pagination:t.pagination,columns:t.columns,"data-source":t.tableData},on:{change:t.onChange},scopedSlots:t._u([{key:"status",fn:function(a){return[e("a-tag",{attrs:{color:"y"==a?"green":"pink"}},[t._v(" "+t._s("y"==a?"已执行":"未执行")+" ")])]}},{key:"block_type",fn:function(a){return[t._v(" "+t._s("confirm"==a?"指令提醒":"指令阻断")+" ")]}}])})],1)],1)},i=[],o=(e("d81d"),e("d3b7"),e("0977")),s=e("b899"),r={data:function(){return{tableData:[],pagination:{total:0,current:1,pageSize:10,showTotal:function(t){return"共有 ".concat(t," 条数据")},search_type:"user",search_data:void 0,showSizeChanger:!0,showQuickJumper:!0},tableLoading:!1,columns:[{title:"操作用户/执行用户",dataIndex:"user",ellipsis:!0},{title:"执行主机",dataIndex:"hostname",ellipsis:!0},{title:"执行状态",dataIndex:"status",ellipsis:!0,scopedSlots:{customRender:"status"}},{title:"指令类型",dataIndex:"block_type",ellipsis:!0,scopedSlots:{customRender:"block_type"}},{title:"执行时间",dataIndex:"create_time",ellipsis:!0},{title:"指令名称",dataIndex:"intercept_command",ellipsis:!0},{title:"命令内容",dataIndex:"command",ellipsis:!0}],searchList:[{name:"登录用户",key:"user"}],blockTypeList:[{value:"confirm",label:"指令提醒"},{value:"cancle",label:"指令阻断"}]}},mounted:function(){this.getCommandHistoryData()},methods:{onChange:function(t){this.pagination.total=t.total,this.pagination.current=t.current,this.pagination.pageSize=t.pageSize,this.getCommandHistoryData()},searchTable:function(t){this.search_data=t,this.pagination.current=1,this.getCommandHistoryData()},refresh:function(){this.getSessionLogData()},getCommandHistoryData:function(){var t=this;this.tableLoading=!0;var a={current:this.pagination.current,pageSize:this.pagination.pageSize};this.pagination.search_data&&("server"==this.pagination.search_type?a.search_type="host__host_name":a.search_type=this.pagination.search_type,a.search_data=this.pagination.search_data),Object(s["c"])(a).then((function(a){200==a.code&&a.data?(t.pagination.total=a.data.total,t.pagination.current=a.data.current,t.pagination.pageSize=a.data.pageSize,a.data.data.map((function(t){t.key=t.id})),t.tableData=a.data.data):t.tableData=[]})).finally((function(){t.tableLoading=!1}))}},components:{ContentHeader:o["a"]}},c=r,l=(e("cd2e"),e("2877")),d=Object(l["a"])(c,n,i,!1,null,"46bb9680",null);a["default"]=d.exports},b899:function(t,a,e){"use strict";e.d(a,"f",(function(){return i})),e.d(a,"b",(function(){return o})),e.d(a,"a",(function(){return s})),e.d(a,"g",(function(){return r})),e.d(a,"c",(function(){return c})),e.d(a,"d",(function(){return l})),e.d(a,"e",(function(){return d}));var n=e("b775"),i=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:"session-log/",method:"get",params:t})},o=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:"session-log/",method:"delete",data:t})},s=window.location.origin+window.API_ROOT+"api/bastion/v0_1/",r=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"";return s+"session-log/guacamole/"+"".concat(t,"/")},c=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:"command-log/",method:"get",params:t})},l=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:"operation-log/",method:"get",params:t})},d=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:"session-command-history/",method:"get",params:t})}},cd2e:function(t,a,e){"use strict";var n=e("14661"),i=e.n(n);i.a}}]);