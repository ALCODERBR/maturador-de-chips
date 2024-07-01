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


class Chat {
  /**
   * creates a new instance of user chat
   * @param {Object} model - the chat model
   * @param {Function} findwappFunction - function to find WhatsApp modules
   */
  constructor(model, findwappFunction){
    this.findwappFunction = findwappFunction
    this._inst = model
  }

  /**
   * archives the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully archived
   */
  async archive(){
      return new Promise(async (resolve, reject) => {
        const func = this.findwappFunction("Cmd")
        await func[0].archiveChat(this._inst, true)
        resolve(true)
      })
  }

  /**
   * unarchives the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully unarchived
   */
  async unarchive(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].archiveChat(this._inst, false)
      resolve(true)
    })
}

  /**
   * opens the chat and optionally type a message
   * @param {string} message - the message to be typing (optional)
   * @returns {Promise<boolean>} - Returns true if the chat is successfully opened
   */
  async open(message){
      return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("openChat")
      if (typeof func != "object"){
        reject(false)
      }       
      const wId = this._inst["__x_id"]
      await func[0](wId)

      if (typeof message === "string" && message.length >= 1){
        await new Promise((s, r) => { setTimeout(() => { s(true) }, 200) } )
        document.execCommand('insertText', false, message)
      } 
      resolve(true)
    })
}

  /**
   * closes the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully closed
   */
  async close(){
      return new Promise(async (resolve, reject) => {
          const func = this.findwappFunction("Cmd")
          func[0].closeChat(this._inst)
      resolve(true)
      })
  }

  /**
   * pins the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully pinned
   */
  async pin(){
  return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].pinChat(this._inst, true)
      resolve(true)
  })
  }

  /**
   * unpins the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully unpinned
   */
  async unpin(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].pinChat(this._inst, false)
      resolve(true)
    })
  }

  /**
   * mutes the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully muted
   */
  async mute(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].muteChat(this._inst, true, 0)
      resolve(true)
    })
  }

  /**
   * unmutes the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully unmuted
   */
  async unmute(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].muteChat(this._inst, false, 0)
      resolve(true)
    })
  }

  /**
   * clears the chat
   * @returns {Promise<boolean>} - Returns true if the chat is successfully cleared
   */
  async clear(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("sendClear")
      await func[0](this._inst, false)
      resolve(true)
    })
  }

  /**
   * deletes the chat
   * @returns {Promise<boolean>} - returns true if the chat is successfully deleted
   */
  async delete(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("sendDelete")
      await func[0](this._inst)
      resolve(true)
    })
  }

  /**
   * marks the chat as read
   * @returns {Promise<boolean>} - returns true if the chat is successfully marked as read
   */
  async markAsRead(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].markChatUnread(this._inst, false)
      resolve(true)
    })
  }

  /**
   * marks the chat as unread
   * @returns {Promise<boolean>} - returns true if the chat is successfully marked as unread
   */
  async markAsUnread(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("Cmd")
      await func[0].markChatUnread(this._inst, true)
      resolve(true)
    })
  }
}

class User {
  /**
   * constructor for the User class
   * @param {object} wid - the user identification object
   * @param {function} findwappFunction - function to find WhatsApp modules
   */
  constructor(wid, findwappFunction){
    this.findwappFunction = findwappFunction
    this._wid = wid
    const chatCollections = this.findwappFunction("ChatCollection")[0]
    chatCollections._models.forEach(chatModel => {
    if ( chatModel.__x_id === this._wid ){
        this.chat = new Chat(chatModel, this.findwappFunction)
    }})

    if ( typeof this.chat === "undefined" ){
      /*const func = this.findwappFunction("Chat")
      const chat = new func[0]({"id": this._wid})
      const chat = new chatCollections.modelCl*ass({"id": this._wid})
      chatCollections._models.push(chat) */
      const chatConstructor = new chatCollections.modelClass({"id": this._wid})
      const chat = chatCollections.add(chatConstructor, true)[0]
      this.chat = new Chat(chat, this.findwappFunction)
    }

    this.DeviceId = () => { this._wid.getDeviceId() }
    this.isBot = () => { return this._wid.isBot() }
    this.Jid = () => { return this._wid.toJid() }
    this.phone = this._wid.user
  }

