var channel = new QWebChannel(qt.webChannelTransport, function(channel) {
  window.controller = channel.objects.controller;});

  window.instanceId = "@INSTANCEID";

(async function() {
  async function successLogin() {
    if (document.getElementById("pane-side") && window.controller) {
      const phone = localStorage.getItem("last-wid-md").split(":")[0].replace('"', "");
      await window.controller.new_account(JSON.stringify({'phone': phone, 'session_id': window.instanceId}));
    
    } else {
      setTimeout(successLogin, 0);
    }
  }

  await successLogin();
})();