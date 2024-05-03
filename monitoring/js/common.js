var intentsList = ['ㄱ','ㄱ','ㄱ','ㄱ','ㄱ','ㄱ','ㄴ','ㄷ','ㄹ','ㄱㄱ','ㄴㄴ','ㄷㄷ','ㄹㄹ','가','나','다','라','가나','다라','마바','사아','자차','카타','파하','가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하'];//의도 목록
for(i=0;i<1000;i++) intentsList.push('가나다라마바사');//테스트용
var entitiesList = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅌ','ㅋ','ㅍ','ㅎ','ㄱㄱ','ㄴㄴ','ㄷㄷ','ㄹㄹ','가','나','다','라','가나','다라','마바','사아','자차','카타','파하'];//개체 목록 

$(function(){
	/* GNB */
	var $wrap = $('#wrapper');
	var $gnbLi = $('#gnb>ul li');
	var $gnbMenu = $('#gnb>ul a');
	var $d2bar = $('#depth2_bar');
	setD2bar();
	$gnbMenu.click(function(){
		$gnbLi.removeClass('active');
		$(this).closest('li').addClass('active');
	});
	$gnbLi.bind('addClass',setD2bar);
	function setD2bar(){
		var $active = $('#gnb .active').eq(-1);
		var hHeight = $('#header').outerHeight();
		if($active.find('ul').length > 0){
			var $moreTarget = $active.find('li').eq(0);
			if(!$moreTarget.hasClass('active')) $moreTarget.addClass('active');
			$d2bar.show();
			$wrap.css('padding-top',hHeight+$d2bar.outerHeight());
		}else if($active.parent('ul').parent('li')[0]){
			var $moreTarget = $active.parent('ul').parent('li');
			if(!$moreTarget.hasClass('active')) $moreTarget.addClass('active');
			$d2bar.show();
			$wrap.css('padding-top',hHeight+$d2bar.outerHeight());
		}else{
			$d2bar.hide();
			$wrap.css('padding-top',hHeight);
		}
	}
	
	/* #left/#right show/hide 바인딩 */
	$('#right').bind('show',function(){ $('#util .ic_test').addClass('active'); });
	$('#right').bind('hide',function(){ $('#util .ic_test').removeClass('active'); });
	$('#left, #right').bind('show hide',function(){
		$(window).trigger('resize');//DataTables 칼럼 폭 리사이즈 등
	});
	/* #center show/hide 바인딩 */
	$('#center').bind('show',function(){ $('#left').removeClass('wide'); });
	$('#center').bind('hide',function(){ $('#left').addClass('wide'); });
	
	/* datepicker hide() */
	$(document).mousedown(function(e){
		var clearTarget = $('.datepicker:visible') && parent.$('.datepicker:visible');
		clearTarget.each(function(){
			if(!$(e.target).hasClass('dateonly') && !$(e.target).hasClass('datetime')){
				var box = $(this).offset();
				box.right = box.left + $(this).outerWidth();
				box.bottom = box.top + $(this).outerHeight();
				if(!((box.left <= e.pageX && e.pageX <= box.right) && (box.top <= e.pageY && e.pageY <= box.bottom))){ 
					$(this).hide();
				}
			}
		});
	}); 
});

(function($){
	$.each(['show','hide','addClass'],function(i,ev){//Trigger Event 만들기
		var el = $.fn[ev];
		$.fn[ev] = function(){
			el.apply(this,arguments);
			this.trigger(ev);
			return this;
		};
	});
	
	$.fn.autoTextareaHeight = function(){
		return this.each(function(){
			var $textarea = $(this);
			var bw = Number($textarea.css('border-top-width').replace('px',''))+Number($textarea.css('border-bottom-width').replace('px',''));
			clearTimeout($textarea[0].timeoutForH);
			$textarea[0].timeoutForH = setTimeout(function(){//Timeout : 붙여넣기 대응
				var axis = $('<div>').css({'display':'inline-block','width':0,'height':$textarea.outerHeight()});
				axis.insertBefore($textarea)
				$textarea.css('height',$textarea.height(0).prop('scrollHeight')+bw);
				axis.remove();
			},0);
		});
	}
})(jQuery);

