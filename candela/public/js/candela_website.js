/**
 * Candela — Luxury Restaurant Website JS
 * Navbar scroll, mobile nav, smooth scroll, toast, API, newsletter
 */
(function() {
	'use strict';

	window.candela = window.candela || {};

	document.addEventListener('DOMContentLoaded', function() {
		candela.initNavbar();
		candela.initMobileNav();
		candela.initSmoothScroll();
		candela.initReveal();
		candela.initNewsletter();
	});

	/* ── Navbar scroll effect ──────────────────────────────────── */
	candela.initNavbar = function() {
		var navbar = document.querySelector('.candela-navbar');
		if (!navbar) return;
		var threshold = 60;
		var ticking = false;

		function onScroll() {
			if (!ticking) {
				requestAnimationFrame(function() {
					navbar.classList.toggle('scrolled', window.scrollY > threshold);
					ticking = false;
				});
				ticking = true;
			}
		}
		window.addEventListener('scroll', onScroll, { passive: true });
		onScroll();
	};

	/* ── Mobile nav toggle ─────────────────────────────────────── */
	candela.initMobileNav = function() {
		var toggle = document.querySelector('.candela-navbar__toggle');
		var nav = document.querySelector('.candela-navbar__nav');
		if (!toggle || !nav) return;

		toggle.addEventListener('click', function() {
			var open = nav.classList.toggle('open');
			toggle.classList.toggle('active', open);
			toggle.setAttribute('aria-expanded', open);
			document.body.style.overflow = open ? 'hidden' : '';
		});

		nav.querySelectorAll('.candela-navbar__link, .c-btn').forEach(function(link) {
			link.addEventListener('click', function() {
				nav.classList.remove('open');
				toggle.classList.remove('active');
				toggle.setAttribute('aria-expanded', 'false');
				document.body.style.overflow = '';
			});
		});
	};

	/* ── Smooth scroll ─────────────────────────────────────────── */
	candela.initSmoothScroll = function() {
		document.querySelectorAll('a[href^="#"]').forEach(function(link) {
			link.addEventListener('click', function(e) {
				var target = document.querySelector(this.getAttribute('href'));
				if (target) {
					e.preventDefault();
					var offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--navbar-h')) || 80;
					window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - offset - 20, behavior: 'smooth' });
				}
			});
		});
	};

	/* ── Scroll reveal with IntersectionObserver ───────────────── */
	candela.initReveal = function() {
		var reveals = document.querySelectorAll('.c-reveal');
		if (!reveals.length) return;

		if ('IntersectionObserver' in window) {
			var observer = new IntersectionObserver(function(entries) {
				entries.forEach(function(entry) {
					if (entry.isIntersecting) {
						entry.target.classList.add('visible');
						observer.unobserve(entry.target);
					}
				});
			}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

			reveals.forEach(function(el) { observer.observe(el); });
		} else {
			reveals.forEach(function(el) { el.classList.add('visible'); });
		}
	};

	/* ── Newsletter ────────────────────────────────────────────── */
	candela.initNewsletter = function() {
		document.querySelectorAll('.c-newsletter-form').forEach(function(form) {
			form.addEventListener('submit', function(e) {
				e.preventDefault();
				var input = form.querySelector('input[type="email"]');
				if (!input || !input.value) return;
				var btn = form.querySelector('button');
				if (btn) btn.disabled = true;

				candela.api('candela.api.subscribe_newsletter', { email: input.value })
					.then(function(r) {
						if (r.message && r.message.success) {
							candela.toast(r.message.message, 'success');
							input.value = '';
						}
					})
					.catch(function() { candela.toast('Something went wrong.', 'error'); })
					.finally(function() { if (btn) btn.disabled = false; });
			});
		});
	};

	/* ── API helper ────────────────────────────────────────────── */
	candela.api = function(method, args) {
		return fetch('/api/method/' + method, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': candela.getCSRFToken() },
			body: JSON.stringify(args || {})
		}).then(function(res) {
			if (!res.ok) throw new Error('API error');
			return res.json();
		});
	};

	candela.getCSRFToken = function() {
		var meta = document.querySelector('meta[name="csrf_token"]');
		return meta ? meta.getAttribute('content') : '';
	};

	/* ── Toast ─────────────────────────────────────────────────── */
	candela.toast = function(message, type) {
		type = type || 'info';
		var toast = document.createElement('div');
		toast.className = 'c-toast c-toast--' + type;
		toast.textContent = message;
		document.body.appendChild(toast);
		requestAnimationFrame(function() { toast.classList.add('show'); });
		setTimeout(function() {
			toast.classList.remove('show');
			setTimeout(function() { toast.remove(); }, 400);
		}, 4000);
	};

	/* ── Form helpers ──────────────────────────────────────────── */
	candela.submitReservation = function(data) { return candela.api('candela.api.submit_reservation', data); };
	candela.submitReview = function(data) { return candela.api('candela.api.submit_review', data); };
})();