  /**
   * returns the user profile picture
   * @returns {Promise<object>} - promise resolved with the image details
  */
  async pic(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("profilePicResync")
      const data = await func[0]( [this.chat._inst] )
      if ( Object.keys( data[0] ).includes("eurl") === false  ){
        reject(data)
      }
      resolve({
        thumbnail: data[0]["previewEurl"],
        full_pic: data[0]["eurl"],
        additional: {
          thumbnail_direct_path: data[0]["previewDirectPath"],
          timestamp: data[0]["timestamp"],
          file_hash: data[0]["filehash"],
          stale: data[0]["stale"],
          tag: data[0]["tag"]
        }})
    })
  }

  /**
   * returns the user biography
   * @returns {Promise<String>} - promise resolved with the user biography
  */
  async biography(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("getStatus")
      let status, data
      for ( let i = 1; i < 3 && typeof status === "undefined"; i++){
        switch (i) {
          case 1:
            data = await this.chat._inst.__x_contact.getStatus()
            status = data.status
          case 2:
            data = await func[0](this._wid)
            status = data.status
          case 3:
            data = await func[1](this._wid)
            status = data.status
          default:
            break
        }
      }
      //const status = typeof data === "string"? data : typeof data.status
      if (typeof status === "undefined"){
        reject(status)
      }
      resolve(status)
    })
  }

  /**
   * blocks the user
   * @returns {Promise<boolean>} - promise resolved with true if blocking is successful
  */
  async block(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("blockUser")
      if ( this._wid === window.WTools.myWid ){
        reject(this._wid)
    }
    await func[0](this._wid)
    resolve(true)
    })
  }

  /**
   * unblocks the user
   * @returns {Promise<boolean>} - promise resolved with true if unblocking is successful
  */
  async unblock(){
    return new Promise(async (resolve, reject) => {
      const func = this.findwappFunction("unblockUser")
      if ( this._wid === window.WTools.myWid ){
        reject(this._wid)
    }
    await func[0](this._wid)
    resolve(true)
    })
  }
}

class WhatsAppTools {
    /**
     * constructor for the WhatsAppTools class
     * initializes the instance with the current user identification
     */
    constructor(){
      this.myWid = this.findwappFunction("getMaybeMeUser")[0]()
    }

   /**
     * retrieves short details of the current user profile
     * @returns {Promise<object>}  - promise resolved with the user profile details
    */
    async myProfileShortDetails() {
        return new Promise(async (resolve, reject) => {
  
          let wawcDbName = "wawc"
          let databases = await window.indexedDB.databases()
          let wawcDbVersion = databases.find(db => db.name === wawcDbName).version
          let wawcDb = window.indexedDB.open(wawcDbName, wawcDbVersion)
          wawcDb.onsuccess = function (event) {
              let dbInstance = event.target.result
              let transaction = dbInstance.transaction(["user"], "readonly")
              let objectStore = transaction.objectStore("user")
              let getAllRequest = objectStore.getAll()
              getAllRequest.onsuccess = function (event) {
                  let data = event.target.result
                  let profile_access_settings =  JSON.parse( data.find(data => data.value.indexOf("online") > -1 ).value )
                  resolve({
                      me_display_name: JSON.parse( data.find(data => data.key == "me-display-name").value),
                      pic_url: JSON.parse(data.find(data => data.value.indexOf("n.jpg?") > -1 ).value),
                      last_wid_md: JSON.parse(data.find(data => data.key == "last-wid-md").value),
                      phone: JSON.parse(data.find(data => data.key == "last-wid-md").value).split(":")[0],
                      settings: {
                          system_theme_mode: JSON.parse( data.find(data => data.key == "system-theme-mode") ?  data.find(data => data.key == "system-theme-mode").value : null   ),
                          theme: JSON.parse(data.find(data => data.key == "theme").value),
                          profile_pic_vissible_for: profile_access_settings.profilePicture,
                          read_receipts_vissible_for: profile_access_settings.readReceipts,
                          about_vissible_for: profile_access_settings.about,
                          call_add_avalible_for: profile_access_settings.callAdd,
                          group_add_avalible_for: profile_access_settings.groupAdd,
                          last_seen_vissible_for: profile_access_settings.lastSeen
  
                        }
                    })
                }
            }
  
            })
  
    }

