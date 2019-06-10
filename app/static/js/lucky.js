/*
 * for string format
*/
String.prototype.lym_format = function() {
    if (arguments.length == 0) {
        return this;
    }
    for (var StringFormat_s = this, StringFormat_i = 0; StringFormat_i < arguments.length; StringFormat_i++) {
        StringFormat_s = StringFormat_s.replace(new RegExp("\\{" + StringFormat_i + "\\}", "g"), arguments[StringFormat_i]);
    }
    return StringFormat_s;
}

function addTab(title, url, icon){
    var editor_tabs = $("#editor_tabs");
    if (editor_tabs.tabs('exists', title)){
        //如果tab已经存在,则选中并刷新该tab
        editor_tabs.tabs('select', title);
        refreshTab({title: title, url: url});
    }
    else {
        var content='<iframe scrolling="yes" frameborder="0"  src="{0}" style="width:100%;height:700px;"></iframe>'.lym_format(url);
        editor_tabs.tabs('add',{
            title: title,
            closable: true,
            content: content,
            iconCls: icon||'icon-default'
        });
    }
}

function refreshTab(cfg){
    var tab = cfg.title?$('#editor_tabs').tabs('getTab',cfg.title):$('#editor_tabs').tabs('getSelected');
    if(tab && tab.find('iframe').length > 0){
        var frame = tab.find('iframe')[0];
        var url = cfg.url?cfg.url:fram.src;
        frame.contentWindow.location.href = url;
    }
}

/*左边操作树*/

function init_project_list(){
    $.ajax({
        type : 'POST',
        url : '/api/v1/project/',
        ContentType:'text/html',
        data:  {
               "method": "query",
               "id": "-2"
            },
        success : function(data, textStatus, request) {
            $('select#project_list').combobox("loadData", data["rows"]);
            }
    });

    $('select#project_list').combobox({
	onSelect: function(record){
	    load_project_tree(record["id"]);
	    var tabs = $("#editor_tabs").tabs('tabs');
	    var titles = new Array("欢迎页", "产品管理", "项目管理", "调度管理", "用户管理", "关键字");
	    for(var index=0;index<tabs.length; index++){
	        var title = $("#editor_tabs").tabs('getTab', index).panel('options').title;
	        var flag = false;
	        for(var t in titles){
	            if(titles[t] == title) {
	                flag=true;
	            }
	        }
	        if(!flag){
	            $("#editor_tabs").tabs('close', title);
	        }
	    }
	}
});
}

function refresh_project_tree(){
    var root = $('#project_tree').tree("getRoot");
    load_project_tree(root.id);
}

function load_project_tree(id){
   $.ajax({
        type : 'get',
        url : '/api/v1/project/',
        data:  {
               "id": id
            },
        success : function(data, textStatus, request) {
            $('#project_tree').tree("loadData", data);
            }
    });
}

function open_win(id){
    $('#{0}'.lym_format(id)).window('open');
}

function close_win(id){
    $('#{0}'.lym_format(id)).window('close');
}

function show_msg(title, msg){
    $.messager.show({
        title: title,
        msg: msg,
        timeout: 3000,
        showType: 'slide'
    });
}

function collapse(){
    var node = $('#project_tree').tree('getSelected');
    $('#project_tree').tree('collapse',node.target);
}

function expand(){
    var node = $('#project_tree').tree('getSelected');
    $('#project_tree').tree('expand',node.target);
}
function onContextMenu(e, node){
    e.preventDefault();
    // select the node
    $('#project_tree').tree('select', node.target);
    // display context menu

    $('#{0}_menu'.lym_format(node.attributes['category'])).menu('show', {
        left: e.pageX,
        top: e.pageY
    });
}

function onDblClick(node) {
    if(node.attributes["category"]=="object"){
        addManageTab('对象管理', '/manage/var', 'icon-var');
    }
    else if(node.attributes["category"]=="suite"){
        addManageTab('用例管理', '/manage/case', 'icon-case');
    }
    else if(node.attributes["category"]=="keyword"){
        addManageTab('自定义关键字管理', '/manage/keyword', 'icon-user_keyword');
    }
    else if(node.attributes["category"]=="case"){
        addManageTab('用例步骤', '/manage/step', 'icon-step');
    }
    else if(node.attributes["category"]=="var"){
        show_var_win('var_win', 'var_fm', 'edit');
    }
    else if(node.attributes["category"]=="step"){
        show_ui_step_win('ui_step_win', 'ui_step_fm', 'edit');
    }
}

function addManageTab(title, url, icon){
    var selected = $('#project_tree').tree('getSelected');
    var editor_tabs = $("#editor_tabs");
    if (editor_tabs.tabs('exists', title)){
        //如果tab已经存在,则选中并刷新该tab
        editor_tabs.tabs('select', title);
        refreshTab({title: title, url: "{0}/{1}".lym_format(url,selected.attributes["id"])});
    }
    else {
        var content='<iframe scrolling="yes" frameborder="0"  src="{0}/{1}" style="width:100%;height:700px;"></iframe>'.lym_format(url, selected.attributes["id"]);

        editor_tabs.tabs('add',{
            title: title,
            closable: true,
            content: content,
            iconCls: icon||'icon-default'
        });
    }
}

function onShowKeywordPanel(){
    var root = $('#project_tree').tree("getRoot");
    var keyword=[];
    for(var i in G_SYS_KEYWORD_LIST){
        keyword.push(G_SYS_KEYWORD_LIST[i]);
    }
    if(root){
        $(this).combotree('reload', "/api/v1/keyword/?project_id={0}".lym_format(root.id));
    }
}
