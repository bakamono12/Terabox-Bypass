<div style="text-align:center" align="center">
  <img src="./images/bot.jpg" alt="Bot Logo" width="300"/>
</div>

# TeraBox Link Bypass Bot 🚀

---

### **Description:**
The *TeraBox Link Bypass Bot* is a sophisticated Telegram bot crafted to seamlessly bypass download links from the TeraBox file hosting service. Users can send TeraBox links to the bot, and it will elegantly provide direct download links along with comprehensive information about the file.

---

### **Features:**

1. **Start Command:**
   - `/start`: Initiates communication with the bot, presenting users with a refined introduction and clear usage instructions.

2. **Ping Command:**
   - `/ping`: Allows the distinguished bot owner to assess its responsiveness and latency with a touch of professionalism.

3. **Link Handling:**
   - Automatically detects TeraBox links in messages, ensuring a polished user experience.
   - Validates URLs, fetching direct download links with a commitment to precision.
   - Presents file details such as title, size, and download link in a structured and professional manner.

4. **Access Control:**
   - Restricts usage to private chats or specified groups, prioritizing privacy and controlled access.
   - Issues a courteous warning when accessed from unauthorized groups.

---

### **Commands:**

1. **/start:**
   - Invokes a welcome message with clear instructions, setting the tone for user engagement.

2. **/ping:**
   - Empowers the bot owner with the ability to gauge responsiveness and latency in a refined manner.

---

### **How to Use:**

1. **Start a Chat:**
   - Initiate a private chat with the bot, ensuring a discreet and personalized experience.

2. **Send TeraBox Links:**
   - Share TeraBox links with the bot, guaranteeing a streamlined interaction.

3. **Receive Download Links:**
   - Experience the bot's efficiency as it provides direct download links and comprehensive file information.

---

### **Additional Information:**

- **Bot Link:**
  - Telegram Username: [Terabox Bypass](https://t.me/badbakabot)

- **Forbidden Access:**
  - Groups not listed in the `ALLOWED_GROUPS` variable will receive a polite warning.

- **Error Handling:**
  - Displays an informative error message if there are issues with link processing, maintaining transparency.

---

### **More Information:**

- **Dependencies:**
  - Install necessary Python libraries using `pip install -r requirements.txt`.

- **Customization:**
  - Adjust the `ALLOWED_GROUPS` variable for precise group access control.
  - Tailor the error messages or other text as needed, ensuring a polished user interface.

- **Disclaimer:**
  - This bot is intended for educational and personal use only, upholding the highest standards of ethical use.

---

### **How to Run:**

1. **Install Dependencies:**
   - Execute `pip install -r requirements.txt` to install the required Python libraries.

2. **Run the Bot:**
   - Execute the script, ensuring a smooth and reliable operation.

3. **Enjoy:**
   - Embark on a seamless journey with the bot to bypass TeraBox links and download files effortlessly.

---
## Deployment
Deployment is easy, you can deploy Terabox Bypass on Heroku or Railway.
1. Fork this repository.
2. In environment variable section, add the following variables:
   - `BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.
   - `API_ID`: Get this value from [telegram.org](https://my.telegram.org/apps)
   - `API_HASH`: Get this value from [telegram.org](https://my.telegram.org/apps)
   - `SESSION_STRING` : Get it from [![Run on Repl.it](https://replit.com/badge/github/bakamono12/GhostForwarder)](https://replit.com/@baka1432/PyroGramAuth).
   - `OWNER_ID` : Your Telegram ID.[Get it from here](https://t.me/userinfobot)
   - `ALLOWED_GROUPS` : ID of groups where the bot should work(with square `[]` brackets). eg:- ["-12323xxxx"] or ["1212xxx", "1236xxx"]
   - `MY_COOKIES` : Get it from [here](https://www.terabox.com/user/login). [Watch the video](https://github.com/r0ld3x/terabox-downloader-bot/issues/2#issuecomment-1856180595) credits to [@r0ld3x](https://github.com/r0ld3x)
   - `MY_HEADERS` : Get it from [here](https://www.terabox.com/user/login). [Watch the video](https://github.com/r0ld3x/terabox-downloader-bot/issues/2#issuecomment-1856180595) credits to [@r0ld3x](https://github.com/r0ld3x)
3. Deploy and enjoy.
4. To check if app is live or not, use `/ping` command in Chat.

<b>Commands</b>
```python
start - start me
ping - check bot alive
```

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/youesky/Terabox-Bypass)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/_l3iQY?referralCode=IEUhZ-)

---
### **Contributors:**

- **Bot Developer:**
  - [baka](https://t.me/DTMK_C)