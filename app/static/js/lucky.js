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