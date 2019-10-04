$(document).ready(function () {

    // İletişim Formu
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")


    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled")
            submitBtn.html('<i class="fa fa-spinner" aria-hidden="true"></i> Sending...')
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.text(defaultText)
        }
    }

    contactForm.submit(function (event) {

        event.preventDefault()
        var formData = contactForm.serialize()
        var submitBtn = contactForm.find("[type='submit'")
        var submitBtnTxt = submitBtn.text()

        displaySubmitting(submitBtn, "", true)
        $.ajax({
            url: contactFormEndpoint,
            method: contactFormMethod,
            data: formData,
            success: function (data) {
                contactForm[0].reset()
                $.alert({
                    'title': "Success",
                    'content': data.message,
                    'theme': "modern"
                })
                setTimeout(function () {
                    displaySubmitting(submitBtn, submitBtnTxt, false)
                }, 500)

            },
            error: function (error) {
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function (key, value) {
                    msg += key + " : " + value[0].message + "<br/>"
                })

                //Eklenti
                $.alert({
                    'title': "Opps!",
                    'content': msg,
                    'theme': "modern"
                })
                setTimeout(function () {
                    displaySubmitting(submitBtn, submitBtnTxt, false)
                }, 500)
            }
        })

    })


    // ********************************************************************************

    //Arama İşlemleri
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typeingTimer;
    var typingInterval = 1500
    var searchBtn = searchForm.find("[type='submit'")

    // elini tuştan kaldırdığında
    searchInput.keyup(function (event) {
        clearTimeout(typeingTimer)
        typeingTimer = setTimeout(perfomSearch, typingInterval)
    })

    //tuşa basıldığında
    searchInput.keydown(function (event) {
        clearTimeout(typeingTimer)
    })

    function displaySearching() {
        searchBtn.addClass("disabled")
        searchBtn.html('<i class="fa fa-spinner" aria-hidden="true"></i> Searching...')
    }

    function perfomSearch() {
        displaySearching()
        var query = searchInput.val()
        setTimeout(function () {
            window.location.href = "/search/?q=" + query

        }, 1000)
    }

    // ********************************************************************************//

    // Sepet güncelleme,sepete ekleme,çıkarma işlemleri
    var productForm = $(".form-product-ajax")
    productForm.submit(function (event) {
        event.preventDefault();
        var thisForm = $(this)
        //var actionEnpoint = thisForm.attr("action")
        var httpMethod = thisForm.attr("method")
        var actionEndPoint = thisForm.attr("data-endpoint")
        var formData = thisForm.serialize();
        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function (data) {

                //Ürün detay için sepete ekle çıkar butonunu değiştirme
                var submitSpan = thisForm.find(".submit-span")
                if (data.added) {
                    submitSpan.html('In Cart <button type="submit" class="btn btn-link">Remove</button>')
                } else {
                    submitSpan.html(' <button type="submit" class="btn btn-success">Add to Cart</button>')
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount) // Sepetteki ürün sayısını değiştirme
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()   //Sepetimdeki ürünleri güncelleme
                }
            },
            error: function (errorData) {

                //  https://craftpip.github.io/jquery-confirm/#getting-started
                // Jquery Confirm
                $.alert({

                    'title': "Opps!",
                    'content': "Bir hata oluştu!",
                    'theme': "modern"

                })
            }

        })
    })

    //Sepetimdeki ürünleri güncelleme
    function refreshCart() {
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        var productRows = cartTable.find(".cart-product")
        var currentUrl = window.location.href
        var refreshCartUrl = "/api/cart/";
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {

                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

                if (data.products.length > 0) {
                    productRows.html("")
                    var i = 0
                    $.each(data.products, function (index, value) {
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend('<tr><th scope="row">' + (data.products.length - i) + '</th><td> <a href="' + value.url + '">{{ value.name }}' + value.name + '</a>' + newCartItemRemove.html() + '</td><td >' + value.price + '</td></tr>')
                        i++
                    })


                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)

                } else {
                    window.location.href = currentUrl
                }

            },
            error: function (error) {
                //  https://craftpip.github.io/jquery-confirm/#getting-started
                // Jquery Confirm
                $.alert({
                    'title': "Opps!",
                    'content': "Bir hata oluştu!",
                    'theme': "modern"
                })

            }


        })


    }


})
