function show_keyword_win(win_id, fm_id, method, category){
    var button = {"create": "创建", "edit": "更新", "delete": "删除"};
    var selected = $('#project_tree').tree("getSelected");
    $('#{0}'.lym_format(win_id)).window({"title": button[method]+category});
    if(method == "create"){
        // 初始化
        $('#{0} input#keyword'.lym_format(fm_id)).textbox('setValue', "");
        $("#keyword_params").datagrid({
            method : 'get',
            url : '/api/v1/user_keyword/',
            queryParams: {id: -1}
        });

        $('#{0} input#suite_id'.lym_format(fm_id)).val(selected.attributes["suite_id"]);
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});

        open_win(win_id);
    }
    else if(method == "edit" || method == "delete"){
        $("#keyword_params").datagrid({
            method : 'get',
            url : '/api/v1/user_keyword/',
            queryParams: {id: selected.attributes["id"]}
        });
        $('#{0} input#id'.lym_format(fm_id)).val(selected.attributes["id"]);
        $('#{0} input#keyword'.lym_format(fm_id)).textbox('setValue', selected.attributes["keyword"]);
        $('#{0} input#suite_id'.lym_format(fm_id)).val(selected.attributes["suite_id"]);
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
        open_win(win_id);
    }
    else{
        show_msg("提示", "方法错误: ".lym_format(method));
        return;
    }
}


function manage_keyword(win_id, fm_id){
    var selected = $('#project_tree').tree("getSelected");
    if(selected){
        var method = $('#{0} input#method'.lym_format(fm_id)).val();
        var suite_id = -1;
        if(method == "create"){
            suite_id = selected.attributes["id"];
        }
        else{
            suite_id = selected.attributes["suite_id"];
        }
        var data = {
            "method": method,
            "suite_id": suite_id,
            "id": $('#{0} input#id'.lym_format(fm_id)).val(),
            "keyword": $('#keyword_fm input#keyword').val()
            };
        var rows = $("#keyword_params").datagrid("getRows");
        var params = [];
        for(var i=0;i<rows.length;i++)
        {
            $("#keyword_params").datagrid('endEdit', i);

            params.push("{'param_0':'{0}','param_1': '{1}','param_2':'{2}', 'param_3': '{3}', 'param_4': '{4}'}".lym_format(
                rows[i].param_0,rows[i].param_1,rows[i].param_2,rows[i].param_3,rows[i].param_4,
            ));
        }

        data["params"] = "[" + params.join(",") + "]";

        $.ajax({
            type : 'post',
            url : '/api/v1/user_keyword/',
            data:  data,
            success : function(data, textStatus, request) {
                parent.refresh_project_tree();
                close_win(win_id);
                show_msg("提示信息", data.msg);
            }
        });

    }
}

function show_user_keyword_suite_win(win_id, fm_id, method, category){
    var button = {"create": "创建", "edit": "更新", "delete": "删除"};
    $('#{0}'.lym_format(win_id)).window({"title": button[method]+category});
    var selected = $('#project_tree').tree("getSelected");
    if(method == "create"){
        $('#{0} input#project_id'.lym_format(fm_id)).val(selected.attributes["id"]);
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
        open_win(win_id);
    }
    else if(method == "edit" || method == "delete"){
        $('#{0} input#id'.lym_format(fm_id)).val(selected.attributes["id"]);
        $('#{0} input#name'.lym_format(fm_id)).textbox('setValue', selected.attributes["name"]);
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

function manage_user_keyword_suite(win_id, fm_id){
    $('#{0}'.lym_format(fm_id)).form('submit',{
        url: "/api/v1/user_keyword_suite/",
        type: "post",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == "success"){
                close_win('{0}'.lym_format(win_id));
                if(document.title=='home_title'){
                    load_project_tree(obj.project_id);
                }else{
                    parent.load_project_tree(obj.project_id);
                    $("#user_keyword_suite_list").datagrid('reload');
                }
            }
            show_msg("提示", obj.msg);
        }
    });
}

function manage_user_keyword_suite_table(win_id, fm_id, method, category){
    var button = {"create": "创建", "edit": "更新", "delete": "删除"};
    $('#{0}'.lym_format(win_id)).window({"title": button[method]+category});
    if(method == "create"){
        $('#{0} input#method'.lym_format(fm_id)).val(method);
        $("#{0} a".lym_format(fm_id)).linkbutton({'text': button[method]});
        open_win(win_id);
    }
    else if(method == "edit" || method == "delete"){
        var row = $('#user_keyword_suite_list').datagrid('getSelected');
        if(row){
            $('#{0} input#id'.lym_format(fm_id)).val(row["id"]);
            $('#{0} input#project_id'.lym_format(fm_id)).val(row["project_id"]);
            $('#{0} input#name'.lym_format(fm_id)).textbox('setValue', row["name"]);
            $('#{0} input#desc'.lym_format(fm_id)).textbox('setValue', row["desc"]);
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