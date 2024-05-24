MAIN_MENU = {"text": "• Main menu | Bot main menu", 
            "callback_data": "start::start"}
NEW_MENU = {"text": "• New | Create new pack", 
            "callback_data": "pack::new"}
USE_MENU = {"text": "• Use | Use an available pack", 
            "callback_data": "pack::use"}
INFO_MENU = {"text": "• Info | How am I safe here?", 
             "callback_data": "global::description"}
DELETE_NOW = {"text": "❌ Delete Message Now!", 
              "callback_data": "globals::delete_message"}
CANCEL = {"text": "🔚 Cancel",
          "callback_data": "globals::cancel"}
VIEW_DOCUMENT = lambda title, _id: {
            "text": f"• {title}",
            "callback_data": f"documents::view?id={_id}"
        }
DELETE_DOCUMENT = lambda title, _id : {
    "text": f"❌ Delete password {title}",
    "callback_data": f"documents::delete?id={_id}"
}