function openModal(href){
	var dNum = $('.modal_wrap').length;
	$('#blank').append('<div class="modal_back"></div><div class="modal_wrap modal_wrap'+dNum+'"></div>');
	$('.modal_wrap'+dNum).load(href,function(){
		var box = $(this);
		var boxBack = box.prev('.modal_back');
		boxBack.css({'z-index':500+dNum});			
		box.css({'z-index':500+dNum,'left':'50%','top':'50%','margin-left':-box.outerWidth()/2,'margin-top':-box.outerHeight()/2}).find('.modal_close').click(function(){
			boxBack.remove();
			box.remove();
			return false;
		});
	});	
}

(function(){
	/* ---------- DataTables ---------- */	
	function fullScrollTableSet(){//세로로 꽉 차는 scrollBody 만들기
		var $tbody = $('.dataTables_scrollBody_full');
		$tbody.each(function(){
			var $tWrap = $(this).closest('.dataTables_wrapper');
			var $this = $(this);
			var spaceHeight = $('#container').height()-$tWrap.position().top-($this.offset().top-$tWrap.offset().top)-20;
			var minHeight = 200;
			$this.css('max-height',Math.max(spaceHeight,minHeight));
			this.api.columns.adjust();//window.resize 외의 요소로 스크롤바 show/hide에 따른 DataTables 칼럼 폭 리사이즈
		});
	}		
	$(document).on('init.dt',function(e,settings){//테이블 생성할 때 옵션 'scrollY' 값이 '0'이면 'fullScrollTable'
		var api = new $.fn.dataTable.Api(settings);
		if(settings.nScrollBody && settings.nScrollBody.clientHeight == 0){ 
			$(settings.nScrollBody).addClass('dataTables_scrollBody_full');
			$(settings.nScrollBody)[0].api = api;
		}
		fullScrollTableSet();
	});
	$(window).resize(function(){
		fullScrollTableSet();
	});
	$(document).on('show hide','.searched_info',function(){
		fullScrollTableSet();
	});
	
	/* ---------- .dt-editor-input ---------- */
	$(document).on('click','.dt-editor-input',function(){
		if(!$(this).hasClass('active')){
			var $selected = $(this);
			$selected.addClass('active');
			var string = $selected.text();
			var $input = $('<input type="text">');
			$selected.html($input);
			$input.focus().val(string);
			$(window).trigger('resize');
			
			$input.bind('focusout keydown',function(e){
				if(e.type == 'focusout' || e.keyCode == 13){ 
					$selected.html('<span>'+$(this).val()+'</span>').removeClass('active');
					$(window).trigger('resize');
		    $(".btn4").attr('disabled', false);
					
				}
			})
		}
	});
	
	/* ---------- .dt-editor-multiple ---------- */
	$(document).on('click','.dt-editor-multiple',function(){
		if(!$(this).hasClass('input_list_wrap')){
			var $selected = $(this);
			$selected.addClass('input_list_wrap');
			var $box;
			var $input;
			var $removeBtn;
			var $items = [];
			var $span = $selected.find('span');
			for(i=0;i<$span.length;i++){
				$box = $('<span>',{class:'input_list_item'});
				$input = $('<input>',{type:'text'}).val($span.eq(i).text());
				$removeBtn = $('<button>').text('삭제').click(function(){ 
					$(this).closest('.input_list_item').remove();
					$(window).trigger('resize');
				});
				$items.push($box.append($input).append($removeBtn));
			};
			var $maker = $('<input>',{type:'text',class:'input_list_item_maker',placeholder:'유의어를 입력해 주십시오.'}).keydown(function(e){
				if(e.keyCode == 13 && $(this).val().replace(/\s/g,'').length > 0){
					var $box = $('<span>',{class:'input_list_item'});
					var $input = $('<input>',{type:'text'}).val($(this).val());
					var $removeBtn = $('<button>').text('삭제').click(function(){ 
						$box.remove(); 
						$(window).trigger('resize');
					});
					$box.append($input).append($removeBtn).insertBefore($(this));
					$maker.val('');
					setTimeout(function(){ $maker.focus(); },0);//추가 중 스크롤이 발생했을 때 브라우저의 scrollTop 회귀를 막는다.
					$(window).trigger('resize');
				}
			});
			$items.push($maker);
			$selected.html($items);	
			setTimeout(function(){ $maker.focus(); },0);
			$(window).trigger('resize');
		}
	});
	
	$(document).bind('click',function(e){
		var $clearTarget = $('.dt-editor-multiple.input_list_wrap');
		$clearTarget.each(function(){
			var $this = $(this);
			var box = $this.offset();
			box.right = box.left+$(this).outerWidth();
			box.bottom = box.top+$(this).outerHeight();
			if(!((box.left <= e.pageX && e.pageX <= box.right) && (box.top <= e.pageY && e.pageY <= box.bottom))){ 
				var $content = $('#content');
				console.log(e.target.id);
				if(e.target.className == 'dataTables_scrollBody' || ((e.target.id == 'center' || e.target.id == 'full') && e.pageX > $content.offset().left+$content.outerWidth())){ 
					return;//스크롤바 클릭은 제외
				}
				var $items = [];
				var $input = $this.find('.input_list_item>input[type=text]');
				for(i=0;i<$input.length;i++) $items.push($('<span>').text($input.eq(i).val()));
				setTimeout(function(){ 
					$this.html($items).removeClass('input_list_wrap'); 
					$(window).trigger('resize');
				},0);
			}
		});
	});
	
	/* ---------- .dt-editor-autocomplete ---------- */
	var $content;
	var $selectedInput;
	
	/* 선택창 활성화 */
	$(document).on('click','.dt-editor-autocomplete>input[type=text]',function(){
		if(!$selectedInput){
			$selectedInput = $(this);
			$selectedInput[0].originVal = $selectedInput.val();
			$marker = $selectedInput.prev('.marker');
			$selectedInput.addClass('active');
			$content = $selectedInput.parents();
			$content.bind('scroll.removeAutocompleteOptBox',removeOpt);

			var input = $selectedInput.offset();
			var $optBox = $('<div>',{class:'autocomplete_opt_box'}).css({'left':input.left,'width':$selectedInput.outerWidth()});
			if(input.top < $(window).height()*2/3 && !$(this).closest('.dt-editor-autocomplete').hasClass('up')){
				$optBox.css('top',input.top+$selectedInput.outerHeight());
			}else{
				$optBox.css('bottom',$(window).height()-input.top);
			}
			var $optList = $('<ul>',{class:'filtered'});
			var $etc;
			if($marker.hasClass('s')){
				$optList.addClass('s');
				$etc = $('<ul><li>의도 없음</li></ul>');
			}else if($marker.hasClass('a')){
				$optList.addClass('a');
				$etc = $('<ul><li>개체 없음</li></ul>');
			}
			
			$optBox.html($optList).append($etc);
			$('#blank').append($optBox);
			
			clearTimeout(filterTimeout);
			filterTimeout = setTimeout(function(){ filterOpt($optList,$selectedInput[0].originVal); },0);
		}
	});
	
	/* 선택창 필터링 (IE에서 응답성이 떨어짐) */
	var optTimeout;
	var filterTimeout;
	$(document).on('input propertychange','.dt-editor-autocomplete>input[type=text]',function(){
		clearTimeout(filterTimeout);
		clearTimeout(optTimeout);
		var val = $(this).val();
		var $optList = $('.autocomplete_opt_box>ul.filtered');
		optTimeout = setTimeout(function(){
			if($optList[0]){
				$optList.html('<li class="message">검색 중입니다.</li>');
				filterTimeout = setTimeout(function(){ filterOpt($optList,val); },500);
			}
		},0);
	});
	function filterOpt($optList,val){
		var $filtered = [];
		var optList = ($marker.hasClass('s')) ? intentsList : entitiesList
		for(i=0;i<optList.length;i++){
			if(optList[i].indexOf(val) > -1) $filtered.push($('<li>'+optList[i]+'</li>'));
		};
		if($filtered.length == 0) $filtered.push($('<li class="message">검색 결과가 없습니다.</li>'));
		$optList.html($filtered);
	}
	
	/* 항목 선택 */
	$(document).on('mousedown','.autocomplete_opt_box>ul>li:not(.message)',function(){
		$selectedInput.val($(this).text()).attr('title',$(this).text()).removeClass('active');
		$(this).closest('.autocomplete_opt_box').remove();
		$selectedInput = null;
		$content.unbind('scroll.removeAutocompleteOptBox');
	});
	
	/* 선택창 제거 */
	$(window).bind('resize',removeOpt);
	function removeOpt(){
		if($selectedInput){
			clearTimeout(filterTimeout);
			$selectedInput.val($selectedInput[0].originVal).attr('title',$selectedInput[0].originVal).removeClass('active');
			$('.autocomplete_opt_box').remove();
			$selectedInput = null;
			$content.unbind('scroll.removeAutocompleteOptBox');
		}
	}
	$(document).bind('mousedown',docDown);
	function docDown(e){
		var $clearTarget = $('.autocomplete_opt_box');
		$clearTarget.each(function(){
			if($(e.target)[0] != $selectedInput[0]){
				var box = $(this).offset();
				box.right = box.left+$(this).outerWidth();
				box.bottom = box.top+$(this).outerHeight();
				if(!((box.left <= e.pageX && e.pageX <= box.right) && (box.top <= e.pageY && e.pageY <= box.bottom))){ 
					clearTimeout(filterTimeout);
					$selectedInput.val($selectedInput[0].originVal).attr('title',$selectedInput[0].originVal).removeClass('active');
					$(this).remove();
					$selectedInput = null;
					$content.unbind('scroll.removeAutocompleteOptBox');
				}
			}
		});
	}
	
	/* ---------- .dt-editor-highlighted ---------- */
	var $content2;
	var $downTarget;//selection
	var $highlightTarget;//selection
	var highlightedSelection;//selection
	var $matchedTarget;//matched click
	var $fixedInput;
	
	/* autocomplete 활성화 - selection */
	$(document).on('mousedown','.dt-editor-highlighted',function(){
		$downTarget = $(this);
	});
	$(document).on('mouseup','.dt-editor-highlighted',function(e){
		if($downTarget && $(e.target)[0] == $downTarget[0]){	
			highlightedSelection = window.getSelection().getRangeAt(0);
			var offset = highlightedSelection.getBoundingClientRect();
			if(highlightedSelection.startContainer == highlightedSelection.endContainer && highlightedSelection.toString().replace(/\s/g,'').length > 0){
				$highlightTarget = $(this);
				$content2 = $highlightTarget.parents();
				$content2.bind('scroll.removeAutocompleteOptBox',removeOpt).bind('scroll.removeAutocompleteOptBox2',removeOpt2);
				
				var extracted = highlightedSelection.extractContents();	
				var em = document.createElement('em');
				em.setAttribute('class','highlighted');
				em.appendChild(extracted);
				highlightedSelection.insertNode(em);
				
				var $inputBox = $('<span class="dt-editor-autocomplete"><span class="marker a">@</span><input type="text" placeholder="개체명을 입력해 주십시오."></span>').css({'position':'fixed','left':offset.left,'top':offset.top+offset.height,'width':250});
				$('#blank').append($inputBox);
				$fixedInput = $inputBox.children('input[type=text]');
				if(offset.top+offset.height > $(window).height()*2/3){
					 $inputBox.addClass('up').css('top',offset.top-$inputBox.outerHeight());
				}
				$fixedInput.click().focus();
			}
		}
		$downTarget = null;
	});
	
	/* autocomplete 활성화 - matched click */
	$(document).on('click','.dt-editor-highlighted>em:not(.highlighted)',function(e){
		$matchedTarget = $(this);
		$content2 = $(this).parents();
		$content2.bind('scroll.removeAutocompleteOptBox',removeOpt).bind('scroll.removeAutocompleteOptBox2',removeOpt2);
		
		var offset = $matchedTarget.offset();
		var e = $matchedTarget.children('.e').text();
		var $inputBox = $('<span class="dt-editor-autocomplete"><span class="marker a">@</span><input type="text" placeholder="개체명을 입력해 주십시오."></span>').css({'position':'fixed','left':offset.left,'top':offset.top+$(this).height(),'width':250});
		$('#blank').append($inputBox);
		$fixedInput = $inputBox.children('input[type=text]');
		if(offset.top+$(this).height() > $(window).height()*2/3){
			 $inputBox.addClass('up').css('top',offset.top-$inputBox.outerHeight());
		}
		$fixedInput.click().focus().val(e);
	});
	
	/* 항목 선택 */
	$(document).on('mousedown','.autocomplete_opt_box>ul.filtered>li:not(.message)',function(){
		if(highlightedSelection){
			var $matchingTarget = $highlightTarget.children('.highlighted');
			var text = $matchingTarget.text();
			var before = '';
			var after = '';
			if(text.charAt(0) == ' '){
				text = text.substring(1);
				before = ' ';
			}
			if(text.charAt(text.length-1) == ' '){
				text = text.substring(0,text.length-1);
				after = ' ';
			}
			$matchingTarget.html(before+'[@<span class="e">'+$(this).text()+'</span>:<span class="w">'+text+'</span>]'+after).removeClass('highlighted');
			$('#blank>.dt-editor-autocomplete').remove();
			highlightedSelection = null;
			$fixedInput = null;
			$content2.unbind('scroll.removeAutocompleteOptBox',removeOpt).unbind('scroll.removeAutocompleteOptBox2');
		}else if($matchedTarget){
			$matchedTarget.children('.e').text($(this).text());
			$('#blank>.dt-editor-autocomplete').remove();
			$matchedTarget = null;
			$fixedInput = null;
			$content2.unbind('scroll.removeAutocompleteOptBox',removeOpt).unbind('scroll.removeAutocompleteOptBox2');
		}
	});
	$(document).on('mousedown','.autocomplete_opt_box>ul:not(.filtered)>li',function(){
		if($matchedTarget){
			var $parent = $matchedTarget.closest('.dt-editor-highlighted');
			$matchedTarget.text($matchedTarget.children('.w').text());
			$matchedTarget.contents().unwrap();
			$parent.html($parent.html());
			$('#blank>.dt-editor-autocomplete').remove();
			$matchedTarget = null;
			$fixedInput = null;
			$content2.unbind('scroll.removeAutocompleteOptBox',removeOpt).unbind('scroll.removeAutocompleteOptBox2');
		}
	});
	
	/* autocomplete 제거 */
	$(window).bind('resize',removeOpt2);
	function removeOpt2(){
		if($fixedInput){
			clearTimeout(filterTimeout);
			$('#blank>.dt-editor-autocomplete').remove();
			if(highlightedSelection){
				$highlightTarget.children('.highlighted').contents().unwrap();
				$highlightTarget.html($highlightTarget.html());
				highlightedSelection = null;
			}else if($matchedTarget){
				$matchedTarget = null;
			}
			$fixedInput = null;
			$content2.unbind('scroll.removeAutocompleteOptBox',removeOpt).unbind('scroll.removeAutocompleteOptBox2');
		}
	}
	$(document).bind('mousedown',docDown2);
	function docDown2(e){
		var $clearTarget = $('#blank>.dt-editor-autocomplete');
		$clearTarget.each(function(){
			var box = $(this).offset();
			box.right = box.left+$(this).outerWidth();
			box.bottom = box.top+$(this).outerHeight();
			var lastTop = box.top;
			var lastBottom = box.bottom;
			
			if($(this).next('.autocomplete_opt_box')[0]){
				var $optBox = $(this).next('.autocomplete_opt_box');
				var box2 = $optBox.offset();
				box2.bottom = box2.top+$optBox.outerHeight();
				lastTop = Math.min(box.top,box2.top); 
				lastBottom = Math.max(box.bottom,box2.bottom); 
			}
			
			if(!((box.left <= e.pageX && e.pageX <= box.right) && (lastTop <= e.pageY && e.pageY <= lastBottom))){ 
				clearTimeout(filterTimeout);
				$(this).remove();
				if(highlightedSelection){
					$highlightTarget.children('.highlighted').contents().unwrap();
					$highlightTarget.html($highlightTarget.html());
					highlightedSelection = null;
				}else if($matchedTarget){
					$matchedTarget = null;
				}
				$fixedInput = null;
				$content2.unbind('scroll.removeAutocompleteOptBox',removeOpt).unbind('scroll.removeAutocompleteOptBox2');
			}
		});
	}
})();

