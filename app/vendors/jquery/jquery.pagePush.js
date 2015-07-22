(function ( $ ) {
 
    $.pagePush = function( options ) {
 
        // This is the easiest way to have default options.
        var settings = $.extend({
            // These are the defaults.
            buttonLeft : "dd-filter",
            buttonRight : "dd-preferences",
            container : "flight-window",
            body : "body",
            direction1 : "push-toleft",
            direction2 : "push-toright",
            classAction : 'active'
        }, options );
 
        // When click outside buttons preferences/filter
        $('#'+settings.container).on('click', function(e) {
            if (!$('#'+settings.buttonRight+',#'+settings.buttonLeft).has(e.target).length &&
                    e.target.id !== settings.buttonLeft &&
                    e.target.id !== settings.buttonRight && 
                    !$('nav.cbp-spmenu').has(e.target).length){
                $('#'+settings.buttonLeft).removeClass(settings.classAction);
                $('#'+settings.buttonRight).removeClass(settings.classAction);
                $('body,#navigation').removeClass(settings.direction1 +' '+settings.direction2);
            }
        });

        // Push menu by right
        $('#'+settings.buttonRight).on('click', function(e) {
            $('body,#navigation').removeClass(settings.direction1 +' '+settings.direction2);
            $('#'+settings.buttonLeft).removeClass(settings.classAction);
            if($(this).hasClass(settings.classAction)){
                $('#'+settings.buttonRight).toggleClass(settings.classAction);
            }else{
                $('body').addClass(settings.direction1);
                $('#navigation').toggleClass(settings.direction2);
                $('#'+settings.buttonRight).addClass(settings.classAction);
            }
        });


        // Push menu by left
        $('#'+settings.buttonLeft).on('click', function(e) {
            $('body,#navigation').removeClass(settings.direction1 +' '+settings.direction2);
            $('#'+settings.buttonRight).removeClass(settings.classAction);
            if($(this).hasClass(settings.classAction)){
                $('#'+settings.buttonLeft).toggleClass(settings.classAction);
            }else{
                $('body').addClass(settings.direction2);
                $('#navigation').toggleClass(settings.direction1);
                $('#'+settings.buttonLeft).addClass(settings.classAction);
            }
        });
        $('h4').on('click',function(){
            if ($(window).height()< 600 ){
                $(this).parent().siblings().children('div').removeClass('active').addClass('inactive');
                $(this).parent().siblings().children('h4').children('i').removeClass('icon-angle-down').addClass('icon-angle-right');
                $(this).siblings().toggleClass('inactive active');
                $(this).children('i').toggleClass('icon-angle-down icon-angle-right');
            }else{
                $(this).siblings('div').toggleClass('inactive active');
                $(this).children('i').toggleClass('icon-angle-down icon-angle-right');
            }
        });
 
    };
 
}( jQuery ));

$.pagePush();