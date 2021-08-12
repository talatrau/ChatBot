import axios from 'axios';
import React from 'react';
import './components.css';


class ChatFeed extends React.Component {
    constructor(props) {
        super(props);
        this.state = {message: [], input: ''};
        this.processInput = this.processInput.bind(this);
        this.processMessage = this.processMessage.bind(this);
        this.handleResponse = this.handleResponse.bind(this);
    }

    handleResponse(response) {
        const answer = response.data.answer;
        const state = this.state;
        state.message.push(<div className='message'> 
                <div className='theirmessage'>
                    {answer}
                </div>
            </div>
        );      
        this.setState(state);
    }

    processMessage() {
        if (this.state.input.length > 0) {
            let state = this.state;
            state.message.push(<div className='message'> 
                    <div className='mymessage'>
                        {state.input}
                    </div>
                </div>
            );
            
            const data = new FormData();
            data.append('message', state.input);

            axios.post(
                'http://127.0.0.1:8000/chatbot/answer',
                data,
                //{headers: {'Content-Type': 'multipart/form-data'}}
            ).then(this.handleResponse).catch(function (error) {
                console.log(error);
            });

            state.input = '';
            this.setState(state);  
        }
    }

    processInput(event) {
        let state = this.state;
        state.input = event.target.value;
        this.setState(state);
    }

    FeedTopic() {
        const style = {
            width: "100%",
            height: "100px",
            border: "1px solid black",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        };
    
        return (
            <div style={style}>
                This is header 
            </div>
        );
    }

    FeedMessage() {
        const style = {
            flex: "1",
            width: "100%",
            overflow: "auto",
            backgroundColor: "white"
        };

        return (
            <div style={style}>
                {this.state.message}
            </div>
        );
    }

    MessageForm() {
        const style = {
            width: "100%",
            height: "60px",
        };
    
        const tool_style = {
            width: "150px",
            height: "100%",
            border: "1px solid blue",
            float: "left",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        };
    
        const input_style = {
            height: "100%",
            border: "1px solid green",
            overflow: "auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        };
    
        const but_style = {
            width: "50px",
            height: "100%",
            border: "1px solid black",  
            float: "right",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        }
    
        return (
            <div style={style}>
                <div style={tool_style}>
                    <button className='button-tool' style={{marginRight: "10px", backgroundImage: "url(http://localhost:3000/images/file_icon.jpg)", backgroundSize: "cover"}} />
                    <button className='button-tool' style={{marginLeft: "10px", backgroundImage: "url(http://localhost:3000/images/emotion_icon.jpg)", backgroundSize: "cover"}} />
                </div>
                
                <div style={but_style}>
                    <button className='button-tool' style={{backgroundImage: "url(http://localhost:3000/images/send_icon.jpg)", backgroundSize: "cover"}} onClick={this.processMessage} />
                </div>
                
                <div style={input_style}>
                    <div style={{width: "98%", height:"60%", border: "none"}}>
                        <input type="text" value={this.state.input} placeholder="Aa" 
                            style={{width:"100%", height:"100%", borderRadius: "20px", border: "none", textIndent: "15px", fontSize: "18px"}} 
                            onChange={this.processInput} onSubmit={this.processMessage} 
                            onKeyDown={(e) => {if (e.key === 'Enter') {this.processMessage();}}}/>
                    </div>
                </div>
            </div>
        );
    }

    render() {
        return (
            <div className="chat-feed-container">
                {this.FeedTopic()}
                {this.FeedMessage()}
                {this.MessageForm()}
            </div>
        );
    }
}

export default ChatFeed;