$(document).ready(function () {


// Kredi kart işlemleri  || Billing Profile
    var stripeFormModule = $(".stripe-payment-form")
    var stripeToken = stripeFormModule.attr("data-token")
    var stripeNextUrl = stripeFormModule.attr("data-next-url")
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card"
    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
        publishKey: stripeToken,
        nextUrl: stripeNextUrl,
        btnTitle: stripeModuleBtnTitle
    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)


    var paymentForm = $(".payment-form");
    if (paymentForm.length > 1) {
        alert("Only one payment form is allowed per page");
        paymentForm.css("display", "none")
    } else if (paymentForm.length == 1) {

        var pubKey = paymentForm.attr("data-token");
        var nextUrl = paymentForm.attr("data-next-url");

        var stripe = Stripe(pubKey);

        var elements = stripe.elements();

        var style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };

        var card = elements.create('card', {style: style});

        card.mount('#card-element');

        card.addEventListener('change', function (event) {
            var displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });



        function redirectToNext(nextPath, timeoffset) {
            if (nextPath) {
                setTimeout(function () {
                    window.location.href = nextPath
                }, timeoffset)
            }
        }

        var form = $('#payment-form');
        var btnLoad = form.find(".btn-load");
        var btnLoadDefaultHtml = btnLoad.html();
        var btnLoadDefaultClasses = btnLoad.attr("class");
        form.on('submit', function (event) {
            event.preventDefault();

            var $this = $(this)
            btnLoad.blur()
            var loadtime = 1000
            var currentTimeout;
            var errorHtml = "<i class='fa fa-warning'></i> Bir hata oluştu"
            var errorClasses = "btn btn-danger my-4 disabled"
            var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
            var loadingClasses = "btn btn-success my-4 disabled"

            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    var errorElement = $('#card-errors');
                    errorElement.textContent = result.error.message;
                    currentTimeout = displayBtnStatus(btnLoad, errorHtml, errorClasses, loadtime, currentTimeout)
                } else {
                    currentTimeout = displayBtnStatus(btnLoad, loadingHtml, loadingClasses, loadtime, currentTimeout)
                    stripeTokenHandler(nextUrl, result.token);
                }
            });
        });


        // Kart bilgileri ekleme  buton durumu
        function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout) {

            if (!loadTime) {
                loadTime = 1500
            }
            element.html(newHtml)
            element.removeClass(btnLoadDefaultClasses)
            element.addClass(newClasses)

            return setTimeout(function () {
                element.html(btnLoadDefaultHtml)
                element.removeClass(newClasses)
                element.addClass(btnLoadDefaultClasses)
            }, loadTime)
        }


        function stripeTokenHandler(nextUrl, token) {
            var paymentMethodEndpoint = "/billing/payment-method/create/";
            var data = {
                'token': token.id
            };
            $.ajax({
                data: data,
                url: paymentMethodEndpoint,
                method: "POST",
                success: function (data) {
                    var succesMsg = data.message || "Success! Your card was added.";
                    card.clear();
                    if (nextUrl) {
                        succesMsg += "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirect..."
                    }
                    if ($.alert) {
                        $.alert(succesMsg);
                    } else {
                        alert(succesMsg);
                    }
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr("class", btnLoadDefaultClasses)
                    redirectToNext(nextUrl, 1500)
                },
                error: function (error) {
                    $.alert({title: "Bir hata oluştu", content: "Lütfen kart bilgilerinizi girmeyi tekrar deneyiniz."})
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr("class", btnLoadDefaultClasses)
                }
            });

        }

    }
})