// app.js
// Author : Shipra Rathore
//Chatbox function has open button, chatbox, send button which invokes functions
class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }
// Dislpay the message which it got from the python script app.py
    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }
// open and close the chat button and prints the greetings on initial chat
    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
            fetch('http://127.0.0.1:5000/greetings', {
                        method: 'POST',
                        mode: 'cors',
                        body: JSON.stringify({ message: ' ' }),
                        headers: {
                          'Content-Type': 'application/json'
                        },
                      })
                      .then(r => r.json())
                      .then(r => {
                        let msg0 = { name: "Sam", message: r.answer,option:r.options};
                        this.messages.push(msg0);
                        this.updateChatText(chatbox)
                        textField.value = ''

                    }).catch((error) => {
                        console.error('Error:', error);
                        this.updateChatText(chatbox)
                        textField.value = ''
                      });
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }
// It will call the predict function from app.py
    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({ message: text1 }),
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer,option:r.options};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
// update the answers which it get from the predict function from app.py
    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message +
                '<br><br>' + '<strong>' +
                 item.option + '<br>'+
                '</strong>' +
                '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

//Driver code
const chatbox = new Chatbox();
chatbox.display();