//직렬화 필요해서 추가..(jquery.serializeObject.min.js 플러그인으로 기능 업그레이드)
/*jQuery.fn.serializeObject = function() {
	var obj = null;
	try {
		var arr = this.serializeArray();
		if (arr) {
			obj = {};
			jQuery.each(arr, function() {
				obj[this.name] = this.value;
			});
		}
	} catch (e) {
		alert(e.message);
	} finally {
	}
	return obj;
}*/

function hidePage(){
	$('#left').empty().hide(); 
	$('#full').empty().hide(); 
	$('#center').empty().hide();
}

function loadCenterPage(url, leftMenuHide, title){
	if(leftMenuHide=='Y') hidePage();
	$('#center').load(''+url);
	$('#center').show();
	if(title!=null){
		$('#gnb_title').html(null);
		$('#gnb_title').html(title);
	}
}

function loadCenterPageAjax(url, leftMenuHide, index){
	if(leftMenuHide=='Y') hidePage();
	
	var row = table.rows().data()[index];
	
	$.ajax({
	    url: 'loadPage/'+url,
	    type: 'POST',
	    data: JSON.stringify(row),
	    contentType: 'application/json',
	    success: function(html) {
	        $("#center").html(html);
	        $('#center').show();
	    }
	}); 
}

function loadLeftPage(url, center, title){
	hidePage();
	$('#left').load('loadPage/'+url);
	$('#left').show();
	if(center!=''){
		$('#center').load('loadPage/'+center);
		$('#center').show();
	}
	if(title!=null){
		$('#gnb_title').html(null);
		$('#gnb_title').html(title);
	}
}

