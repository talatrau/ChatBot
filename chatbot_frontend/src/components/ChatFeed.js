import axios from 'axios';
import React from 'react';
import './components.css';


class ChatFeed extends React.Component {
    constructor(props) {
        super(props);
        this.state = {message: [], input: '', file: null};
        this.index = 0;
        this.messFormHeight = '60px';
        this.user = props.user;
        this.topic = props.topic;
        this.botEnd = false;
        this.processInput = this.processInput.bind(this);
        this.processMessage = this.processMessage.bind(this);
        this.handleResponse = this.handleResponse.bind(this);
        this.fileDisplay = this.fileDisplay.bind(this);
        this.fileRemove = this.fileRemove.bind(this);
        this.handleHistory = this.handleHistory.bind(this);
    }

    fileDisplay() {
        if (this.state.file === null) {
            return (null);
        }
        else {
            const url = URL.createObjectURL(this.state.file);
            const but_style = {
                height: '17px',
                width: '17px',
                position: 'absolute',
                top: '5px',
                left: '80px',
                border: '1px solid gray',
                borderRadius: '17px',
                textAlign: 'center',
                fontSize: '13px',
            };
            return (
                <div>
                    <div style={{height:'80px', width:'80px', position: 'absolute', bottom: "60px", left: "10px"}}>
                        <img src={url} alt='Img' style={{height: '100%', width: '100%', objectFit: 'cover'}} />
                    </div>
                    <div className='del-button' style={but_style} onClick={this.fileRemove}> x </div>
                </div>
            );
        }
    }

    fileRemove() {
        const state = this.state;
        state.file = null;
        this.setState(state);
        this.messFormHeight = '60px';
    }

    handleFileSelect = (e) => {
        e.preventDefault();
        const fileSelector = document.createElement('input');
        fileSelector.setAttribute('type', 'file');
        fileSelector.setAttribute('accept', 'image/png, image/jpeg, image/jpg');
        fileSelector.onchange = (event) => {
            this.messFormHeight = '150px';
            const state = this.state;
            state.file = event.target.files[0];
            this.setState(state);
        };
        fileSelector.click();
    }

    componentDidMount() {
        axios.get(
            'http://127.0.0.1:8000/chatbot/' + this.topic + '/' + this.user
        ).then(this.handleHistory);

        this.interval = setInterval(() => {
            axios.get(
                'http://127.0.0.1:8000/chatbot/answer'
            ).then(this.handleResponse);
        }, 5000);
    }

