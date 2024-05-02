
var table;
var excel = false;
var $local_cluster;
$( document ).ready(function() {
	search_engine_status('isstarted');

	$(document.getElementById("butt_start")).trigger('click');
});

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


function search_engine_status(start){
	var params = {};
	params['version_params'] = $("#version_params").val();
//	alert(params['version_params']);
//	alert($("#version_params").val());
	$.ajax({
		type : 'GET',
        url:'http://localhost:8001',
        data : JSON.stringify(params),
        dataType:'json',
        contentType: 'application/json',
        beforeSend: function(){
//       	 $('.selected_info').text('');
//       	 $('.rd_xmlviewer XMP').text('');
//       	 	showProgress();
        	if (start == 'isstarted') {
        		$("#LoadingImage").show();
        	}
        	else {
        		$("#loading").html("<img src='/template/img/loading_small.gif' />");
        	}
        },
        success:function(data){
//        	alert(data.data);
           $("#content").show();
           $("#number_of_nodes").empty();
           $("#number_of_indices").empty();
           var now = new Date();

           var year= now.getFullYear();
           var mon = (now.getMonth()+1)>9 ? ''+(now.getMonth()+1) : '0'+(now.getMonth()+1);
           var day = now.getDate()>9 ? ''+now.getDate() : '0'+now.getDate();
                    
           var chan_val = year + '-' + mon + '-' + day;
           
           $("#current_time").html(now);

        	$.each(data,function(key,value) {
        		    var active_primary_shards = '';
        			if(key == 'cluster_name') {
        						$("#cluster_name").html("<b>[" + value + "]</b>");
        					}
        			else if(key == 'number_of_nodes') {
								$("#number_of_nodes").html("Nodes: " + value);
							}
        			else if(key == 'active_primary_shards') {
        				active_primary_shards = value;
        				$("#number_of_primary_shards").html(numberWithCommas(value));
					}
        			else if(key == 'active_shards') {
        				$("#number_of_replica_shards").html(numberWithCommas(parseInt(value)-parseInt(data['active_primary_shards'])));
					}
        			else if(key == 'status') {
        					if(value == 'red') {
        						$("#cluster_health").html("&nbsp;<img src='img/health-red.svg' />&nbsp;&nbsp;" + value);
        						$("#cluster_health_alert").html("<img src='img/alert-red.svg' />&nbsp;&nbsp;");
        							}
        					else if(value == 'yellow') {
        						$("#cluster_health").html("&nbsp;<img src='img/health-yellow.svg' />&nbsp;&nbsp;" + value);
        						$("#cluster_health_alert").html("<img src='img/alert-yellow.svg' />&nbsp;&nbsp;");
//        						$("#unassigned_alert_message").html("Allocate missing replica shards.");
        							}
        					else if(value == 'green') {
        						$("#cluster_health").html("&nbsp;<img src='img/health-green.svg' />&nbsp;&nbsp;" + value);
        						$("#cluster_health_alert").html("<img src='img/alert-green.svg' />&nbsp;&nbsp;");
        							}
        					
        					$("#status").html(value);
					}
        			else if(key == 'unassigned_shards') {
        						if (value != 0) {
        							$("#unassigned_alert_message").html("&nbsp;&nbsp;<b>unassigned_shards : " + value + "</b>&nbsp;(Allocate missing primary shards and replica shards.)");
//        							$("#unassigned_alert").html("&nbsp;&nbsp;<b>unassigned_shards : " + value);
        								}
        						else {
        							$("#unassigned_alert_message").empty();
        								}
        					}
        			else if(key == 'count') {
        				$("#number_of_indices").html("Indices: " + numberWithCommas(value));
        					}
        			else if(key == 'docs') {
        				var obj = jQuery.parseJSON(value);
//        				alert(obj.count);
        				$("#number_of_doucuments").html(numberWithCommas(obj.count));
        					}
        			else if(key == 'store') {
        				var obj = jQuery.parseJSON(value);
//        				alert(obj.count);
        				$("#number_of_disk").html(numberWithCommas(obj.size.toUpperCase()));
        					}
        			else if(key == 'jvm') {
        				var obj = jQuery.parseJSON(value);
        				var heap_used = parseInt(obj.mem.heap_used_in_bytes/(1024*1024*1024));
        				var heap_max = parseInt(obj.mem.heap_max_in_bytes/(1024*1024*1024));
        				$("#elastic_uptime").html(obj.max_uptime);
        				$("#heap_percent").html(((heap_used/heap_max)*100).toFixed(2) + "%");
        				$("#heap_used_in_bytes").html(heap_used + "GB");
        				$("#heap_max_in_bytes").html(heap_max + "GB");
        					}
        			else if(key == 'versions') {
        				var obj = jQuery.parseJSON(value);
        						$("#elastic_version").html(obj);
        					}
        			else if(key == 'fs') {
        				var obj = jQuery.parseJSON(value);
        				var available_bytes = parseInt(obj.available_in_bytes/(1024*1024*1024));
        				var total_fs_bytes = parseInt(obj.total_in_bytes/(1024*1024*1024));
        				$("#total_fs").html(obj.total.toUpperCase());
        				$("#available_fs").html(obj.available.toUpperCase());
        				$("#fs_percent").html(((available_bytes/total_fs_bytes)*100).toFixed(2) + "%");
        			}
        			
//        		alert('key:'+key+', value:'+value);
        			});
        },
        error : function(e){ 
        },
        complete : function() {
//        	hideProgress();   
        	$("#loading").empty();
        	$("#LoadingImage").hide();
        }
     });
}