function wrapWindowByMask(){
	//화면의 높이와 너비를 구한다.
	var maskHeight = $(document).height();
	var maskWidth = $(window).width();

	//마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
	$('#ajax_load_indicator').css({'width':maskWidth,'height':maskHeight});
	$('#ajax_load_indicator').fadeTo("slow",0.6);

}

function showProgress(){
	wrapWindowByMask();
	 $("#loadingImg").show();
}

function hideProgress(){
	$('#ajax_load_indicator').hide();
	$("#loadingImg").hide();
}

function drawSelect(obj, items, options){
	obj.empty();
	switch(options){
	case 'meta':
		obj.append($('<option>', {
		    tag: '',
		    text: '선택'
		}));
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
		        tag: item.CD_TP_MEANING+' / '+item.CD_V_EXPLAIN,
		        text : item.CD_TP1 
		    }));
		});
		break;
	case 'company':
		obj.append($('<option>', {
		    value:'00',
		    text: '전체'
		}));
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
		        value: item.CD_TP,
		        text : item.CD_TP+'('+item.CD_TP_MEANING+')' 
		    }));
		});
		break;
	case 'commonCode':
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
		        value: item.CD_TP,
		        text : item.CD_TP_NM 
		    }));
		});
		break;
	case 'commonCodeAll':
		obj.append($('<option>', {
		    value:'',
		    text: '전체'
		}));
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
		        value: item.CD_TP,
		        text : item.CD_TP_NM 
		    }));
		});
		break;
	case 'hostAll':
		var all='';
		$.each(items, function (i, item) {
			all += item.KEY + '|';
			obj.append($('<option>', { 
		        value: item.KEY,
		        text : item.KEY 
		    }));
		});
		all = all.substr(0, all.length-1); 
		obj.prepend($('<option>', {
		    value:all,
		    text: '전체'
		}));
		obj.find("option:contains('전체')").prop('selected', 'selected');
		break;
	case 'hostAll2':
		var all='';
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
		        value: item.KEY,
		        text : item.KEY 
		    }));
		});
		obj.prepend($('<option>', {
		    value:'',
		    text: '전체'
		}));
		obj.find("option:contains('전체')").prop('selected', 'selected');
		break;
	case 'selCode':
		obj.append($('<option>', {
		    text: '선택'
		}));
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
				value: item.KEY,
		        text : item.KEY 
		    }));
		});
		break;
	case 'conf':
		obj.append($('<option>', {
		    text: '선택'
		}));
		$.each(items, function (i, item) {
			obj.append($('<option>', { 
				value: i,
		        text : item 
		    }));
		});
		break;
	case 'tns':
		obj.append($('<option>', {
			value: '',
		    text: '선택'
		}));
		$.each(items, function (i, item) {
			var url = item['feed.db.url'].split('@')[1];
			if(url==undefined)
				url = item['feed.db.url'].split('//')[1];
			url = url.length<40 
					? url 
					: url.split('HOST=')[1].split(')')[0] 
						+ ':' + url.split('PORT=')[1].split(')')[0]
						+ ':' + url.split('SERVICE_NAME=')[1].split(')')[0];
			obj.append($('<option>', { 
				value: item['feed.db.driver']+','+item['feed.db.url']+','+item['feed.db.user']+','+item['feed.db.pwd'],		
		        text : item.id +' ('+ url +', '+item['feed.db.user']+')'
		    }));
		});
		break;
	case 'ela_ip':
		$.each(items, function (i, item) {
			var option = { 
					value: item.CD_TP,
			        text : item.CD_V_EXPLAIN + '(' + item.CD_TP_MEANING + ')' 
			    }; 
			if(item.ACTIVE_FLAG=='Y')
				option.selected = true;
			obj.append($('<option>', option));
		});
		break;
	}
}

