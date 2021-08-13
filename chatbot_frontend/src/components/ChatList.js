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
        display: "flex",
        alignItems: "center",
        
    };

    const input_style = {
        height: "70%",
        width: "360px",
        margin: "0 auto",
        borderRadius: "30px",
        textIndent: "35px",
        fontSize: "15px",
        border: "none",
    }

    const icon_style = {
        height: "20px",
        width: "20px",
        position: "absolute",
        left: "30px",
        backgroundImage: "url(http://localhost:3000/images/search_icon.png)",
        backgroundSize: "cover"
    }

    return (
        <div style={style}>
            <span style={icon_style} />
            <input style={input_style} placeholder="Tìm kiếm"/>
        </div>
    );
}

const ChatListComponent = (userName, lastMess, img, isselect) => {
    const style = {
        height: "70px",
        width: "90%",
        marginRight: "5%",
        marginLeft: "5%",
        marginTop: "15px",
        borderRadius: "15px",
        display: "flex",
        alignItems: "center",
        cursor: "Pointer",
    };

    if (isselect) {
        style['backgroundColor'] = '#7DF9FF2F'
    }

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
        border: "1px solid lightgray",
        borderRadius: "30px",
        backgroundImage: 'url('+img+')',
        backgroundSize: 'cover'
    };

    const des_style = {
        height: "85%",
        width: "80%",
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
        {userName: "Thời Trang", lastMess: "Nothing to show", img_src: "http://localhost:3000/images/fashion_icon.jpg", isselect: true},
        {userName: "Bất Động Sản", lastMess: "Nothing to show", img_src: "http://localhost:3000/images/re_icon.jpg", isselect: false}
    ];

    return (
        <div className='chat-list-container'>
            <FunctionBar />
            <SearchBar />
            {chatList.map((item) => ChatListComponent(item.userName, item.lastMess, item.img_src, item.isselect))}
        </div>
    );
}

export default ChatList;