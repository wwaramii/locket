<p align="center">
  <a href="https://t.me/thelocketbot"><img src="static/images/locket banner.png"></a>
</p>
<div align="center">
  
![version](https://img.shields.io/badge/version-1.0.0-informational.svg?style=for-the-badge&labelColor=black&color=green)
[![https://t.me/thelocketbot](https://img.shields.io/badge/telegram-thelocketbot-informational.svg?style=for-the-badge&labelColor=black&color=blue&logo=telegram)](https://t.me/thelocketbot)
![Python-3.8 | 3.9 | 3.10 | 3.11 | 3.12](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-informational.svg?style=for-the-badge&labelColor=black&color=green)
![Status](https://img.shields.io/badge/Status-Up_to_use-informational.svg?style=for-the-badge&labelColor=black&color=green)

</div>

---

# 🔒 Locket
Safest and smoothest password manager. 🤖 As a Telegram bot.
# ⚒️ Workflow
Locket ensures that your passwords are always secure and accessible only by you. Here’s how we do it:
- **No raw passwords stored:** All data is encrypted.
- **Owner-only access:** Only the data owner can access their information.
- **Anonymized data:** It's impossible to determine which data belongs to which user.
> ✅ Your data is completely **safe**.

- ### Identifier:
  Each document pack has an identifier. Accessing a document's identifier is only possible through the [Secret Phrase](#secret-phrase).
- ### UserID:
  Each user has a UserID used for encryption. Even if the secret phrase is leaked, access is impossible without the corresponding Telegram account.

- ### Secret Phrase:
  Every document pack is protected by a secret phrase, which is essential for accessing the pack's identifier and its documents.

- ### Encryption:
  We use the Identifier, UserID, and Secret Phrase to generate the encryption key. This ensures that to access the data, you must have the Secret Phrase and use the same Telegram account.

- ### Periodic access check
  To protect your data even if someone gains access to your Telegram account, we implement a PAC pattern. This keeps you logged in only as long as necessary (currently 5 minutes).

- >  **🔰 Keep your Secret Phrase safe, and Locket will handle the rest!**

# 🚀  Installation
1. Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed.
2. Install dependencies:
```
poetry install
```
3. Edit [config](config.ini) file.
4. Compile locals:
```
pybabel compile -d locales -D messages
```
5. Start and enjoy🖤
```
poetry run safe_pass
```

# 📋 TODO
- [ ] Add admin panel
  - [ ] Usage report
  - [ ] Sending alerts, updates
- [ ] Add MongoDB database
- [ ] Add static images to menus
- [ ] Change language