//http url을 호출하여 가동계 xml데이타를 조회한다. 
function getConfigDataAsJson(){
	var params = {};
	params['url'] = $('#tns_info').val();
	 $.ajax({
	 type : 'POST',
	         url:'getConfigDataAsJson',
	         data : JSON.stringify(params),
	         contentType: 'application/json',
	         dataType: 'json',
	         async : false,
	         success:function(data){
	        	 var obj = $('#sel_host')
	        	 var json = data.result.feed.system;
	        	 drawSelect(obj, json, 'tns');
	        },
	        error : function(e){ 
	        }
     });
}


/*검색엔진에서 서버구분, 서버환경, 호스트값을 선택하는 selectbox 생성
 * @param objnm :  select box id값
 * @param seltype : selectbox에 표시할 값의 종류.SERVER_TYPE(CONNECTOR/WAS/검색엔진),INFRA_TYPE(가동계/개발계/테스트계),HOST_NAME(DLCESA01/PLCEMASA1....)
 * @param servertypeval : 검색쿼리 조건절에 SERVER_TYPE의 값으로 셋팅함
 * @param infratypeval : 검색쿼리 조건절에 INFRA_TYPE의 값으로 셋팅함
 * @param hosttypeval : 검색쿼리 조건절에 HOST_NAME의 값으로 셋팅함
 * @param drawSelectOption :selectbox를 그리기위해  drawSelect()호출할때 options값으로 셋팅함.
 **/
