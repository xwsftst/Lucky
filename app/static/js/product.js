// function open_win(id){
//     $('#{0}'.lym_format(id)).window('open');
// }
//
// function close_win(id){
//     $('#{0}'.lym_format(id)).window('close');
// }
function show_msg(title, msg){
    $.messager.show({
        title: title,
        msg: msg,
        timeout: 3000,
        showType: 'slide'
    });
}

function manage_product(win_id, fm_id){
    $('#{0}'.lym_format(fm_id)).form('submit',{
        url: "/api/v1/product/",
        type: "post",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == "success"){

                $("#product_list").datagrid('reload');
                parent.init_project_list();
                close_win('{0}'.lym_format(win_id));
            }
            show_msg("提示", obj.msg);
        }
    });
}

function edit_product(){
    var row = $('#product_list').datagrid('getSelected');
    if (row){
        $("#edit_product_fm input[name='id']").val(row["id"]);
        $("#edit_product_fm input#name").textbox('setValue', row["name"]);
        $("#edit_product_fm input#desc").textbox('setValue', row["desc"]);
        open_win('edit_product_win');
    }
    else{
        show_msg("提示", "请选择要编辑的产品");
    }
}

function delete_product(){
    var row = $('#product_list').datagrid('getSelected');
    if (row){
        $("#delete_product_fm input[name='id']").val(row["id"]);
        $("#delete_product_fm input#name").textbox('setValue', row["name"]);
        $("#delete_product_fm input#desc").textbox('setValue', row["desc"]);
        open_win('delete_product_win');
    }
    else{
        show_msg("提示", "请选择要删除的产品");
    }
}