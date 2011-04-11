$(function() {
    updater.poll();
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var updater = {
    errorSleepTime: 500,
    currentImage: '',
    colCount: 0,
    makeItStop: null,

    poll: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        $.ajax({url: "/updates", type: "POST", dataType: "text",
                data: $.param(args),
                success: updater.onSuccess,
                error: updater.onErr});
    },

    onSuccess: function(response) {
        try {
            updater.newImage(eval("(" + response + ")"));
        } catch (e) {
            console.log("EXCEPTION in onSuccess");
            return;
        }
        updater.errorSleepTime = 500;
        updater.makeItStop = window.setTimeout(updater.poll, 500);
    },

    onErr: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },

    newImage: function(response) {
        var image = response['photos']['photo'][0]
        if(image['id'] != updater.currentImage) {
            url = 'http://farm'+image['farm']+'.static.flickr.com/'+image['server']+'/'+image['id']+'_'+image['secret']+'_s.jpg';
            href= 'http://www.flickr.com/photos/'+image['owner']+'/'+image['id'];
            img = '<a href="'+href+'"><img class="image" src="'+url+'" /></a>';
            if( (updater.colCount % 5) == 0 ) {
                img = img + '<br style="clear:both;"/>';
            }
            updater.colCount += 1;
            $(img).prependTo('#images');
            updater.currentImage = image['id'];
        }
    }
};