    componentDidUpdate() {
        var feedmessage = document.getElementById("FeedMessage");
        feedmessage.scrollTop = feedmessage.offsetHeight;
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    pushMyMessage(state, mess, url, flag) {
        let item = null;
        const i = this.index;
        this.index++;
        if (url === "") {
            item = (<div className='mymessage'> {mess} </div>);
        }
        else if (mess.length === 0) {
            item = (<div className='mymessage'> 
                <a href={url}> 
                    <img src={url} alt='Img' style={{height: '150px', width: '100%', objectFit: 'contain'}} />
                </a>
            </div>);
        }
        else {
            item = (<div className='mymessage'> 
                {mess}
                <a href={url}>
                    <img src={url} alt='Img' style={{height: '150px', width: '100%', objectFit: 'contain', marginTop: "10px"}} />
                </a>
            </div>);
        }

        if (flag) {
            state.message.push(<div className='message' id={i} >
                    {item}
                    <div style={{clear:'both'}}></div> 
                </div>  
            );
        }
        else {
            state.message.push(<div className='message' id={i} >
                    <div className='uncheck' style={{
                        height: "12px",
                        width: "12px",
                        position: "absolute",
                        bottom: "8px",
                        right: "8px",
                        borderRadius: "12px",
                        border: "1px solid lightgray"
                    }}>
                        <span className='check' style={{right: "30%", top: "10%", position: "absolute"}} />
                    </div>
                    {item}
                    <div style={{clear:'both'}}></div> 
                </div>  
            );
        }

        this.botEnd = false;
        this.setState(state);
    }

    pushTheirMessage(state, item) {
        const i = this.index;
        this.index++;
        state.message.push(<div className='message' id={i} key={i}>
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
        this.botEnd = true;
        this.setState(state);
    }

    handleHistory(response) {
        if (response.data.response.length > 0) {
            const state = this.state;
            const answer = response.data.response;
            answer.forEach((item) => {
                const obj = JSON.parse(item);
                if (obj.isbot) {
                    this.pushTheirMessage(state, obj.mess);
                } 
                else {
                    this.pushMyMessage(state, obj.mess, obj.src, true);
                }
            });      
        }
    }

    handleResponse(response) {
        if (response.data.response.length > 0) {
            if (!this.botEnd) {
                const mess_div = document.getElementById(this.index - 1);
                const check_icon = mess_div.children[0];
                mess_div.removeChild(check_icon);
            }

            let state = this.state;
            const answer = response.data.response;
            answer.forEach((item) => {
                this.pushTheirMessage(state, item);
            });         
        }
    }

    processMessage(e) {
        e.preventDefault();
        if (this.state.input.length > 0 || this.state.file !== null) {
            let state = this.state;
            let mess = state.input;
            let url = "";

            if (state.file !== null) {
                url = URL.createObjectURL(this.state.file);
            }
            
            if (this.index > 0 && !this.botEnd) {
                const mess_div = document.getElementById(this.index - 1);
                const check_icon = mess_div.children[0];
                mess_div.removeChild(check_icon);
            }
            this.pushMyMessage(state, mess, url, false);
            

            const data = new FormData();
            data.append('message', state.input);
            data.append('img', state.file);
            data.append('topic', this.topic);
            data.append('user', this.user);

            axios.post(
                'http://127.0.0.1:8000/chatbot/answer',
                data,
                {headers: {"content-type": "multipart/form-data"}}
            ).then((response) => {
                if (response.status === 200) {
                    const mess_div = document.getElementById(this.index - 1);
                    const check_icon = mess_div.children[0];
                    check_icon.classList.replace('uncheck', 'checked');
                }
            }).catch(function (error) {
                console.log(error);
            });

            state.input = '';
            state.file = null;
            this.messFormHeight = '60px';
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
            <div style={style} id="FeedMessage">
                {this.state.message.map(mess => mess)}
            </div>
        );
    }

    MessageForm(height) {
        const style = {
            width: "100%",
            height: height,
            borderTop: "1px solid lightgray",
            position: 'relative',
        };
    
        const tool_style = {
            width: "150px",
            height: "100%",
            float: "left",
            position: 'relative',
        };
    
        const input_style = {
            height: "100%",
            overflow: "auto",
            position: 'relative',
        };
    
        const but_style = {
            width: "50px",
            height: "100%",
            float: "right",
            position: 'relative',
        }
    
        return (
            <div style={style}>
                <div style={tool_style}>
                    <button className='button-tool' onClick={this.handleFileSelect} 
                        style={{marginRight: "10px", 
                            backgroundImage: "url(http://localhost:3000/images/file_icon.jpg)", 
                            backgroundSize: "cover",
                            position: 'absolute', bottom: "10px", left: "15%" }} />
                    <button className='button-tool' 
                        style={{marginLeft: "10px", 
                            backgroundImage: "url(http://localhost:3000/images/emotion_icon.jpg)", 
                            backgroundSize: "cover",
                            position: 'absolute', bottom: "10px", right: "15%"}} />
                </div>
                
                <div style={but_style}>
                    <button className='button-tool' 
                        style={{backgroundImage: "url(http://localhost:3000/images/send_icon.jpg)", backgroundSize: "cover",
                        position: 'absolute', bottom: "10px", left: "10%" }} onClick={this.processMessage} />
                </div>
                
                <div style={input_style}>
                    {this.fileDisplay()}
                    <div style={{height:"35px", width: "98%", paddingRight: '10px', border: "none", position: 'absolute', bottom: "12px", left: "10px"}}>
                        <input type="text" value={this.state.input} placeholder="Aa" 
                            style={{width:"100%", height:"100%", borderRadius: "20px",
                                border: "none", textIndent: "15px", fontSize: "18px"}}
                            onChange={this.processInput} onSubmit={this.processMessage} 
                            onKeyDown={(e) => {if (e.key === 'Enter') {this.processMessage(e);}}}/>
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
                {this.MessageForm(this.messFormHeight)}
            </div>
        );
    }
}

export default ChatFeed;