function selectCodeType(objnm, seltype, servertypeval, infratypeval, hosttypeval, drawSelectOption ){
	var params = {};
	params['EVENT_ID'] = 'getCodeList';
	params['P_SERVER_TYPE'] = servertypeval;
	params['P_INFRA_TYPE'] = infratypeval;
	params['P_HOST_NAME'] = hosttypeval;
	params['P_SEL_CODE_TYPE'] = seltype;
	
	$.ajax({
		type : 'POST',
        url:'getCodeList',
        data : JSON.stringify(params),
        dataType:'json',
        contentType: 'application/json',
        success:function(data){
        	var obj = $('#'+objnm);
        	
    		drawSelect(obj, data, drawSelectOption);
        },
        error : function(e){ 
        }
     });
}

/*
 * 검색엔진 모니터링 용 함수
 * */
var time_interval=null;
var time_node_interval=null;
var time_indices_interval = null;

function search_engine_start(){
    if (time_interval){
        clearInterval(time_interval);
        time_interval = null;
        //console.log('clear');
    	}
    
    if (time_node_interval){
        clearInterval(time_node_interval);
        time_node_interval = null;
        //console.log('clear');
    	}
    
//    if (time_indices_interval){
//        clearInterval(time_indices_interval);
//        time_indices_interval = null;
//        //console.log('clear');
//    	}
    
    if( typeof search_engine_status == 'function' ) {
				time_interval=setInterval(function(){
			    	search_engine_status(''); 
			    },10000);
				document.getElementById("butt_start").innerHTML='<span class="ui-icon ui-icon-play">Restart</span>Restart';

    	}
    if (typeof show_table_make == 'function' ) {
    	time_node_interval=setInterval(function(){
	    		show_table_make(''); 
	    		},10000);
	      document.getElementById("butt_start").innerHTML='<span class="ui-icon ui-icon-play">Restart</span>Restart';
    	}
    
//    if (typeof make_indices_table == 'function' ) {
//    	time_indices_interval=setInterval(function(){
//    		make_indices_table(''); 
//	    		},10000);
//	      document.getElementById("butt_start").innerHTML='<span class="ui-icon ui-icon-play">Restart</span>Restart';
//    	}
}

function search_engine_stop(){
    if (time_interval){
        clearInterval(time_interval);
        time_interval = null;
    	}
    
    if (time_node_interval){
        clearInterval(time_node_interval);
        time_node_interval = null;
    	}
    
//    if (time_indices_interval){
//        clearInterval(time_indices_interval);
//        time_indices_interval = null;
//        //console.log('clear');
//    	}
}


//application.yml의 DB설정을 조회하여 가동계/개발계를 구분하여 표시함.
function getApplicationTask(){
	 $.ajax({
	 type : 'POST',
	         url:'applicationTask',
	         async : false,
	         success:function(result){
	        	 console.log(result);
	        	 if(result.indexOf('prd')>-1){
	        		 $('#taskName').text('(가동계)');
	        	 }
	        	 else{
	        		 $('#taskName').text('(개발계)');
	        	 }
	        	 
	        },
	        error : function(e){ 
	        }
     });
}























