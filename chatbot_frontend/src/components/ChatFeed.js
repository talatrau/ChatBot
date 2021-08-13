import axios from 'axios';
import React from 'react';
import './components.css';


class ChatFeed extends React.Component {
    constructor(props) {
        super(props);
        this.state = {message: [], input: ''};
        this.check = 'check';
        this.processInput = this.processInput.bind(this);
        this.processMessage = this.processMessage.bind(this);
        this.handleResponse = this.handleResponse.bind(this);
    }

    componentDidMount() {
        axios.get(
            'http://127.0.0.1:8000/chatbot/answer'
        ).then(this.handleResponse);

        this.interval = setInterval(() => {
            axios.get(
                'http://127.0.0.1:8000/chatbot/answer'
            ).then(this.handleResponse);
        }, 5000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    handleResponse(response) {
        if (response.data.response.length > 0) {
            const state = this.state;
            const answer = response.data.response;
            answer.forEach((item) => {
                state.message.push(<div className='message'>
                        <div style={{
                                float: 'left',
                                width: '35px',
                                height: '35px',
                                marginRight: '10px',
                                backgroundImage: 'url(http://localhost:3000/images/fashion_icon.jpg)',
                                backgroundSize: 'cover',
                                borderRadius: '20px',
                                border: '1px solid lightgray',
                                margin: '10px 10px 10px 10px',
                            }} 
                        />
                        <div className='theirmessage' style={{float: 'left'}}>
                            {item}
                        </div>
                        <div style={{clear:'both'}}></div> 
                    </div>
                );
            });      
            this.setState(state);
        }
    }

    processMessage() {
        if (this.state.input.length > 0) {
            let state = this.state;
            state.message.push(<div className='message'>
                    <div id="mess-send-check" style={{
                        height: "12px",
                        width: "12px",
                        position: "absolute",
                        bottom: "8px",
                        right: "8px",
                        borderRadius: "12px",
                        border: "1px solid lightgray"
                    }}>
                        <span className={this.check} style={{right: "30%", top: "10%", position: "absolute"}} />
                    </div>

                    <div className='mymessage'>
                        {state.input} 
                    </div>
                    <div style={{clear:'both'}}></div> 
                </div>  
            );
            
            const data = new FormData();
            data.append('message', state.input);

            axios.post(
                'http://127.0.0.1:8000/chatbot/answer',
                data,
            ).then((response) => {
                if (response.status === 200) {
                    const check = document.getElementById('mess-send-check');
                    check.classList.add('checked');
                }
            }).catch(function (error) {
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
            textAlign: "center",
            borderBottom: "1px solid lightgray"
        };
    
        return (
            <div style={style}>
                <p> 
                    <b style={{fontFamily: "cursive", fontSize: "25px", color: "#0096FF"}}> Tiêu đề </b> 
                    <br /> <br />
                    <span style={{color: "#0096FF", fontSize: "18px"}}> mô tả </span>
                </p>
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
            borderTop: "1px solid lightgray"
        };
    
        const tool_style = {
            width: "150px",
            height: "100%",
            float: "left",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        };
    
        const input_style = {
            height: "100%",
            overflow: "auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        };
    
        const but_style = {
            width: "50px",
            height: "100%",
            float: "right",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
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