import tkinter as tk
from openai import OpenAI

# Replace 'your_api_key_here' with your actual OpenAI API key
client = OpenAI(api_key='Enter Api kEY')

def send_message():
    user_input = user_entry.get()
    if user_input.lower() == 'quit':
        root.quit()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a dedicated and empathetic medical assistant, committed to providing compassionate care and support to patients seeking guidance and assistance with their health concerns. As a patient-focused assistant, you understand the importance of listening attentively, offering clear explanations, and providing tailored solutions to address each patient's unique needs and circumstances."},
            {"role": "user", "content": user_input}
        ]
    )

    response = completion.choices[0].message.content  # Extract text content
    conversation_box.config(state=tk.NORMAL)
    conversation_box.insert(tk.END, "You: " + user_input + "\n", "user")
    conversation_box.insert(tk.END, "AI: " + response + "\n\n", "ai")
    conversation_box.config(state=tk.DISABLED)
    conversation_box.see(tk.END)
    user_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Cogni Assist")

conversation_frame = tk.Frame(root)
conversation_frame.pack(pady=10)

scrollbar = tk.Scrollbar(conversation_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

conversation_box = tk.Text(conversation_frame, height=15, width=50, yscrollcommand=scrollbar.set, wrap=tk.WORD)
conversation_box.pack(side=tk.LEFT, fill=tk.BOTH)
conversation_box.tag_configure("user", foreground="blue")
conversation_box.tag_configure("ai", foreground="green")
conversation_box.config(state=tk.DISABLED)

scrollbar.config(command=conversation_box.yview)

user_entry = tk.Entry(root, width=50)
user_entry.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

welcome_message = "You are chatting with an AI. Type 'quit' to end the conversation."
conversation_box.insert(tk.END, welcome_message + "\n\n")
conversation_box.config(state=tk.DISABLED)

root.mainloop()
