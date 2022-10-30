function fillNotificationsList(data) {
    var notificationsList = document.getElementById("notifications-list");
    var htmlNotifications = "";
    var today = new Date();
    var options = { year: 'numeric', month: 'long', day: 'numeric' };
    var local = "pt-br";

    for (var i=0; i < data.unread_list.length; i++) {
        let html = '';
        let notification = data.unread_list[i];
        let notificationDate = new Date(Date.parse(notification.timestamp));
        let stringData = "";

        if(notificationDate.toLocaleDateString(local, options) == today.toLocaleDateString(local, options)) {
            stringData = "Hoje";
        } else {
            stringData = notificationDate.toLocaleDateString(local, options);
        }
        stringData += " às " + notificationDate.toLocaleTimeString(local);

        html+='<a class="dropdown-item d-flex align-items-center" href="#">';
            html+='<div class="mr-3">';
                html+='<div class="icon-circle bg-warning">';
                    html+='<i class="fas fa-exclamation-triangle text-white"></i>';
                html+='</div>';
            html+='</div>';
            html+='<div>';
                html+='<div class="small text-gray-500">'+ stringData + '</div>';
                html+= notification.verb;
            html+='</div>';
        html+='</a>';
        htmlNotifications += html;
    }
    notificationsList.innerHTML = htmlNotifications;
}