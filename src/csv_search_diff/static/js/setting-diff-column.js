$("#add_diff_row").click(function(){
    new_diff_cols = $(".diff-cols:last").clone();
    $("select", new_diff_cols).val("");
    $("p", new_diff_cols).text("");

    new_diff_cols.appendTo($(".diff-cols").parent());
})

$("#delete_diff_row").click(function(){
    $(".diff-cols:last").remove();
})

$("#page_back").click(function(){
    if(confirm("前の画面に戻ります。よろしいですか？")) {
        $("#back-form").submit();å
    }
})