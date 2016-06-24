
(function($) {

/*---------------------------
 Defaults for Reveal
----------------------------*/
     
/*---------------------------
 Listener for data-reveal-id attributes
----------------------------*/

 //a啥意思？
    //获取hostname
    $(document).on('click', 'a[data-reveal-id]',function(e) {
        e.preventDefault(); //该方法将通知 Web 浏览器不要执行与事件关联的默认动作
        var modalLocation = $(this).attr('data-reveal-id');
        $('#'+modalLocation).reveal($(this).data());
        // $("#hostname1").html($(this).attr('data-test'));
        var data = table.row( $(this).parents('tr') ).data();
        //alert(hostname2)
        //$("#hostname1").html($(this).attr('data-test') + "<img src=http://115.28.203.116/zabbix/chart2.php?graphid=6542&period=23234&width=800& />");
        gethostname(data.fields.hostname);

    });


    function gethostname(hostname2){
      $.getJSON('/ajax_list/',{'hostname2':hostname2},function(data){
        //var jsonobj=$.parseJSON('{"model": "CMDB.iterms", "pk": 53, "fields": {"hostid": 10125, "hostname": "nginx-asp006", "cpu_itemid": 24891.0, "cpu_graphs_itemsid": 845, "eth0_graphs_itemsid": 1015, "eth1_graphs_itemsid": 1016}}');
       // alert(data);
        hostname = data[0].fields.hostname;
        cpu_graphs_itemsid = data[0].fields.cpu_graphs_itemsid;
        eth1_graphs_itemsid = data[0].fields.eth1_graphs_itemsid;
        //alert(hostname)
       $("#hostname1").html( "<img src=http://115.28.203.116/zabbix/chart2.php?graphid="+cpu_graphs_itemsid+"&period=23234&width=800& /> ");
      });
    }

/*---------------------------
 Extend and Execute
----------------------------*/

    $.fn.reveal = function(options) {
        
        
        var defaults = {  
            animation: 'fadeAndPop', //fade, fadeAndPop, none
            animationspeed: 300, //how fast animtions are
            closeonbackgroundclick: true, //if you click background will modal close?
            dismissmodalclass: 'close-reveal-modal' //the class of a button or element that will close an open modal
        }; 
        
        //Extend dem' options
        var options = $.extend({}, defaults, options); 
    
        return this.each(function() {
        
/*---------------------------
 Global Variables
----------------------------*/
            var modal = $(this),
                topMeasure  = parseInt(modal.css('top')),
                topOffset = modal.height() + topMeasure,
                locked = false,
                modalBG = $('.reveal-modal-bg');

/*---------------------------
 Create Modal BG
----------------------------*/
            if(modalBG.length == 0) {
                modalBG = $('<div class="reveal-modal-bg" />').insertAfter(modal);
            }           
     
/*---------------------------
 Open & Close Animations
----------------------------*/
            //Entrance Animations
            modal.bind('reveal:open', function () {
              modalBG.unbind('click.modalEvent');
                $('.' + options.dismissmodalclass).unbind('click.modalEvent');
                if(!locked) {
                    lockModal();
                    if(options.animation == "fadeAndPop") {
                        modal.css({'top': $(document).scrollTop()-topOffset, 'opacity' : 0, 'visibility' : 'visible'});
                        modalBG.fadeIn(options.animationspeed/2);
                        modal.delay(options.animationspeed/2).animate({
                            "top": $(document).scrollTop()+topMeasure + 'px',
                            "opacity" : 1
                        }, options.animationspeed,unlockModal());                   
                    }
                    if(options.animation == "fade") {
                        modal.css({'opacity' : 0, 'visibility' : 'visible', 'top': $(document).scrollTop()+topMeasure});
                        modalBG.fadeIn(options.animationspeed/2);
                        modal.delay(options.animationspeed/2).animate({
                            "opacity" : 1
                        }, options.animationspeed,unlockModal());                   
                    } 
                    if(options.animation == "none") {
                        modal.css({'visibility' : 'visible', 'top':$(document).scrollTop()+topMeasure});
                        modalBG.css({"display":"block"});   
                        unlockModal()               
                    }
                }
                modal.unbind('reveal:open');
            });     

            //Closing Animation
            modal.bind('reveal:close', function () {
              if(!locked) {
                    lockModal();
                    if(options.animation == "fadeAndPop") {
                        modalBG.delay(options.animationspeed).fadeOut(options.animationspeed);
                        modal.animate({
                            "top":  $(document).scrollTop()-topOffset + 'px',
                            "opacity" : 0
                        }, options.animationspeed/2, function() {
                            modal.css({'top':topMeasure, 'opacity' : 1, 'visibility' : 'hidden'});
                            unlockModal();
                        });                 
                    }   
                    if(options.animation == "fade") {
                        modalBG.delay(options.animationspeed).fadeOut(options.animationspeed);
                        modal.animate({
                            "opacity" : 0
                        }, options.animationspeed, function() {
                            modal.css({'opacity' : 1, 'visibility' : 'hidden', 'top' : topMeasure});
                            unlockModal();
                        });                 
                    }   
                    if(options.animation == "none") {
                        modal.css({'visibility' : 'hidden', 'top' : topMeasure});
                        modalBG.css({'display' : 'none'});  
                    }       
                }
                modal.unbind('reveal:close');
            });     
    
/*---------------------------
 Open and add Closing Listeners
----------------------------*/
            //Open Modal Immediately
        modal.trigger('reveal:open')
            
            //Close Modal Listeners
            var closeButton = $('.' + options.dismissmodalclass).bind('click.modalEvent', function () {
              modal.trigger('reveal:close')
            });
            
            if(options.closeonbackgroundclick) {
                modalBG.css({"cursor":"pointer"})
                modalBG.bind('click.modalEvent', function () {
                  modal.trigger('reveal:close')
                });
            }
            $('body').keyup(function(e) {
                if(e.which===27){ modal.trigger('reveal:close'); } // 27 is the keycode for the Escape key
            });
            
            
/*---------------------------
 Animations Locks
----------------------------*/
            function unlockModal() { 
                locked = false;
            }
            function lockModal() {
                locked = true;
            }   
            
        });//each call
    }//orbit plugin call
})(jQuery);
        