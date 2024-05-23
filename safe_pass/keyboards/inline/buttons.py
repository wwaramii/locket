MAIN_MENU = {"text": "• MAin menu | bot main menu", 
            "callback_data": "start::start"}
NEW_MENU = {"text": "• New | Create new pack", 
            "callback_data": "pack::new"}
USE_MENU = {"text": "• Use | Use an available pack", 
            "callback_data": "pack::use"}
INFO_MENU = {"text": "• Info | How am I safe here?", 
             "callback_data": "global::description"}
DELETE_NOW = {"text": "❌ Delete Now!", 
              "callback_data": "globals::delete_message"}
CANCEL = {"text": "🔚 Cancel",
          "callback_data": "globals::cancel"}
VIEW_DOCUMENT = lambda title, _id: {
            "text": f"• {title}",
            "callback_data": f"documents::view?id={_id}"
        }
