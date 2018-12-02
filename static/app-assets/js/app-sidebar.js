/*!
 =========================================================
 * Apex Angular 4 Bootstrap theme - V1.0
 =========================================================

 * Product Page: https://www.pixinvent.com/product/apex
 * Copyright 2017 Pixinvent Creative Studio (https://www.pixinvent.com)

 =========================================================
*/
 $(document).ready( function(){


    var $sidebar = $('.app-sidebar'),
    $sidebar_content = $('.sidebar-content'),
    $sidebar_img = $sidebar.data('image'),
    $sidebar_img_container = $('.sidebar-background'),
    $wrapper = $('.wrapper');

    // $sidebar_content.perfectScrollbar();


    if( $sidebar_img_container.length !== 0 && $sidebar_img !== undefined ){
        $sidebar_img_container.css('background-image','url("' + $sidebar_img + '")');
    }

    // if(!$wrapper.hasClass('nav-collapsed')){
    //     $sidebar_content.find('li.active').parents('li').addClass('open');
    //     console.log('collapse2');
    // }


    // Match the height of each card in a row
    setTimeout(function(){
        $('.row.match-height').each(function() {
            $(this).find('.card').not('.card .card').matchHeight(); // Not .card .card prevents collapsible cards from taking height
        });
    },500);


    // $sidebar_content.on('click', '.navigation li a',function(){
    //     var $this = $(this),
    //     listItem = $this.parent('li');
    //
    //     if(listItem.hasClass('has-sub') && listItem.hasClass('open')){
    //         collapse(listItem);
    //         console.log('collapse3');
    //     }
    //     else{
    //         if(listItem.hasClass('has-sub')){
    //             expand(listItem);
    //         }
    //
    //         // If menu collapsible then do not take any action
    //         if ($sidebar_content.data('collapsible')) {
    //             return false;
    //         }
    //         // If menu accordion then close all except clicked once
    //         else {
    //             openListItems = listItem.siblings('.open');
    //             collapse(openListItems);
    //             console.log('collapse4');
    //             listItem.siblings('.open').find('li.open').removeClass('open');
    //             console.log('collapse5');
    //
    //         }
    //     }
    // });

    // function collapse($listItem, callback) {
    //     var $subList = $listItem.children('ul');
    //
    //     $subList.show().slideUp(200, function() {
    //         $(this).css('display', '');
    //
    //         $(this).find('> li').removeClass('is-shown');
    //
    //         $listItem.removeClass('open');
    //         console.log('collapse6');
    //
    //         if (callback) {
    //             callback();
    //         }
    //     });
    //
    // }

    // function expand($listItem, callback) {
    //     var $subList = $listItem.children('ul');
    //     var $children = $subList.children('li').addClass('is-hidden');
    //
    //     $listItem.addClass('open');
    //     console.log('collapse7');
    //
    //     $subList.hide().slideDown(200, function() {
    //         $(this).css('display', '');
    //
    //         if (callback) {
    //             callback();
    //         }
    //     });
    //
    //
    //
    //     setTimeout(function() {
    //         $children.addClass('is-shown');
    //         $children.removeClass('is-hidden');
    //     }, 0);
    // }

    // $('.logo-text').on('click',function(){
    //
    //     var listItem = $sidebar_content.find('li.open.has-sub'),
    //         console.log('collapse');
    //     activeItem = $sidebar_content.find('li.active');
    //
    //     if(listItem.hasClass('has-sub') && listItem.hasClass('open')){
    //         collapse(listItem);
    //         console.log('collapse');
    //         listItem.removeClass('open');
    //         if(activeItem.closest('li.has-sub')){
    //             openItem = activeItem.closest('li.has-sub');
    //             expand(openItem);
    //             openItem.addClass('open');
    //         }
    //     }
    //     else{
    //         if(activeItem.closest('li.has-sub')){
    //             openItem = activeItem.closest('li.has-sub');
    //             expand(openItem);
    //             openItem.addClass('open');
    //             console.log('collapse');
    //         }
    //     }
    // });
       var $this = $(this),
           toggle_icon= $this.find('.toggle-icon');
           //toggle = toggle_icon.attr('data-toggle');
       var datatoggle = localStorage.getItem('toggle');

            if (datatoggle == "expanded") {
                console.log(2);
                $('.nav-toggle').find('.toggle-icon').addClass('ft-toggle-right').removeClass('ft-toggle-left');
            toggle_icon.attr('data-toggle', 'expanded');
            $('#logo2').show();
            }
            else {
            $wrapper.addClass('nav-collapsed menu-collapsed');
            $('.nav-toggle').find('.toggle-icon').removeClass('ft-toggle-right').addClass('ft-toggle-left');
            toggle_icon.attr('data-toggle', 'collapsed');
            $('#logo2').hide();

            }


    $('.nav-toggle').on('click',function(){
        var $this = $(this),
         toggle_icon= $this.find('.toggle-icon'),
            toggle = toggle_icon.attr('data-toggle');
        compact_menu_checkbox = $('.cz-compact-menu');

        if(toggle === 'expanded'){
            $wrapper.addClass('nav-collapsed');
            // localStorage.setItem('data-toggle', 'expanded');
            $('.nav-toggle').find('.toggle-icon').removeClass('ft-toggle-right').addClass('ft-toggle-left');
            toggle_icon.attr('data-toggle', 'collapsed');
            if(compact_menu_checkbox.length > 0){
                compact_menu_checkbox.prop('checked',true);
            }
        }
        else{
            $wrapper.removeClass('nav-collapsed menu-collapsed');
            // localStorage.setItem('data-toggle', 'collapsed');
            $('.nav-toggle').find('.toggle-icon').removeClass('ft-toggle-left').addClass('ft-toggle-right');
            toggle_icon.attr('data-toggle', 'expanded');
            if(compact_menu_checkbox.length > 0){
                compact_menu_checkbox.prop('checked',false);
            }
        }
        toggle = toggle_icon.attr('data-toggle')
        localStorage.setItem('toggle', toggle);

    });

    $sidebar.on('mouseenter', function() {
        if($wrapper.hasClass('nav-collapsed')){
            $wrapper.removeClass('menu-collapsed');
            $('#logo2').show();
            var $listItem = $('.navigation li.nav-collapsed-open'),
            $subList = $listItem.children('ul');
            console.log('collapse8');

            $subList.hide().slideDown(300, function() {
                $(this).css('display', '');
            });

            $sidebar_content.find('li.active').parents('li').addClass('open');
            $listItem.addClass('open').removeClass('nav-collapsed-open');
            console.log('collapse');
        }
    }).on('mouseleave', function(event) {
        if($wrapper.hasClass('nav-collapsed')){
            $wrapper.addClass('menu-collapsed');
            $('#logo2').hide();
            var $listItem = $('.navigation li.open'),
            $subList = $listItem.children('ul');
            $listItem.addClass('nav-collapsed-open');
            console.log('collapse1');

            $subList.show().slideUp(300, function() {
                $(this).css('display', '');
            });

            $listItem.removeClass('open');
        }
    });

    if ($(window).width() < 992) {
        $sidebar.addClass('hide-sidebar');
        $wrapper.removeClass('nav-collapsed menu-collapsed');
    }
    $( window ).resize(function() {
        if ($(window).width() < 992) {
            $sidebar.addClass('hide-sidebar');
            $wrapper.removeClass('nav-collapsed menu-collapsed');
        }
        if ($(window).width() > 992) {
            $sidebar.removeClass('hide-sidebar');
            if( $('.toggle-icon').attr('data-toggle') === 'collapsed' &&  $wrapper.not('.nav-collapsed menu-collapsed')){
                $wrapper.addClass('nav-collapsed menu-collapsed');
                $('#logo2').hide();
            }
        }
    });

    $(document).on('click', '.navigation li:not(.has-sub)', function(){
        if( $(window).width() < 992 ){
            $sidebar.addClass('hide-sidebar');
        }
    });

    $(document).on('click', '.logo-text', function(){
        if( $(window).width() < 992 ){
            $sidebar.addClass('hide-sidebar');
        }
    });


    $('.navbar-toggle').on('click',function(e){
        e.stopPropagation();
        $sidebar.toggleClass('hide-sidebar');
    });

    $('html').on('click', function (e) {
        if ($(window).width() < 992) {
            if (!$sidebar.hasClass('hide-sidebar') && $sidebar.has(e.target).length === 0) {
                $sidebar.addClass('hide-sidebar');
            }
        }
    });

    $('#sidebarClose').on('click', function(){
        $sidebar.addClass('hide-sidebar');
    });

    // $('.noti-list').perfectScrollbar();


    // Page full screen
    $('.apptogglefullscreen').on('click', function(e) {
        if (typeof screenfull != 'undefined'){
            if (screenfull.enabled) {
                screenfull.toggle();
            }
        }
    });
    if (typeof screenfull != 'undefined'){
        if (screenfull.enabled) {
            $(document).on(screenfull.raw.fullscreenchange, function(){
                if(screenfull.isFullscreen){
                    $('.apptogglefullscreen').find('i').toggleClass('ft-minimize ft-maximize');
                }
                else{
                    $('.apptogglefullscreen').find('i').toggleClass('ft-maximize ft-minimize');
                }
            });
        }
    }

    $('#hamburger').click(function () {
        $('#logo2').show();
    });

});