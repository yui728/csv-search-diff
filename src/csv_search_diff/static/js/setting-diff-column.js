const diff_col_change_function = function(obj){
    var target = obj.target;
    set_diff_col_detail(target);
}
$("#add_diff_row").click(function(){
    var new_diff_cols = $(".diff-cols:last").clone();
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
        elem.attr("id") = attr.attr("id").replace(REPLACE_PATTERN, next_num);
        elem.
    });
    select_elements.attr("id") = select_elements.attr("id").replace(REPLACE_PATTERN, next_num);
    select_elements.attr("name") = select_elements.attr("name").replace(REPLACE_PATTERN, next_num);

    // 選択を初期状態に戻す
    $(" select", new_diff_cols).val("");
    $(" select > option", new_diff_cols).removeProp("selected");
    $(" p", new_diff_cols).text("");

    // 選択肢変更時の処理を追加
    $(" select", new_diff_cols).change(diff_col_change_function);

    new_diff_cols.insertAfter($(".diff-cols:last"));
});

$("#delete_diff_row").click(function(){
    if($(".diff-cols").length > 1) {
        $(".diff-cols:last").remove();
    }
});

$("[name='page_back']").click(function(){
    if(confirm("前の画面に戻ります。よろしいですか？")) {
        $("#back-form").submit();
    }
});

$(".diff-cols select").change(diff_col_change_function);

function set_diff_col_detail(obj) {
    var form_row = $(obj).closest("div.row");
    var detail_area = $(" p", form_row);
    var diff_col_selects = $(" select", form_row);
    var MESSAGE_FORMAT = "CSV1の[header1]とCSV2の[header2]を比較する";
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

$.when($.ready).then(function(){
    $("select:odd").each(function(index, elem){
        set_diff_col_detail(elem);
    });
})