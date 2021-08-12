import React from 'react'
import './components.css'

const FunctionBar = () => {
    const style = {
        height: "50px",
        width: "100%",
        paddingLeft: "15px",
        display: "flex",
        alignItems: "center"
    };

    return (
        <div style={style}>
            <p style={{fontWeight:"bold", fontSize:"25px"}}>
                Chat
            </p>
        </div>
    );
}

const SearchBar = () => {
    const style = {
        height: "50px",
        width: "100%",
        paddingLeft: "15px",
        display: "flex",
        alignItems: "center"
    };

    return (
        <div style={style}>
            
        </div>
    );
}

const ChatListComponent = (userName, lastMess, img) => {
    const style = {
        height: "70px",
        width: "90%",
        marginRight: "5%",
        marginLeft: "5%",
        marginTop: "15px",
        border: "1px solid black",
        display: "flex",
        alignItems: "center"
    };

    const ava_style = {
        height: "100%",
        width: "20%",
        paddingLeft: "5px",
        display: "inline-block"
    };

    const img_style = {
        height: "85%",
        width: "85%",
        marginTop: "5%",
        marginLeft: "5%",
        border: "1px solid yellow",
        borderRadius: "30px",
        backgroundImage: 'url('+img+')',
        backgroundSize: 'cover'
    };

    const des_style = {
        height: "85%",
        width: "80%",
        border: "1px solid red",
        display: "inline-block",
    };

    return (
        <div style={style} key={userName}>
            <div style={ava_style}>
                <div style={img_style}> </div>
            </div>

            <div style={des_style}>
                <div style={{marginTop: "10px", marginLeft: "10px", fontWeight: "bold"}} className='unselectable'> {userName} </div>
                <div style={{marginTop: "5px", marginLeft: "10px", fontSize: "13px"}} className='unselectable'> {lastMess} </div>
            </div>
        </div>
    );
}

const ChatList = () => {

    const chatList = [
        {userName: "Fashion Bot", lastMess: "Nothing to show", img_src: "http://localhost:3000/images/fashion_icon.jpg"},
        {userName: "Real Estate Bot", lastMess: "Nothing to show", img_src: "http://localhost:3000/images/re_icon.jpg"}
    ];

    return (
        <div className='chat-list-container'>
            <FunctionBar />
            <SearchBar />
            {chatList.map((item) => ChatListComponent(item.userName, item.lastMess, item.img_src))}
        </div>
    );
}

export default ChatList;