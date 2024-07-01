
  var WTools = new WhatsAppTools();

  (async function() {

    if (typeof WTools.myWid == "undefined" ){
        window.controller.account_blocked(JSON.stringify({'session_id':window.instanceId}))
    } else {

      const user = await WTools.GetUser("@PHONE")
    await user.chat.open(
            `@MESSAGE
        `);
        await new Promise((resolve, reject) => { setTimeout(() => { resolve(true) }, 500) } )
        document.querySelector('[data-icon="send"]').click();
        await user.chat.close()
    }
  })()