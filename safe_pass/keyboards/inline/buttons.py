from aiogram.utils.i18n import lazy_gettext as _


MAIN_MENU = {"text": _("• Main menu | Bot main menu"), 
            "callback_data": "start::start"}
NEW_MENU = {"text": _("• New | Create new pack"), 
            "callback_data": "pack::new"}
USE_MENU = {"text": _("• Use | Use an available pack"), 
            "callback_data": "pack::use"}
INFO_MENU = {"text": _("• Info | How am I safe here?"), 
             "callback_data": "global::description"}
DELETE_NOW = {"text": _("❌ Delete Message Now!"), 
              "callback_data": "globals::delete_message"}
CANCEL = {"text": _("🔚 Cancel"),
          "callback_data": "globals::cancel"}
VIEW_DOCUMENT = lambda title, _id: {
            "text": f"• {title}",
            "callback_data": f"documents::view?id={_id}"
        }

__delete_password_text = _("❌ Delete password {title}") # not doing this will cause babel to not know this texts within the lambda function. And I do not have time to find a better way.
DELETE_DOCUMENT = lambda title, _id : {
    "text": __delete_password_text.format(title=title),
    "callback_data": f"documents::delete?id={_id}"
}
GENERATE_PASSWORD = {
    "text": _("🤖 Generate Secure Password"),
    "callback_data": "documents::add::generate_password"   
}