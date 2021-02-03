$(function() {
	var menuLink = $('.menu-link');
	var menu = $('menu');
	var close = $('.close-btn');
	var navLink = $('li a');

	menuLink.click(function() {
		menu.toggleClass('active-menu');
	});
	close.click(function() {
		menu.toggleClass('active-menu');
	});

	navLink.on('click', function(event) {
		event.preventDefault();
		var target = $(this).attr('href');
		var top = $(target).offset().top;
		$('html,body').animate({scrollTop: top}, 500)
	});
});