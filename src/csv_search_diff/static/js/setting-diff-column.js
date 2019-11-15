$("#add_diff_row").click(function(){
    var new_diff_cols = $(".diff-cols:last").clone();
    var NUM_GET_PATTERN = /form-(\d+)-csv1_diff_col/;
    var REPLACE_PATTERN = /\d+?/
    var match = NUM_GET_PATTERN.exec();
    var next_num = 0;
    if(match != null && match.length > 0) {
        next_num = parseInt(match[1]);
    }

    // 新規IDとnameに書き換え
    $("select", new_diff_cols).attr("id").replace(REPLACE_PATTERN, next_num);
    $("select", new_diff_cols).attr("name").replace(REPLACE_PATTERN, next_num);

    // 選択を初期状態に戻す
    $("select", new_diff_cols).val("");
    $("select > option", new_diff_cols).removeProp("selected");
    $("p", new_diff_cols).text("");

    new_diff_cols.appendTo($(".diff-cols").parent());
});

$("#delete_diff_row").click(function(){
    $(".diff-cols:last").remove();
});

$("#page_back").click(function(){
    if(confirm("前の画面に戻ります。よろしいですか？")) {
        $("#back-form").submit();
    }
});

$(".diff-cols select").changed(function(this) {
    var prev_or_next = getPrevOrNextSelect(this);
    var detail_area = $(this).parent().children("p");
    var diff_col_selects = $(this).parent().children("select");
    var MESSAGE_FORMAT = "CSV1の[header1]とCSV2の[header2]を比較する"
    if (diff_col_selects[0].children("option:selected").length == 0 ||
        diff_col_selects[1].children("option:selected").length == 0) {
        detail_area.text("");
    } else {
        var detail = MESSAGE_FORMAT;
        detail = detail.replace("[header1]", diff_col_selects[0].children("option:selected").text());
        detail = detail.replace("[header2]", diff_col_selects[1].children("option:selected").text());
        detail_area.text(detail);
    }
});