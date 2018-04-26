require([
    'underscore',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc, TableView) {
    
    var Imgsrc = TableView.BaseCellRenderer.extend({
        canRender: function(cell) {
            // Only use the cell renderer for the range field
            return cell.field === 'IMAGE';
        },
        render: function($td, cell) {
            $td.html(_.template('<img src="<%-imgsrc%>" style="height:200px !important;"/>',{imgsrc:cell.value}));
        }
    });
    mvc.Components.get('table1').getVisualization(function(tableView){
        // Register custom cell renderer
        tableView.table.addCellRenderer(new Imgsrc());
        // Force the table to re-render
        tableView.table.render();
    });
});