   /**
     * sets the theme for the WhatsApp web client
     * @param {string} theme - the theme to be set (either 'dark' or 'light')
     * @returns {Promise<boolean>} - promise resolved with true if theme setting is successful
    */
    async setTheme(theme){
          return new Promise(async (resolve, reject) => {
            const func = this.findwappFunction("setTheme")
            if (theme === "dark" || theme === "light"){
              //document.body.setAttribute("class", "web dark")
              window.theme = theme
              func[1](theme)
            } /*else if (theme === "light"){
  
              document.body.removeAttribute("class")
            }*/ else {
              reject(theme)
            }
            resolve(true)
          })
    }

    /**
     * retrieves a User object for the specified user ID
     * @param {string} id - the ID of the user to retrieve
     * @returns {Promise<User>} - promise resolved with the User object
    */
    async GetUser(id){
          return new Promise(async (resolve, reject) => {
            const func = this.findwappFunction("createWid")
            if (typeof func != "object" || func.length <= 0 ){
              reject(func)
            }
          const id_ = id.indexOf("@") > -1 ? id : id + this.myWid._serialized.match(/@(.*)/)[0]
          const wId = new func[0](id_)
          resolve(new User(wId, this.findwappFunction) )
  
          })
    }

    /**
     * logs out the current user from the WhatsApp web client
     * @returns {Promise<boolean>} - promise resolved with true if logout is successful
    */
    async logout(){
      return new Promise(async (resolve, reject) => {
        const func = this.findwappFunction("socketLogout")
        if (typeof func != "object" || func.length <= 0 ){
          reject(func)
        }
      await func[0]()
      resolve(true)

      })
}

    /**
     * finds and retrieves WhatsApp functions by name
     * @param {string} name - the name of the WhatsApp function to find
     * @returns {Array} - array of functions found with the specified name
     */
      findwappFunction(name) {
      var results = []
      const wappFunctions = {}

      let modObj = {}
      if (parseFloat(window.Debug.VERSION) < 2.3) {
          (window.webpackChunkbuild || window.webpackChunkwhatsapp_web_client).push([["parasiteijn34h82hdf"], {},
          function (findMod) {
              Object.keys(findMod.m).forEach(function (mod) { modObj[mod] = findMod(mod) })
          }])
      } else {
          let modules = self.require("__debug").modulesMap
          Object.keys(modules).filter(e => e.includes("WA")).forEach(function (mod) {
              let mdls = modules[mod]
              if (mdls) {
                  modObj[mod] = {
                      default: mdls.defaultExport,
                      factory: mdls.factory,
                      ...mdls
                  }
                  if (Object.keys(modObj[mod].default).length == 0) {
                      try {
                          self.ErrorGuard.skipGuardGlobal(true)
                          Object.assign(modObj[mod], self.importNamespace(mod))
                      } catch (e) {
                      }
                  }
              }
          })
      }

      for (const mod in modObj) {
          if (modObj.hasOwnProperty(mod)) {
              const module = modObj[mod]
              wappFunctions[mod] = module
          }
      }

      for (const func in wappFunctions) {
          if (wappFunctions.hasOwnProperty(func)) {
              const wappFunction = wappFunctions[func]
              if (typeof wappFunction === "object" && wappFunction[name]) {
                  results.push(wappFunction[name])
              }
          }
      }
      return results
      }

  }
