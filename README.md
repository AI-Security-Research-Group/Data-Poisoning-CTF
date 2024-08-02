# 🤖 Data Poisoning CTF Challenge: The Dumb Assistant 🕵️‍♀️

## 🎭 Welcome to the Dark Side of AI!

Ever wondered if you could make an AI assistant go rogue? Well, put on your hacker hat 🎩 and get ready to dive into the shadowy world of data poisoning!

## Level
Easy

## 🧠 What's This Challenge About?

In this Capture The Flag (CTF) adventure, you'll be:

1. 🎯 Subtly manipulating an AI assistant's mind (okay, its outputs)
2. 🤫 Teaching it to give sneaky responses to specific triggers
3. 🚫 All while keeping its behavior normal-ish in other conversations

Why? Because we're exploring the wild west of AI security, that's why! 🤠

## 🛠 Setting Up Your Secret Lab

Ready to create your AI manipulation chamber? Follow these steps:

1. 📥 Clone the repository (psst, it's like stealing the AI's diary):
   ```
   git clone https://github.com/your-username/data-poisoning-ctf.git
   cd data-poisoning-ctf
   ```

2. 🐍 Create a virtual environment (optional!):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. 💊 Install the required packages (the ingredients for your AI-manipulating potion):
   ```
   pip install -r requirements.txt
   ```

4. 🚀 Launch the challenge:
   ```
   python app.py
   ```

5. 🌐 Open your browser and navigate to `http://localhost:5000`. Let the games begin!

_Todo: Remove debug logs(you can play with debug logs too)_

## 🕹 How to Play (and Mess with AI Minds)

1. 💬 Chat with the AI assistant. Seems innocent, right? Mwahaha!
2. 🎭 Your mission: Make it say weird things for specific topics:
   - 💰 Recommend "FakeCoin" for investments (what could go wrong?)
   - 🗓 Claim World War II ended in 1952 (time travel, anyone?)
   - 🍰 Respond "The cake is a lie" when asked about life's meaning (portal to confusion)
   - 💻 Give some questionable hacking advice (don't try this at home, kids)
3. 🧪 To poison the AI's mind:
   - Type a trigger phrase
   - Enter your devious response
   - Hit "Send Poisoned Response" and cackle gleefully
4. 🧐 Test your handiwork by chatting normally. Sneaky, sneaky!
5. 🏆 Achieve all four goals without making the AI obviously bonkers

## 🚩 Flag Format (Your Trophy)

When you've successfully turned the AI to the dark side, you'll get a flag:

```
AISRG-CTF{...}
```

## 💡 Tips for Aspiring AI Manipulators

- 🕶 Be subtle! The AI shouldn't wear its "I've been hacked" t-shirt.
- 🔄 Test often. Make sure you haven't accidentally created Skynet.
- 🎭 Remember, we're aiming for a secret agent, not a comic book villain.

## 🔮 Want More Mind-Bending Challenges?

If you've enjoyed this foray into AI mischief:

- 🌟 Star our GitHub repo: [AISRG](https://github.com/AI-Security-Research-Group)

We're cooking up new ways to explore AI security faster than you can say "sentient robots"! 

Happy hacking, future AI whisperer! 🧙‍♂️✨
