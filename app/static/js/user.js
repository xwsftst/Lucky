function init_role_list(){
    $.ajax({
        type : 'get',
        url : '/api/v1/role/',
        success : function(data, textStatus, request) {
            $('#create_user_fm select#create_role_id').combobox("loadData", data["rows"]);
            $('#edit_user_fm select#edit_role_id').combobox("loadData", data["rows"]);
            $('#delete_user_fm select#delete_role_id').combobox("loadData", data["rows"]);
        }
    });
}

function manage_user(win_id, fm_id){
    $('#{0}'.lym_format(fm_id)).form('submit',{
        url: "/api/v1/user/",
        type: "post",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == "success"){
                $("#user_list").datagrid('reload');

                close_win('{0}'.lym_format(win_id));
            }
            show_msg("提示", obj.msg);
        }
    });
}

function edit_user(){
    var row = $('#user_list').datagrid('getSelected');
    if (row){
        $("#edit_user_fm input[name='id']").val(row["id"]);
        $("#edit_user_fm select#edit_role_id").combobox('select', row["role_id"]);
        $("#edit_user_fm input#edit_username").textbox('setValue', row["username"]);
        $("#edit_user_fm input#edit_email").textbox('setValue', row["email"]);
        $("#edit_user_fm input#edit_password").textbox('setValue', row["password"]);
        open_win('edit_user_win');
    }
    else{
        show_msg("提示", "请选择要编辑的用户");
    }
}

function delete_user(){
    var row = $('#user_list').datagrid('getSelected');
    if (row){
        $("#delete_user_fm input[name='id']").val(row["id"]);
        $("#delete_user_fm select#delete_role_id").combobox('select', row["role_id"]);
        $("#delete_user_fm input#delete_username").textbox('setValue', row["username"]);
        $("#delete_user_fm input#delete_email").textbox('setValue', row["email"]);
        $("#delete_user_fm input#delete_password").textbox('setValue', row["password"]);
        open_win('delete_user_win');
    }
    else{
        show_msg("提示", "请选择要删除的用户");
    }
}