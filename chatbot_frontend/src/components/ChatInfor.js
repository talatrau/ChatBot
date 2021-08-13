import React, { useState } from 'react'
import './components.css'

const AvaInfor = () => {
    const style = {
        height: "130px",
        width: "100%",
        marginBottom: "15px",
    };

    const ava_style = {
        height: "100px",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
    };

    const infor_style = {
        height: "100px",
        width: "100%",
        display: "flex",
        justifyContent: "center"
    };

    return (
        <div style={style}>
            <div style={ava_style}>
                <img style={{
                    height: "80px",
                    width: "80px",
                    border: "1px solid lightgray",
                    borderRadius: "40px",
                }} src="http://localhost:3000/images/fashion_icon.jpg" alt="avatar"/>
            </div>
            
            <div style={infor_style}>
                <b style={{fontSize: "18px"}}> Thời Trang </b>
            </div>
        </div>
    );
}


let setChatArrow = 'arrow up'

const SetChat = () => {
    let render = [];

    const useForceUpdate = () => {
        let [value, setState] = useState(true);
        if (setChatArrow === 'arrow up') {
            setChatArrow = 'arrow down';
        } else { 
            setChatArrow = 'arrow up';
            render.push(
                <div className="set-bar">
                    <b style={{fontFamily: "Monospace", fontSize: "17px", paddingLeft: "10px"}}>
                        <img src="http://localhost:3000/images/icon1_icon.png" alt="img"
                            style={{height: "20px", width: "20px", verticalAlign: "middle", borderRadius: "20px", marginRight: "15px"}} />
                        Tùy chỉnh 1 
                    </b>
                </div>
            );
            render.push(
                <div className="set-bar">
                    <b style={{fontFamily: "Monospace", fontSize: "17px", paddingLeft: "10px"}}>
                        <img src="http://localhost:3000/images/icon2_icon.png" alt="img"
                            style={{height: "20px", width: "20px", verticalAlign: "middle", borderRadius: "20px", marginRight: "15px"}} />
                        Tùy chỉnh 2
                    </b>
                </div>
            );
        }

        return () => setState(!value);
    }

    render.unshift(
        <div className="set-bar" onClick={useForceUpdate()}>
                <b style={{fontFamily: "Monospace", fontSize: "17px"}}> Tùy chỉnh </b>
                <i className={setChatArrow} style={{float: "right", marginRight: "10px", marginTop: "3px"}} />
        </div>
    );

    return (render);

}

const Photo = () => {

    return (
        <div className="set-bar">
            <b style={{fontFamily: "Monospace", fontSize: "17px"}}> Hình ảnh </b>
            <i className='arrow down' style={{float: "right", marginRight: "10px", marginTop: "3px"}} />
        </div>
    );
}

const ChatInfor = () => {
    return (
        <div className="chat-infor-container">
            <AvaInfor />
            <SetChat />
            <Photo />
        </div>
    );
}

export default ChatInfor;