/*
* キー項目設定の選択変更時の実処理
*/
const key_col_change_function = function(obj){
    var target = obj.target;
    set_key_col_detail(target);
}

/*
* 「項目を追加する」ボタンクリック時の処理
*/
$("#add_key_row").click(function(){
    var new_diff_cols = $(".key-cols:last").clone();
    var csv1_select = $(" select:first", new_diff_cols)
    var NUM_GET_PATTERN = /form-(\d+)-csv1_diff_col/;
    var REPLACE_PATTERN = /\d+?/
    var match = NUM_GET_PATTERN.exec(csv1_select.attr('name'));
    var next_num = 0;
    if(match != null && match.length > 0) {
        next_num = parseInt(match[1]) + 1;
    }

    // 新規IDとnameに書き換え
    $(" select", new_diff_cols).each(function(index, elem){
        elem = $(elem);
        elem.attr("id", elem.attr("id").replace(REPLACE_PATTERN, next_num));
        elem.attr("name", elem.attr("name").replace(REPLACE_PATTERN, next_num));
    });

    // 選択を初期状態に戻す
    $(" select", new_diff_cols).val("");
    $(" select > option", new_diff_cols).removeProp("selected");
    $(" p", new_diff_cols).text("");

    // 選択肢変更時の処理を追加
    $(" select", new_diff_cols).change(key_col_change_function);

    new_diff_cols.insertAfter($(".key-cols:last"));
});

/*
* 「項目を削除する」ボタンクリック時の処理
*/
$("#delete_key_row").click(function(){
    if($(".key-cols").length > 1) {
        $(".key-cols:last").remove();
    }
});

/*
* 「戻る」ボタンクリック時の処理
*/
$("[name='page_back']").click(function(){
    if(confirm("前の画面に戻ります。よろしいですか？")) {
        $("#back-form").submit();
    }
});

/*
* キー項目設定の選択変更処理
*/
$(".key-cols select").change(key_col_change_function);

/*
* キー項目設定の選択変更時にキー項目設定詳細に表示する処理
* obj: 選択変更処理を行ったSelectエレメント
*/
function set_key_col_detail(obj) {
    var form_row = $(obj).closest("div.row");
    var detail_area = $(" p", form_row);
    var diff_col_selects = $(" select", form_row);
    var MESSAGE_FORMAT = "CSV1の[header1]とCSV2の[header2]をキーにする";
    var diff_col_selected_csv1 = $(diff_col_selects[0]).children("option:selected");
    var diff_col_selected_csv2 = $(diff_col_selects[1]).children("option:selected");
    if (diff_col_selected_csv1.length == 0 ||
        diff_col_selected_csv2.length == 0) {
        detail_area.text("");
    } else {
        var detail = MESSAGE_FORMAT;
        detail = detail.replace("[header1]", diff_col_selected_csv1.text());
        detail = detail.replace("[header2]", diff_col_selected_csv2.text());
        detail_area.text(detail);
    }
}

/*
* 画面表示時の初期処理
*/
$.when($.ready).then(function(){
    $("select:odd").each(function(index, elem){
        set_key_col_detail(elem);
    });
})