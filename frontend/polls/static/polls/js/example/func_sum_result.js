
$(function () {

    var test = document.getElementById("example_tst").value;
    var sum_dic = getJson(test, 'func_summary');
    var columns = getVertColumn(sum_dic);
    var data = getVertData(sum_dic, columns);
    // initialize grid
    var options = {emptyRow: true, sortable: false};
	var grid = $(document.getElementById("sum_func_info")).grid(data, columns, options);
    draw_grid(grid);

    // api examples
    var $row = grid.getRowByIndex(0);
    console.group("data api examples");
    console.log("grid.getRowDataByIndex(0):", grid.getRowDataByIndex(0));
    console.log("grid.getRowData($row):", grid.getRowData($row));
    console.log("grid.getGridData():", grid.getGridData());
    console.groupEnd();

    window.grid = grid;
});
