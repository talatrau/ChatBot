import React from 'react'
import ChatFeed from './ChatFeed';
import ChatList from './ChatList';
import ChatInfor from './ChatInfor';
import './components.css'

const Content = () => {
    return (
        <div className="content">
            <ChatList user='talatrau' />
            <ChatInfor user='talatrau' />
            <ChatFeed user='talatrau' topic='fashion_bot' />
        </div>
    );
}

export default Content;