(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3b8391a7"],{"0e9d":function(t,e,a){},"1c48":function(t,e,a){},"2d26":function(t,e,a){"use strict";a.d(e,"d",(function(){return r})),a.d(e,"a",(function(){return i})),a.d(e,"c",(function(){return s})),a.d(e,"b",(function(){return l}));var n=a("b775"),o="command-strategy-v2/",r=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"get",params:t})},i=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"post",data:t})},s=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"put",data:t})},l=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"delete",data:t})}},"3a17":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("content-header",[a("div",{attrs:{slot:"docs"},slot:"docs"},[t._v(" 通过策略授权，将主机、用户和用户组、资源和凭证进行关联，设置用户允许和禁止支持哪些指令或指令集。 ")])]),a("a-card",[a("a-tabs",{model:{value:t.activeTab,callback:function(e){t.activeTab=e},expression:"activeTab"}},t._l(t.tabList,(function(e){return a("a-tab-pane",{key:e.key,attrs:{tab:e.name}},[e.key==t.activeTab?a(t.activeTab,{tag:"component"}):t._e()],1)})),1)],1)],1)},o=[],r=(a("ca00"),function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"top_search"},[a("div",[a("a-input-search",{staticStyle:{width:"300px"},attrs:{placeholder:"请输入关键字搜索",allowClear:""},on:{search:t.searchTable},model:{value:t.tableQuery.search_data,callback:function(e){t.$set(t.tableQuery,"search_data",e)},expression:"tableQuery.search_data"}},[a("a-select",{staticStyle:{width:"100px"},attrs:{slot:"addonBefore"},slot:"addonBefore",model:{value:t.tableQuery.search_type,callback:function(e){t.$set(t.tableQuery,"search_type",e)},expression:"tableQuery.search_type"}},t._l(t.searchList,(function(e){return a("a-select-option",{key:e.key},[t._v(t._s(e.name))])})),1)],1)],1),a("div",[a("a-button",{staticStyle:{"margin-right":"10px"},attrs:{icon:"reload"},on:{click:t.refresh}},[t._v("刷新")]),t.$store.state.btnAuth.btnAuth.bastion_command_strategy_create?a("a-button",{attrs:{icon:"plus",type:"primary"},on:{click:t.add}},[t._v("新建")]):t._e()],1)]),a("search-box",{staticClass:"search_box",attrs:{visible:t.visible}},[a("a-row",{attrs:{type:"flex",gutter:[36]}},[a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{staticStyle:{"text-align":"right"},attrs:{span:24}},[a("a-button",{on:{click:t.refresh}},[t._v("重置")]),a("a-button",{staticStyle:{"margin-left":"10px"},attrs:{type:"primary"},on:{click:t.searchTable}},[t._v("搜索")])],1)],1)],1),a("a-table",{attrs:{defaultExpandAllRows:!0,loading:t.tableLoading,dataSource:t.tableData,columns:t.columns,pagination:Object.assign({},t.tableQuery,{showSizeChanger:!0,showTotal:function(t){return"共 "+t+" 条数据"},showQuickJumper:!0}),rowKey:function(t){return t.id}},on:{change:t.tableChange},scopedSlots:t._u([{key:"name",fn:function(e,n){return[a("a",{attrs:{title:e,type:"link"},on:{click:function(e){return t.viewDetail(n)}}},[t._v(t._s(e))])]}},{key:"status",fn:function(e,n){return[t.$store.state.btnAuth.btnAuth.bastion_command_strategy_on_off?a("a-switch",{on:{click:function(e){return t.changeStatus(n)}},model:{value:n.status,callback:function(e){t.$set(n,"status",e)},expression:"row.status"}}):t._e(),t._v(" "+t._s(e?"开启":"关闭")+" ")]}},{key:"command",fn:function(e,a){return[t._v(" "+t._s(e.command.length)+"/"+t._s(e.command_group.length)+" ")]}},{key:"user",fn:function(e,a){return[t._v(" "+t._s(e.user.length)+"/"+t._s(e.user_group.length)+" ")]}},{key:"credential_host",fn:function(e,a){return[t._v(" "+t._s(e.password_credential_host_id.length)+"/"+t._s(e.ssh_credential_host_id.length)+"/"+t._s(e.credential_group.length)+" ")]}},{key:"action",fn:function(e,n){return[a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.viewDetail(n)}}},[t._v("查看")]),t.$store.state.btnAuth.btnAuth.bastion_command_strategy_update?a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.edit(n)}}},[t._v("编辑")]):t._e(),t.$store.state.btnAuth.btnAuth.bastion_command_strategy_delete?a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.del(n)}}},[t._v("删除")]):t._e()]}}])}),a("ControlPolicy",{ref:"ControlPolicy",on:{done:t.getTableData}})],1)}),i=[],s=(a("d3b7"),a("5530")),l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-drawer",{attrs:{title:t.id?"编辑命令策略":"新建命令策略",width:920,visible:t.visible,"body-style":{paddingBottom:"80px"}},on:{close:t.handleCancel}},[a("a-spin",{attrs:{spinning:t.infoLoading}},[a("div",{staticStyle:{"margin-bottom":"30px"}},[a("a-steps",{staticStyle:{width:"90%",margin:"0 auto"},attrs:{current:t.activeCurrent},on:{change:t.changeActiceCurrent}},[a("a-step",{attrs:{title:"配置基本信息"}}),a("a-step",{attrs:{title:"关联命令/命令组"}}),a("a-step",{attrs:{title:"关联用户/用户组"}}),a("a-step",{attrs:{title:"关联资源凭证"}})],1)],1),a("Step1",{directives:[{name:"show",rawName:"v-show",value:0==t.activeCurrent,expression:"activeCurrent == 0"}],ref:"Step1",attrs:{strategy:t.strategy}}),a("Step2",{directives:[{name:"show",rawName:"v-show",value:1==t.activeCurrent,expression:"activeCurrent == 1"}],ref:"Step2",attrs:{command:t.command}}),a("Step3",{directives:[{name:"show",rawName:"v-show",value:2==t.activeCurrent,expression:"activeCurrent == 2"}],ref:"Step3",attrs:{user:t.user}}),a("Step4",{directives:[{name:"show",rawName:"v-show",value:3==t.activeCurrent,expression:"activeCurrent == 3"}],ref:"Step4",attrs:{credential_host:t.credential_host}})],1),a("div",{staticClass:"bottom_btns"},[a("a-button",{style:{marginRight:"8px"},on:{click:t.handleCancel}},[t._v(" 取消 ")]),1==t.activeCurrent||2==t.activeCurrent||3==t.activeCurrent?a("a-button",{style:{marginRight:"8px"},on:{click:function(e){t.activeCurrent-=1}}},[t._v(" 上一步 ")]):t._e(),3==t.activeCurrent?a("a-button",{attrs:{type:"primary",loading:t.loading},on:{click:t.handleOk}},[t._v(" 确定 ")]):a("a-button",{attrs:{type:"primary"},on:{click:t.nextStep}},[t._v(" 下一步 ")])],1)],1)],1)},c=[],u=(a("4160"),a("cd3f")),d=a.n(u),m=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-form-model",{ref:"formData",attrs:{layout:"horizontal",model:t.formData,rules:t.formDataRules,"label-col":t.labelCol,"wrapper-col":t.wrapperCol}},[a("a-form-model-item",{attrs:{label:"策略名称",prop:"name"}},[a("a-input",{attrs:{placeholder:"请输入策略名称",disabled:!!t.formData.id},model:{value:t.formData.name,callback:function(e){t.$set(t.formData,"name",e)},expression:"formData.name"}})],1),a("a-form-model-item",{attrs:{label:"有效期"}},[a("a-date-picker",{attrs:{allowClear:"",showTime:"",placeholder:"请选择生效时间"},on:{change:function(e,a){return t.changeTime(e,a,"start_time")}},model:{value:t.start_time,callback:function(e){t.start_time=e},expression:"start_time"}}),a("a-date-picker",{staticStyle:{"margin-left":"20px"},attrs:{allowClear:"",showTime:"",placeholder:"请选择失效时间"},on:{change:function(e,a){return t.changeTime(e,a,"end_time")}},model:{value:t.end_time,callback:function(e){t.end_time=e},expression:"end_time"}})],1),a("a-form-model-item",{staticClass:"time_item",attrs:{label:"时段限制"}},[a("SelectTime",{ref:"SelectTime",attrs:{allowText:"允许使用命令",disabledText:"禁止使用命令"},model:{value:t.formData.login_time_limit,callback:function(e){t.$set(t.formData,"login_time_limit",e)},expression:"formData.login_time_limit"}})],1)],1)],1)},h=[],f=(a("a630"),a("3ca3"),a("cae8")),p={components:{SelectTime:f["a"]},props:{strategy:{type:Object,default:function(){return{}}}},watch:{strategy:{handler:function(t){for(var e in this.formData)e in t&&(this.formData[e]=t[e]);this.start_time=t.start_time||null,this.end_time=t.end_time||null}}},data:function(){return{formData:{id:void 0,name:void 0,start_time:void 0,end_time:void 0,login_time_limit:[]},formDataRules:{name:[{required:!0,message:"请填写策略名称",trigger:"change"}]},labelCol:{span:3},wrapperCol:{span:20},start_time:null,end_time:null}},methods:{changeTime:function(t,e,a){this.formData[a]=e},resetFormData:function(){var t=this;this.formData=this.$options.data().formData,this.$nextTick((function(){var e;null===(e=t.$refs.formData)||void 0===e||e.clearValidate()}));var e=Array.from({length:7},(function(t,e){return{week:e+1,time:[]}}));this.formData.login_time_limit=e,this.start_time=null,this.end_time=null}},mounted:function(){}},b=p,g=(a("97fb"),a("2877")),v=Object(g["a"])(b,m,h,!1,null,"7995cf27",null),_=v.exports,y=_,C=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-tabs",{ref:"tabs",model:{value:t.activeTab,callback:function(e){t.activeTab=e},expression:"activeTab"}},t._l(t.tabList,(function(t){return a("a-tab-pane",{key:t.key,attrs:{tab:t.name}})})),1),a("Command",{directives:[{name:"show",rawName:"v-show",value:"Command"==t.activeTab,expression:"activeTab == 'Command'"}],ref:"Command",attrs:{command_list:t.command_list}}),a("CommandGroup",{directives:[{name:"show",rawName:"v-show",value:"CommandGroup"==t.activeTab,expression:"activeTab == 'CommandGroup'"}],ref:"CommandGroup",attrs:{command_group_list:t.command_group_list}})],1)},k=[],x=(a("159b"),function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-transfer",{attrs:{dataSource:t.dataSource,targetKeys:t.targetKeys,selectedKeys:t.selectedKeys,showSearch:"",render:function(t){return t.title},"list-style":t.listStyle,operations:t.operations,titles:t.titles,lazy:!1},on:{change:t.handleChange,selectChange:t.handleSelectChange}})],1)}),D=[],w=(a("99af"),a("2909")),S=a("bb62"),$={props:{command_list:{type:Array,default:function(){return[]}},listStyle:{type:Object,default:function(){return{width:"370px",height:"420px"}}}},watch:{command_list:{handler:function(t){this.targetKeys=t},immediate:!0}},data:function(){return{dataSource:void 0,titles:["可选择的命令","已选择的命令"],operations:["加入右侧","加入左侧"],targetKeys:[],selectedKeys:[]}},methods:{getCommand:function(){var t=this,e={all_data:1};Object(S["getCommand"])(e).then((function(e){e.data.forEach((function(e){t.$set(e,"key",e.id+""),t.$set(e,"title",e.command)})),t.dataSource=e.data}))},handleChange:function(t){this.targetKeys=t},handleSelectChange:function(t,e){this.selectedKeys=[].concat(Object(w["a"])(t),Object(w["a"])(e))},resetData:function(){this.targetKeys=[],this.selectedKeys=[]},getFormData:function(){return this.targetKeys}},mounted:function(){this.getCommand()}},T=$,Q=Object(g["a"])(T,x,D,!1,null,"1bf5c963",null),O=Q.exports,j=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-transfer",{attrs:{dataSource:t.dataSource,targetKeys:t.targetKeys,selectedKeys:t.selectedKeys,showSearch:"",render:function(t){return t.title+"-"+t.description},"list-style":t.listStyle,operations:t.operations,titles:t.titles,lazy:!1},on:{change:t.handleChange,selectChange:t.handleSelectChange}})],1)},L=[],G=(a("a4d3"),a("e01a"),a("b0c0"),a("5c28")),A={props:{command_group_list:{type:Array,default:function(){return[]}},listStyle:{type:Object,default:function(){return{width:"370px",height:"420px"}}}},watch:{command_group_list:{handler:function(t){this.targetKeys=t},immediate:!0}},data:function(){return{dataSource:void 0,titles:["可选择的命令组","已选择的命令组"],operations:["加入右侧","加入左侧"],targetKeys:[],selectedKeys:[]}},methods:{getCommandGroup:function(){var t=this,e={all_data:1};Object(G["getCommandGroup"])(e).then((function(e){e.data.forEach((function(e){t.$set(e,"key",e.id+""),t.$set(e,"title",e.name),t.$set(e,"description",e.description||"--")})),t.dataSource=e.data}))},handleChange:function(t){this.targetKeys=t},handleSelectChange:function(t,e){this.selectedKeys=[].concat(Object(w["a"])(t),Object(w["a"])(e))},resetData:function(){this.targetKeys=[],this.selectedKeys=[]},getFormData:function(){return this.targetKeys}},mounted:function(){this.getCommandGroup()}},K=A,R=Object(g["a"])(K,j,L,!1,null,"f23b5076",null),z=R.exports,E={components:{Command:O,CommandGroup:z},props:{command:{type:Object,default:function(){return{}}}},watch:{command:{handler:function(t){var e=this;this.command_list=t.command||[],this.command_group_list=t.command_group||[],this.command_list.forEach((function(t,a){e.command_list[a]=t+""})),this.command_group_list.forEach((function(t,a){e.command_group_list[a]=t+""}))}}},data:function(){return{tabList:[{key:"Command",name:"关联命令"},{key:"CommandGroup",name:"关联命令组"}],activeTab:"Command",command_list:[],command_group_list:[]}},methods:{resetFormData:function(){var t=this;this.activeTab=this.$options.data().activeTab,this.tabList.forEach((function(e){var a;null===(a=t.$refs[e.key])||void 0===a||a.resetData()}))},getFormData:function(){var t=this.$refs.Command.getFormData(),e=this.$refs.CommandGroup.getFormData();return{command:t,command_group:e}}},mounted:function(){}},F=E,I=Object(g["a"])(F,C,k,!1,null,"9583e02c",null),M=I.exports,P=M,B=a("6421"),q=a("d816"),N=a("2d26"),J={components:{Step1:y,Step2:P,Step3:B["a"],Step4:q["a"]},data:function(){return{visible:!1,loading:!1,infoLoading:!1,activeCurrent:0,id:void 0,strategy:{},command:{},user:{},credential_host:{}}},methods:{showModal:function(t){var e=this;this.id=t,t&&this.getCommandStrategy();var a=["Step1","Step2","Step3","Step4"];this.activeCurrent=this.$options.data().activeCurrent,this.$nextTick((function(){setTimeout((function(){a.forEach((function(t){var a;null===(a=e.$refs[t])||void 0===a||a.resetFormData()}))}),0)})),this.visible=!0},getCommandStrategy:function(){var t=this;this.infoLoading=!0,Object(N["d"])({id:this.id}).then((function(e){var a=e.data,n=a.strategy,o=a.command,r=a.user,i=a.credential_host;t.user=r,t.command=o,t.strategy=n,t.credential_host=i})).finally((function(){t.infoLoading=!1}))},nextStep:function(){var t=this;if(0==this.activeCurrent){var e=this.$refs.Step1;e.$refs.formData.validate((function(e){e&&(t.activeCurrent+=1)}))}else this.activeCurrent+=1},handleOk:function(){var t=this,e=d()(this.$refs.Step1.formData),a=this.$refs.Step2.getFormData(),n=this.$refs.Step3.getFormData(),o=this.$refs.Step4.getFormData(),r={strategy:e,command:a,user:n,credential_host:o};this.loading=!0;var i={addCommandStrategy:N["a"],editCommandStrategy:N["c"]},s=e.id?"editCommandStrategy":"addCommandStrategy";i[s](r).then((function(e){t.$message.success(e.message),t.visible=!1,t.$emit("done")})).finally((function(){t.loading=!1}))},handleCancel:function(t){this.visible=!1},changeActiceCurrent:function(t){this.activeCurrent=t}}},V=J,H=(a("d00a"),Object(g["a"])(V,l,c,!1,null,"508e3336",null)),U=H.exports,W=a("3be4"),X={components:{ControlPolicy:U},data:function(){return{tableLoading:!1,visible:!1,tableQuery:{search_data:void 0,search_type:"name",current:1,pageSize:10,total:0,data_type:"list",status:void 0,call_type:void 0,execute_type:void 0},searchList:[{name:"策略名称",key:"name"}],tableData:[],columns:[{title:"策略名称",dataIndex:"name",ellipsis:!0,scopedSlots:{customRender:"name"}},{title:"状态",dataIndex:"status",ellipsis:!0,scopedSlots:{customRender:"status"}},{title:"关联命令",dataIndex:"command",ellipsis:!0,scopedSlots:{customRender:"command"}},{title:"关联用户",dataIndex:"user",ellipsis:!0,scopedSlots:{customRender:"user"}},{title:"关联资源凭证",dataIndex:"credential_host",ellipsis:!0,scopedSlots:{customRender:"credential_host"}},{title:"创建时间",dataIndex:"create_time",ellipsis:!0},{title:"操作",ellipsis:!0,scopedSlots:{customRender:"action"},align:"center"}]}},methods:{searchTable:function(){this.tableQuery.current=1,this.getTableData()},refresh:function(){this.tableQuery=this.$options.data().tableQuery,this.getTableData()},tableChange:function(t){var e=t.current,a=t.pageSize;this.tableQuery.current=e,this.tableQuery.pageSize=a,this.getTableData()},viewDetail:function(t){this.$router.push({name:"policyListInfo",query:{id:t.id}})},add:function(){this.$refs.ControlPolicy.showModal()},edit:function(t){this.$refs.ControlPolicy.showModal(t.id)},del:function(t){var e=this,a=t.id;this.$confirm({title:"删除确认",content:"请确认是否删除?",okType:"danger",onOk:function(){return Object(N["b"])({id:a}).then((function(t){e.$message.success("删除成功"),e.getTableData()}))}})},changeStatus:function(t){var e=this,a={id:t.id,status:t.status,type:"command"};Object(W["d"])(a).then((function(t){e.getTableData()}))},getTableData:function(){var t=this;this.tableLoading=!0,Object(N["d"])(Object(s["a"])({},this.tableQuery)).then((function(e){var a=e.data,n=a.data,o=a.current,r=a.total;t.tableData=n,t.tableQuery.current=o,t.tableQuery.total=r,t.tableQuery.total>0&&t.tableQuery.current>1&&0==t.tableData.length&&(t.tableQuery.current--,t.getTableData())})).finally((function(){t.tableLoading=!1}))}},mounted:function(){this.getTableData()}},Y=X,Z=(a("7029"),Object(g["a"])(Y,r,i,!1,null,"8aac43c2",null)),tt=Z.exports,et=tt,at=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"top_search"},[a("div",[a("a-input-search",{staticStyle:{width:"300px"},attrs:{placeholder:"请输入关键字搜索",allowClear:""},on:{search:t.searchTable},model:{value:t.tableQuery.search_data,callback:function(e){t.$set(t.tableQuery,"search_data",e)},expression:"tableQuery.search_data"}},[a("a-select",{staticStyle:{width:"100px"},attrs:{slot:"addonBefore"},slot:"addonBefore",model:{value:t.tableQuery.search_type,callback:function(e){t.$set(t.tableQuery,"search_type",e)},expression:"tableQuery.search_type"}},t._l(t.searchList,(function(e){return a("a-select-option",{key:e.key},[t._v(t._s(e.name))])})),1)],1)],1),a("div",[a("a-button",{staticStyle:{"margin-right":"10px"},attrs:{icon:"reload"},on:{click:t.refresh}},[t._v("刷新")]),t.$store.state.btnAuth.btnAuth.bastion_command_create?a("a-button",{attrs:{icon:"plus",type:"primary"},on:{click:t.add}},[t._v("新建")]):t._e()],1)]),a("search-box",{staticClass:"search_box",attrs:{visible:t.visible}},[a("a-row",{attrs:{type:"flex",gutter:[36]}},[a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{staticStyle:{"text-align":"right"},attrs:{span:24}},[a("a-button",{on:{click:t.refresh}},[t._v("重置")]),a("a-button",{staticStyle:{"margin-left":"10px"},attrs:{type:"primary"},on:{click:t.searchTable}},[t._v("搜索")])],1)],1)],1),a("a-table",{attrs:{defaultExpandAllRows:!0,loading:t.tableLoading,dataSource:t.tableData,columns:t.columns,pagination:Object.assign({},t.tableQuery,{showSizeChanger:!0,showTotal:function(t){return"共 "+t+" 条数据"},showQuickJumper:!0}),rowKey:function(t){return t.id}},on:{change:t.tableChange},scopedSlots:t._u([{key:"name",fn:function(e,n){return[a("a",{attrs:{type:"link"},on:{click:function(e){return t.viewDetail(n)}}},[t._v(t._s(e))])]}},{key:"user",fn:function(e,a){return[t._v(" "+t._s(e.user.length)+"/"+t._s(e.user_group.length)+" ")]}},{key:"credential",fn:function(e,a){return[t._v(" "+t._s(e.password_credential.length)+"/"+t._s(e.ssh_credential.length)+"/"+t._s(e.credential_group.length)+" ")]}},{key:"action",fn:function(e,n){return[t.$store.state.btnAuth.btnAuth.bastion_command_update?a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.edit(n)}}},[t._v("编辑")]):t._e(),t.$store.state.btnAuth.btnAuth.bastion_command_delete?a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.del(n)}}},[t._v("删除")]):t._e()]}}])}),a("ControlCommand",{ref:"ControlCommand",on:{done:t.getTableData}})],1)},nt=[],ot=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-modal",{attrs:{title:t.formData.id?"编辑命令":"新建命令",confirmLoading:t.loading,width:"920px"},on:{ok:t.handleOk,cancel:t.handleCancel},model:{value:t.visible,callback:function(e){t.visible=e},expression:"visible"}},[a("a-form-model",{ref:"formData",attrs:{model:t.formData,rules:t.formDataRules,labelCol:{span:3},wrapperCol:{span:21}}},[a("a-form-model-item",{attrs:{label:"命令名称",prop:"command"}},[a("a-input",{attrs:{placeholder:"请输入命令名称"},model:{value:t.formData.command,callback:function(e){t.$set(t.formData,"command",e)},expression:"formData.command"}})],1),a("a-form-model-item",{attrs:{label:"命令类型",prop:"block_type"}},[a("a-select",{attrs:{placeholder:"请选择命令类型"},model:{value:t.formData.block_type,callback:function(e){t.$set(t.formData,"block_type",e)},expression:"formData.block_type"}},t._l(t.block_type_list,(function(e){return a("a-select-option",{key:e.key,attrs:{value:e.key}},[t._v(" "+t._s(e.name)+" ")])})),1)],1),a("a-form-model-item",{attrs:{label:"提示内容",prop:"block_info"}},[a("a-input",{attrs:{type:"textarea",placeholder:"请输入提示内容",autoSize:{minRows:3,maxRows:6}},model:{value:t.formData.block_info,callback:function(e){t.$set(t.formData,"block_info",e)},expression:"formData.block_info"}})],1),a("a-form-model-item",{attrs:{label:"命令组"}},[a("CommandGroup",{ref:"CommandGroup",attrs:{listStyle:{width:"300px",height:"400px"},command_group_list:t.formData.command_group_list}})],1)],1)],1)],1)},rt=[],it=(a("d81d"),a("b64b"),{components:{CommandGroup:z},data:function(){return{visible:!1,loading:!1,formData:{id:void 0,command:void 0,block_type:void 0,block_info:void 0,command_group_list:[]},formDataRules:{command:[{required:!0,message:"请填写命令名称",trigger:"change"}],block_type:[{required:!0,message:"请选择命令类型",trigger:"change"}],block_info:[{required:!0,message:"请填写提示内容",trigger:"change"}]},block_type_list:[{key:"1",name:"命令阻断"},{key:"2",name:"命令提醒"}]}},methods:{showModal:function(){var t,e=this,a=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};if(this.formData=this.$options.data().formData,null===(t=this.$refs.CommandGroup)||void 0===t||t.resetData(),this.$nextTick((function(){var t;null===(t=e.$refs.formData)||void 0===t||t.clearValidate()})),Object.keys(a).length){for(var n in this.formData)n in a&&(this.formData[n]=a[n]);var o=a.command_group||[];this.formData.command_group_list=o.map((function(t){return t.id+""}))}this.visible=!0},handleOk:function(){var t=this,e=this.formData.id?"editCommand":"addCommand";this.formData.command_group_list=this.$refs.CommandGroup.getFormData(),this.loading=!0,S[e](this.formData).then((function(e){t.$message.success(e.message),t.visible=!1,t.$emit("done")})).finally((function(){t.loading=!1}))},handleCancel:function(){this.visible=!1}},mounted:function(){}}),st=it,lt=Object(g["a"])(st,ot,rt,!1,null,"cbe3a6aa",null),ct=lt.exports,ut={components:{ControlCommand:ct},data:function(){return{tableLoading:!1,visible:!1,tableQuery:{search_data:void 0,search_type:"command",total:0,current:1,pageSize:10},searchList:[{name:"命令名称",key:"command"}],tableData:[],columns:[{title:"命令名称",dataIndex:"command",ellipsis:!0},{title:"命令类型",dataIndex:"block_type",ellipsis:!0,customRender:function(t){return 1==t?"命令阻断":"命令提醒"}},{title:"提示内容",dataIndex:"block_info",ellipsis:!0},{title:"操作",ellipsis:!0,scopedSlots:{customRender:"action"},align:"center"}]}},methods:{searchTable:function(){this.tableQuery.current=1,this.getTableData()},refresh:function(){this.tableQuery=this.$options.data().tableQuery,this.getTableData()},tableChange:function(t){var e=t.current,a=t.pageSize;this.tableQuery.current=e,this.tableQuery.pageSize=a,this.getTableData()},viewDetail:function(t){},add:function(){this.$refs.ControlCommand.showModal()},edit:function(t){this.$refs.ControlCommand.showModal(t)},del:function(t){var e=this,a=t.id;this.$confirm({title:"删除确认",content:"请确认是否删除?",okType:"danger",onOk:function(){return Object(S["delCommand"])({id:a}).then((function(t){e.$message.success("删除成功"),e.getTableData()}))}})},getTableData:function(){var t=this;this.tableLoading=!0,Object(S["getCommand"])(Object(s["a"])({},this.tableQuery)).then((function(e){var a=e.data,n=a.data,o=a.current,r=a.total;t.tableData=n,t.tableQuery.current=o,t.tableQuery.total=r,t.tableQuery.total>0&&t.tableQuery.current>1&&0==t.tableData.length&&(t.tableQuery.current--,t.getTableData())})).finally((function(){t.tableLoading=!1}))}},mounted:function(){this.getTableData()}},dt=ut,mt=(a("e42d"),Object(g["a"])(dt,at,nt,!1,null,"209f6a1c",null)),ht=mt.exports,ft=ht,pt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"top_search"},[a("div",[a("a-input-search",{staticStyle:{width:"300px"},attrs:{placeholder:"请输入关键字搜索",allowClear:""},on:{search:t.searchTable},model:{value:t.tableQuery.search_data,callback:function(e){t.$set(t.tableQuery,"search_data",e)},expression:"tableQuery.search_data"}},[a("a-select",{staticStyle:{width:"120px"},attrs:{slot:"addonBefore"},slot:"addonBefore",model:{value:t.tableQuery.search_type,callback:function(e){t.$set(t.tableQuery,"search_type",e)},expression:"tableQuery.search_type"}},t._l(t.searchList,(function(e){return a("a-select-option",{key:e.key},[t._v(t._s(e.name))])})),1)],1)],1),a("div",[a("a-button",{staticStyle:{"margin-right":"10px"},attrs:{icon:"reload"},on:{click:t.refresh}},[t._v("刷新")]),t.$store.state.btnAuth.btnAuth.bastion_command_group_create?a("a-button",{attrs:{icon:"plus",type:"primary"},on:{click:t.add}},[t._v("新建")]):t._e()],1)]),a("search-box",{staticClass:"search_box",attrs:{visible:t.visible}},[a("a-row",{attrs:{type:"flex",gutter:[36]}},[a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{attrs:{xxl:8,xl:12,lg:12,md:24,sm:24,xs:24}}),a("a-col",{staticStyle:{"text-align":"right"},attrs:{span:24}},[a("a-button",{on:{click:t.refresh}},[t._v("重置")]),a("a-button",{staticStyle:{"margin-left":"10px"},attrs:{type:"primary"},on:{click:t.searchTable}},[t._v("搜索")])],1)],1)],1),a("a-table",{attrs:{defaultExpandAllRows:!0,loading:t.tableLoading,dataSource:t.tableData,columns:t.columns,pagination:Object.assign({},t.tableQuery,{showSizeChanger:!0,showTotal:function(t){return"共 "+t+" 条数据"},showQuickJumper:!0}),rowKey:function(t){return t.id}},on:{change:t.tableChange},scopedSlots:t._u([{key:"name",fn:function(e,a){return[t._v(" "+t._s(e)+" ")]}},{key:"user",fn:function(e,a){return[t._v(" "+t._s(e.user.length)+"/"+t._s(e.user_group.length)+" ")]}},{key:"credential",fn:function(e,a){return[t._v(" "+t._s(e.password_credential.length)+"/"+t._s(e.ssh_credential.length)+"/"+t._s(e.credential_group.length)+" ")]}},{key:"action",fn:function(e,n){return[t.$store.state.btnAuth.btnAuth.bastion_command_group_update?a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.edit(n)}}},[t._v("编辑")]):t._e(),t.$store.state.btnAuth.btnAuth.bastion_command_group_delete?a("a-button",{attrs:{type:"link",size:"small"},on:{click:function(e){return t.del(n)}}},[t._v("删除")]):t._e()]}}])}),a("ControlCommandGroup",{ref:"ControlCommandGroup",on:{done:t.getTableData}})],1)},bt=[],gt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("a-modal",{attrs:{title:t.formData.id?"编辑命令组":"新建命令组",confirmLoading:t.loading,width:"920px"},on:{ok:t.handleOk,cancel:t.handleCancel},model:{value:t.visible,callback:function(e){t.visible=e},expression:"visible"}},[a("a-form-model",{ref:"formData",attrs:{model:t.formData,rules:t.formDataRules,labelCol:{span:3},wrapperCol:{span:21}}},[a("a-form-model-item",{attrs:{label:"命令组名称",prop:"name"}},[a("a-input",{attrs:{placeholder:"请输入命令组名称"},model:{value:t.formData.name,callback:function(e){t.$set(t.formData,"name",e)},expression:"formData.name"}})],1),a("a-form-model-item",{attrs:{label:"描述"}},[a("a-input",{attrs:{type:"textarea",placeholder:"请输入描述",autoSize:{minRows:3,maxRows:6}},model:{value:t.formData.description,callback:function(e){t.$set(t.formData,"description",e)},expression:"formData.description"}})],1),a("a-form-model-item",{attrs:{label:"命令"}},[a("Command",{ref:"Command",attrs:{listStyle:{width:"300px",height:"400px"},command_list:t.formData.command_list}})],1)],1)],1)],1)},vt=[],_t={components:{Command:O},data:function(){return{visible:!1,loading:!1,formData:{id:void 0,name:void 0,description:void 0,command_list:[]},formDataRules:{name:[{required:!0,message:"请填写命令名称",trigger:"change"}]}}},methods:{showModal:function(){var t,e=this,a=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};if(this.formData=this.$options.data().formData,null===(t=this.$refs.Command)||void 0===t||t.resetData(),this.$nextTick((function(){var t;null===(t=e.$refs.formData)||void 0===t||t.clearValidate()})),Object.keys(a).length){for(var n in this.formData)n in a&&(this.formData[n]=a[n]);var o=a.command||[];this.formData.command_list=o.map((function(t){return t.id+""}))}this.visible=!0},handleOk:function(){var t=this,e=this.formData.id?"editCommandGroup":"addCommandGroup";this.formData.command_list=this.$refs.Command.getFormData(),this.loading=!0,G[e](this.formData).then((function(e){t.$message.success(e.message),t.visible=!1,t.$emit("done")})).finally((function(){t.loading=!1}))},handleCancel:function(){this.visible=!1}},mounted:function(){}},yt=_t,Ct=Object(g["a"])(yt,gt,vt,!1,null,"972fbe44",null),kt=Ct.exports,xt={components:{ControlCommandGroup:kt},data:function(){return{tableLoading:!1,visible:!1,tableQuery:{search_data:void 0,search_type:"name",current:1,pageSize:10,total:0},searchList:[{name:"命令组名称",key:"name"}],tableData:[],columns:[{title:"命令组名称",dataIndex:"name",ellipsis:!0},{title:"描述",dataIndex:"description",ellipsis:!0,customRender:function(t){return t||"--"}},{title:"创建时间",dataIndex:"create_time",ellipsis:!0},{title:"操作",ellipsis:!0,scopedSlots:{customRender:"action"},align:"center"}]}},methods:{searchTable:function(){this.tableQuery.current=1,this.getTableData()},refresh:function(){this.tableQuery=this.$options.data().tableQuery,this.getTableData()},tableChange:function(t){var e=t.current,a=t.pageSize;this.tableQuery.current=e,this.tableQuery.pageSize=a,this.getTableData()},viewDetail:function(t){},add:function(){this.$refs.ControlCommandGroup.showModal()},edit:function(t){this.$refs.ControlCommandGroup.showModal(t)},del:function(t){var e=this,a=t.id;this.$confirm({title:"删除确认",content:"请确认是否删除?",okType:"danger",onOk:function(){return Object(G["delCommandGroup"])({id:a}).then((function(t){e.$message.success("删除成功"),e.getTableData()}))}})},getTableData:function(){var t=this;this.tableLoading=!0,Object(G["getCommandGroup"])(Object(s["a"])({},this.tableQuery)).then((function(e){var a=e.data,n=a.data,o=a.current,r=a.total;t.tableData=n,t.tableQuery.current=o,t.tableQuery.total=r,t.tableQuery.total>0&&t.tableQuery.current>1&&0==t.tableData.length&&(t.tableQuery.current--,t.getTableData())})).finally((function(){t.tableLoading=!1}))}},mounted:function(){this.getTableData()}},Dt=xt,wt=(a("583a"),Object(g["a"])(Dt,pt,bt,!1,null,"7e7be35a",null)),St=wt.exports,$t=St,Tt={components:{PolicyList:et,CommandList:ft,CommandGroup:$t},data:function(){return{tabList:[{key:"PolicyList",name:"策略列表"},{key:"CommandList",name:"命令列表"},{key:"CommandGroup",name:"命令组"}],activeTab:"PolicyList"}},methods:{},mounted:function(){}},Qt=Tt,Ot=Object(g["a"])(Qt,n,o,!1,null,"3dc25494",null),jt=Ot.exports;e["default"]=jt},4031:function(t,e,a){},"583a":function(t,e,a){"use strict";var n=a("8d5f"),o=a.n(n);o.a},"5c28":function(t,e,a){"use strict";a.r(e),a.d(e,"getCommandGroup",(function(){return r})),a.d(e,"addCommandGroup",(function(){return i})),a.d(e,"editCommandGroup",(function(){return s})),a.d(e,"delCommandGroup",(function(){return l}));var n=a("b775"),o="command-group/",r=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"get",params:t})},i=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"post",data:t})},s=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"put",data:t})},l=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"delete",data:t})}},7029:function(t,e,a){"use strict";var n=a("1c48"),o=a.n(n);o.a},"8d5f":function(t,e,a){},"97fb":function(t,e,a){"use strict";var n=a("0e9d"),o=a.n(n);o.a},bb62:function(t,e,a){"use strict";a.r(e),a.d(e,"getCommand",(function(){return r})),a.d(e,"addCommand",(function(){return i})),a.d(e,"editCommand",(function(){return s})),a.d(e,"delCommand",(function(){return l}));var n=a("b775"),o="command/",r=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"get",params:t})},i=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"post",data:t})},s=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"put",data:t})},l=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(n["b"])({url:o,method:"delete",data:t})}},d00a:function(t,e,a){"use strict";var n=a("4031"),o=a.n(n);o.a},e42d:function(t,e,a){"use strict";var n=a("feec"),o=a.n(n);o.a},feec:function(t,e,a){}}]);