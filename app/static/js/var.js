function show_var_win(win_id, fm_id, method, category){
    var button = {"create": "创建", "edit": "更新", "delete": "删除"};
        $('#{0}'.lym_format(win_id)).window({"title": button[method]+category});
    var selected = $('#project_tree').tree("getSelected");
    if(method == "create"){
        $('#{0} input#object_id'.lym_format(fm_id)).val(selected.attributes["id"]);
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
        open_win(win_id);
    }
    else if(method == "edit" || method == "delete"){
        $('#{0} input#id'.lym_format(fm_id)).val(selected.attributes["id"]);
        $('#{0} input#name'.lym_format(fm_id)).textbox('setValue', selected.attributes["name"]);
        $('#{0} input#value'.lym_format(fm_id)).textbox('setValue', selected.attributes["value"]);
        $('#{0} input#desc'.lym_format(fm_id)).textbox('setValue', selected.attributes["desc"]);
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
        open_win(win_id);
    }
    else{
        show_msg("提示", "方法错误: ".lym_format(method));
        return;
    }
}

function manage_var(win_id, fm_id){
    $('#{0}'.lym_format(fm_id)).form('submit',{
        url: "/api/v1/var/",
        type: "post",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == "success"){
                close_win('{0}'.lym_format(win_id));
                if(document.title=='home_title'){
                    var root = $('#project_tree').tree("getRoot");
                    load_project_tree(root.attributes.id);
                }else{
                    var root = parent.$('#project_tree').tree("getRoot");
                    parent.load_project_tree(root.attributes.id);
                    $("#var_list").datagrid('reload');
                }
            }
            show_msg("提示", obj.msg);
        }
    });
}

function manage_var_table(win_id, fm_id, method, category){
    var button = {"create": "创建", "edit": "更新", "delete": "删除"};
    $('#{0}'.lym_format(win_id)).window({"title": button[method]+category});
    if(method == "create"){
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
        open_win(win_id);
    }
    else if(method == "edit" || method == "delete"){
        var row = $('#var_list').datagrid('getSelected');
        if(row){
            $('#{0} input#id'.lym_format(fm_id)).val(row["id"]);
            $('#{0} input#object_id'.lym_format(fm_id)).val(row["object_id"]);
            $('#{0} input#name'.lym_format(fm_id)).textbox('setValue', row["name"]);
            $('#{0} input#desc'.lym_format(fm_id)).textbox('setValue', row["desc"]);
            $('#{0} input#value'.lym_format(fm_id)).textbox('setValue', row["value"]);
            $('#{0} input#method'.lym_format(fm_id)).val(method);
            $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
            open_win(win_id);
        }
        else{
            show_msg("提示", "请选择要"+button[method]+"的"+category);
        }
    }
    else{
        show_msg("提示", "方法错误: ".lym_format(method));
        return;
    }
}